from __future__ import annotations

from contextlib import contextmanager
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
import fcntl
import json
import os
import uuid


def agora() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class ClaimTarefa:
    tarefa_id: str
    claim_id: str
    estado: str = "ATIVA"
    tentativa: int = 1
    adquirido_em: str = ""
    expira_em: str = ""
    retry_em: str | None = None
    ultimo_erro: str | None = None


class ControleExecucao:
    """Autoridade persistente para claims, retry e reconciliação de tarefas."""

    def __init__(self, path: str | Path, lease_segundos: int = 300) -> None:
        if lease_segundos <= 0:
            raise ValueError("lease_segundos deve ser positivo")
        self.path = Path(path)
        self.lock_path = self.path.with_suffix(self.path.suffix + ".lock")
        self.lease_segundos = lease_segundos
        self.claims: dict[str, ClaimTarefa] = {}
        self._carregar()

    @contextmanager
    def _lock(self):
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        with self.lock_path.open("a+") as arquivo:
            fcntl.flock(arquivo.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(arquivo.fileno(), fcntl.LOCK_UN)

    def _recarregar(self) -> None:
        if not self.path.exists():
            self.claims = {}
            return
        dados = json.loads(self.path.read_text(encoding="utf-8"))
        persistidos = {k: ClaimTarefa(**v) for k, v in dados.get("claims", {}).items()}
        # Mantém entradas locais ainda não persistidas (útil para composição/testes),
        # enquanto a versão persistida continua prevalecendo quando a chave existe.
        locais = {k: v for k, v in self.claims.items() if k not in persistidos}
        self.claims = {**locais, **persistidos}

    def claim(self, tarefa_id: str) -> ClaimTarefa:
        with self._lock():
            self._recarregar()
            existente = self.claims.get(tarefa_id)
            if existente and existente.estado == "ATIVA" and not self.expirado(existente):
                raise RuntimeError(f"tarefa já possui claim ativo: {tarefa_id}")
            tentativa = (existente.tentativa + 1) if existente else 1
            inicio = agora()
            claim = ClaimTarefa(
                tarefa_id=tarefa_id,
                claim_id=f"CLAIM-{uuid.uuid4().hex}",
                tentativa=tentativa,
                adquirido_em=inicio.isoformat(),
                expira_em=(inicio + timedelta(seconds=self.lease_segundos)).isoformat(),
            )
            self.claims[tarefa_id] = claim
            self.salvar()
            return claim

    def concluir(self, tarefa_id: str) -> None:
        with self._lock():
            self._recarregar()
            claim = self.claims.get(tarefa_id)
            if claim:
                self.claims[tarefa_id] = ClaimTarefa(**{**asdict(claim), "estado": "CONCLUIDA"})
                self.salvar()

    def falhar(self, tarefa_id: str, erro: str, *, retry_segundos: int | None = None) -> None:
        if retry_segundos is not None and retry_segundos < 0:
            raise ValueError("retry_segundos não pode ser negativo")
        with self._lock():
            self._recarregar()
            claim = self.claims.get(tarefa_id)
            if not claim:
                return
            retry_em = (agora() + timedelta(seconds=retry_segundos)).isoformat() if retry_segundos is not None else None
            estado = "RETRY_AGENDADO" if retry_em else "FALHOU"
            self.claims[tarefa_id] = ClaimTarefa(**{
                **asdict(claim),
                "estado": estado,
                "retry_em": retry_em,
                "ultimo_erro": erro,
            })
            self.salvar()

    def liberar(self, tarefa_id: str) -> None:
        with self._lock():
            self._recarregar()
            claim = self.claims.get(tarefa_id)
            if claim:
                self.claims[tarefa_id] = ClaimTarefa(**{**asdict(claim), "estado": "LIBERADA"})
                self.salvar()

    def expirado(self, claim: ClaimTarefa) -> bool:
        return datetime.fromisoformat(claim.expira_em) <= agora()

    def reconciliar(self) -> list[str]:
        with self._lock():
            self._recarregar()
            recuperadas: list[str] = []
            for tarefa_id, claim in list(self.claims.items()):
                if claim.estado == "ATIVA" and self.expirado(claim):
                    self.claims[tarefa_id] = ClaimTarefa(**{
                        **asdict(claim),
                        "estado": "EXPIRADA",
                        "ultimo_erro": "lease expirado",
                    })
                    recuperadas.append(tarefa_id)
            if recuperadas:
                self.salvar()
            return recuperadas

    def prontas_para_retry(self) -> list[str]:
        with self._lock():
            self._recarregar()
            agora_dt = agora()
            return [
                tarefa_id
                for tarefa_id, claim in self.claims.items()
                if claim.estado == "RETRY_AGENDADO"
                and claim.retry_em is not None
                and datetime.fromisoformat(claim.retry_em) <= agora_dt
            ]

    def salvar(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_name("." + self.path.name + "." + str(os.getpid()) + ".tmp")
        tmp.write_text(
            json.dumps(
                {
                    "versao": "0.2",
                    "lease_segundos": self.lease_segundos,
                    "claims": {k: asdict(v) for k, v in self.claims.items()},
                },
                ensure_ascii=False,
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )
        os.replace(tmp, self.path)

    def _carregar(self) -> None:
        self._recarregar()
