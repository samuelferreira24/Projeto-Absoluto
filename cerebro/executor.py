from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from .politica_execucao import Acao, PoliticaExecucao
from .servico import Cerebro


@dataclass
class PlanoCiclo:
    acao: Acao
    alvo: str | None = None
    contexto: dict[str, Any] = field(default_factory=dict)


class ExecutorCerebro:
    """Ponte entre sinais do Cérebro e execução autorizada.

    A escolha concreta do trabalho permanece externa e contextual; esta
    camada somente aplica política, executa e devolve evidência do ciclo.
    """

    def __init__(self, cerebro: Cerebro | None = None, politica: PoliticaExecucao | None = None) -> None:
        self.cerebro = cerebro or Cerebro()
        self.politica = politica or PoliticaExecucao()

    def selecionar(self, contexto: dict[str, float] | None = None) -> list[tuple[str, float]]:
        return self.cerebro.candidatos_rede(contexto)

    def executar(self, plano: PlanoCiclo, funcao: Callable[[PlanoCiclo], dict[str, Any]]) -> dict[str, Any]:
        if not self.politica.autorizada(plano.acao):
            return {"executado": False, "estado": "BLOQUEADO", "motivo": "ação fora da política de autonomia"}
        resultado = funcao(plano)
        return {"executado": True, "estado": "CONCLUIDO", "resultado": resultado}
