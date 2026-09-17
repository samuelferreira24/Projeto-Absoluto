from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable
import json
from pathlib import Path


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


class Orquestrador:
    """Núcleo mínimo de execução contínua orientado a missão.

    Não impõe uma sequência fixa de trabalho: o executor recebe o estado
    atual e pode decidir qual caminho autorizado deve ser explorado.
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

    def _registrar(self, missao_id: str, etapa: str, estado: str, detalhes: dict[str, Any] | None = None) -> None:
        self.historico.append(RegistroExecucao(missao_id, etapa, estado, detalhes or {}))

    def executar_um_ciclo(self, missao_id: str, executor: Callable[[Missao], dict[str, Any]]) -> dict[str, Any]:
        if missao_id not in self.missoes:
            raise KeyError(missao_id)
        missao = self.missoes[missao_id]
        if missao.estado != "ATIVA":
            return {"executado": False, "motivo": f"missão não está ativa: {missao.estado}"}

        self._registrar(missao_id, "CICLO", "INICIADO")
        try:
            resultado = executor(missao)
            missao.atualizar(resultado=resultado)
            self._registrar(missao_id, "CICLO", "CONCLUIDO", resultado)
            self.salvar()
            return {"executado": True, "resultado": resultado}
        except Exception as exc:
            detalhes = {"erro": type(exc).__name__, "mensagem": str(exc)}
            self._registrar(missao_id, "CICLO", "FALHOU", detalhes)
            missao.atualizar(resultado=detalhes)
            self.salvar()
            raise

    def salvar(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": "0.1",
            "missoes": {k: vars(v) for k, v in self.missoes.items()},
            "historico": [vars(v) for v in self.historico],
        }
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def carregar(self) -> None:
        dados = json.loads(self.path.read_text(encoding="utf-8"))
        self.missoes = {k: Missao(**v) for k, v in dados.get("missoes", {}).items()}
        self.historico = [RegistroExecucao(**v) for v in dados.get("historico", [])]
