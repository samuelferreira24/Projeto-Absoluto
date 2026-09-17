from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
import json
import uuid


def agora() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class Missao:
    id: str
    objetivo: str
    estado: str = "ATIVA"
    contexto: dict[str, Any] = field(default_factory=dict)
    resultado: dict[str, Any] = field(default_factory=dict)
    criada_em: str = field(default_factory=agora)
    atualizada_em: str = field(default_factory=agora)

    def __post_init__(self) -> None:
        if not self.id or not self.objetivo:
            raise ValueError("id e objetivo são obrigatórios")
        if self.estado not in {"ATIVA", "PAUSADA", "CONCLUIDA", "FALHOU", "CANCELADA"}:
            raise ValueError(f"estado de missão inválido: {self.estado}")

    def atualizar(self, estado: str | None = None, resultado: dict[str, Any] | None = None) -> None:
        if estado is not None:
            self.estado = estado
        if resultado is not None:
            self.resultado = resultado
        self.atualizada_em = agora()


@dataclass
class RegistroExecucao:
    missao_id: str
    etapa: str
    estado: str
    detalhes: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=agora)
    ciclo_id: str | None = None
    idempotency_key: str | None = None


class Orquestrador:
    """Núcleo mínimo de execução contínua orientado a missão.

    Não impõe uma sequência fixa de trabalho: o executor recebe o estado
    atual e pode decidir qual caminho autorizado deve ser explorado.

    Cada ciclo possui uma identidade estável. Se um processo cair depois de
    iniciar um ciclo, a recuperação pode repetir o mesmo ciclo com a mesma
    chave de idempotência, permitindo que o executor/serviço externo dedupe
    efeitos colaterais.
    """

    def __init__(self, path: str | Path = "cerebro/data/orquestrador.json") -> None:
        self.path = Path(path)
        self.missoes: dict[str, Missao] = {}
        self.historico: list[RegistroExecucao] = []
        if self.path.exists():
            self.carregar()

    def registrar_missao(self, missao: Missao) -> None:
        if missao.id in self.missoes:
            raise ValueError(f"missão já existe: {missao.id}")
        self.missoes[missao.id] = missao
        self._registrar(missao.id, "MISSAO", "CRIADA", {"objetivo": missao.objetivo})
        self.salvar()

    def _registrar(self, missao_id: str, etapa: str, estado: str, detalhes: dict[str, Any] | None = None, ciclo_id: str | None = None, idempotency_key: str | None = None) -> None:
        self.historico.append(RegistroExecucao(missao_id, etapa, estado, detalhes or {}, ciclo_id=ciclo_id, idempotency_key=idempotency_key))

    def _ciclo_pendente(self, missao_id: str) -> RegistroExecucao | None:
        ciclos_terminados: set[str] = set()
        for registro in reversed(self.historico):
            if registro.missao_id != missao_id or registro.ciclo_id is None or registro.etapa != "CICLO":
                continue
            if registro.estado in {"CONCLUIDO", "FALHOU", "CANCELADO"}:
                ciclos_terminados.add(registro.ciclo_id)
            elif registro.estado == "INICIADO" and registro.ciclo_id not in ciclos_terminados:
                return registro
        return None

    def executar_um_ciclo(self, missao_id: str, executor: Callable[[Missao], dict[str, Any]], ciclo_id: str | None = None) -> dict[str, Any]:
        if missao_id not in self.missoes:
            raise KeyError(missao_id)
        missao = self.missoes[missao_id]
        if missao.estado != "ATIVA":
            return {"executado": False, "motivo": f"missão não está ativa: {missao.estado}"}

        pendente = self._ciclo_pendente(missao_id)
        ciclo_id = ciclo_id or (pendente.ciclo_id if pendente else f"CICLO-{uuid.uuid4().hex}")
        idempotency_key = f"{missao_id}:{ciclo_id}"
        contexto_original = dict(missao.contexto)
        missao.contexto = {**contexto_original, "_execucao": {"ciclo_id": ciclo_id, "idempotency_key": idempotency_key}}

        if pendente is None:
            self._registrar(missao_id, "CICLO", "INICIADO", {"objetivo": missao.objetivo}, ciclo_id, idempotency_key)
        self.salvar()
        try:
            resultado = executor(missao)
            missao.contexto = contexto_original
            missao.atualizar(resultado=resultado)
            self._registrar(missao_id, "CICLO", "CONCLUIDO", resultado, ciclo_id, idempotency_key)
            self.salvar()
            return {"executado": True, "resultado": resultado, "ciclo_id": ciclo_id, "idempotency_key": idempotency_key}
        except Exception as exc:
            missao.contexto = contexto_original
            detalhes = {"erro": type(exc).__name__, "mensagem": str(exc)}
            self._registrar(missao_id, "CICLO", "FALHOU", detalhes, ciclo_id, idempotency_key)
            missao.atualizar(resultado=detalhes)
            self.salvar()
            raise

    def salvar(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"schema_version": "0.2", "missoes": {k: vars(v) for k, v in self.missoes.items()}, "historico": [vars(v) for v in self.historico]}
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def carregar(self) -> None:
        dados = json.loads(self.path.read_text(encoding="utf-8"))
        self.missoes = {k: Missao(**v) for k, v in dados.get("missoes", {}).items()}
        self.historico = [RegistroExecucao(**v) for v in dados.get("historico", [])]
