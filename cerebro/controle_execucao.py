from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
import json
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
    """Autoridade persistente mínima para claims, retry e reconciliação de tarefas."""

    def __init__(self, path: str | Path, lease_segundos: int = 300) -> None:
        if lease_segundos <= 0:
            raise ValueError("lease_segundos deve ser positivo")
        self.path = Path(path)
        self.lease_segundos = lease_segundos
        self.claims: dict[str, ClaimTarefa] = {}
        self._carregar()

    def claim(self, tarefa_id: str) -> ClaimTarefa:
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
        claim = self.claims.get(tarefa_id)
        if claim:
            self.claims[tarefa_id] = ClaimTarefa(**{**asdict(claim), "estado": "CONCLUIDA"})
            self.salvar()

    def falhar(self, tarefa_id: str, erro: str, *, retry_segundos: int | None = None) -> None:
        claim = self.claims.get(tarefa_id)
        if not claim:
            return
        retry_em = None
        estado = "FALHOU"
        if retry_segundos is not None:
            if retry_segundos < 0:
                raise ValueError("retry_segundos não pode ser negativo")
            retry_em = (agora() + timedelta(seconds=retry_segundos)).isoformat()
            estado = "RETRY_AGENDADO"
        self.claims[tarefa_id] = ClaimTarefa(**{**asdict(claim), "estado": estado, "retry_em": retry_em, "ultimo_erro": erro})
        self.salvar()

    def liberar(self, tarefa_id: str) -> None:
        claim = self.claims.get(tarefa_id)
        if claim:
            self.claims[tarefa_id] = ClaimTarefa(**{**asdict(claim), "estado": "LIBERADA"})
            self.salvar()

    def expirado(self, claim: ClaimTarefa) -> bool:
        return datetime.fromisoformat(claim.expira_em) <= agora()

    def reconciliar(self) -> list[str]:
        recuperadas: list[str] = []
        for tarefa_id, claim in list(self.claims.items()):
            if claim.estado == "ATIVA" and self.expirado(claim):
                self.claims[tarefa_id] = ClaimTarefa(**{**asdict(claim), "estado": "EXPIRADA", "ultimo_erro": "lease expirado"})
                recuperadas.append(tarefa_id)
        if recuperadas:
            self.salvar()
        return recuperadas

    def prontas_para_retry(self) -> list[str]:
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
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(
            json.dumps(
                {"versao": "0.1", "lease_segundos": self.lease_segundos, "claims": {k: asdict(v) for k, v in self.claims.items()}},
                ensure_ascii=False,
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )
        tmp.replace(self.path)

    def _carregar(self) -> None:
        if not self.path.exists():
            return
        dados = json.loads(self.path.read_text(encoding="utf-8"))
        self.claims = {k: ClaimTarefa(**v) for k, v in dados.get("claims", {}).items()}
