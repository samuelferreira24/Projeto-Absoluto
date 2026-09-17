from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Protocol

from .politica_execucao import Acao, PoliticaExecucao


class FonteContextual(Protocol):
    def candidatos_rede(self, contexto: dict[str, float] | None = None) -> list[tuple[str, float]]: ...


@dataclass
class PlanoCiclo:
    acao: Acao
    alvo: str | None = None
    contexto: dict[str, Any] = field(default_factory=dict)


class ExecutorCerebro:
    """Ponte entre sinais do Cérebro e execução autorizada.

    Depende apenas do contrato contextual, evitando acoplamento circular ao
    serviço concreto do Cérebro e mantendo a camada de execução substituível.
    """

    def __init__(self, cerebro: FonteContextual | None = None, politica: PoliticaExecucao | None = None) -> None:
        if cerebro is None:
            from .servico import Cerebro
            cerebro = Cerebro()
        self.cerebro = cerebro
        self.politica = politica or PoliticaExecucao()

    def selecionar(self, contexto: dict[str, float] | None = None) -> list[tuple[str, float]]:
        return self.cerebro.candidatos_rede(contexto)

    def executar(self, plano: PlanoCiclo, funcao: Callable[[PlanoCiclo], dict[str, Any]]) -> dict[str, Any]:
        if not self.politica.autorizada(plano.acao):
            return {"executado": False, "estado": "BLOQUEADO", "motivo": "ação fora da política de autonomia"}
        resultado = funcao(plano)
        return {"executado": True, "estado": "CONCLUIDO", "resultado": resultado}
