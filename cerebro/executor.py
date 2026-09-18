from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Protocol

from .controle_agente import ControleAgente
from .politica_execucao import Acao, PoliticaExecucao


class FonteContextual(Protocol):
    def candidatos_rede(self, contexto: dict[str, float] | None = None) -> list[tuple[str, float]]: ...


@dataclass
class PlanoCiclo:
    acao: Acao
    alvo: str | None = None
    contexto: dict[str, Any] = field(default_factory=dict)
    ferramenta: str | None = None
    recurso: str | None = None
    custo_estimado: float = 0.0
    cadeia: int = 1
    aprovacao: bool = False
    aprovacao_id: str | None = None
    correlation_id: str | None = None
    parent_id: str | None = None


class ExecutorCerebro:
    """Ponte entre sinais do Cérebro e execução autorizada.

    A política de autonomia continua sendo obrigatória. Quando um ControleAgente
    é fornecido, a autorização de identidade/escopo também passa a ser
    obrigatória e o resultado é registrado na telemetria.
    """

    def __init__(
        self,
        cerebro: FonteContextual | None = None,
        politica: PoliticaExecucao | None = None,
        controle: ControleAgente | None = None,
    ) -> None:
        if cerebro is None:
            from .servico import Cerebro
            cerebro = Cerebro()
        self.cerebro = cerebro
        self.politica = politica or PoliticaExecucao()
        self.controle = controle

    def selecionar(self, contexto: dict[str, float] | None = None) -> list[tuple[str, float]]:
        return self.cerebro.candidatos_rede(contexto)

    def executar(self, plano: PlanoCiclo, funcao: Callable[[PlanoCiclo], dict[str, Any]]) -> dict[str, Any]:
        ferramenta = plano.ferramenta or plano.acao.nome
        if not self.politica.autorizada(plano.acao, ferramenta=ferramenta, recurso=plano.recurso, custo_estimado=plano.custo_estimado, cadeia=plano.cadeia, aprovacao_id=plano.aprovacao_id):
            if self.controle:
                self.controle.registrar_resultado(
                    operacao=plano.acao.nome, estado="BLOQUEADO",
                    ferramenta=plano.ferramenta, recurso=plano.recurso,
                    correlation_id=plano.correlation_id, parent_id=plano.parent_id,
                    detalhes={"motivo": "ação fora da política de autonomia"},
                )
            return {"executado": False, "estado": "BLOQUEADO", "motivo": "ação fora da política de autonomia"}

        if self.controle:
            permitido, motivo = self.controle.verificar(
                operacao=plano.acao.nome,
                ferramenta=ferramenta,
                recurso=plano.recurso,
                nivel=int(plano.acao.nivel),
                custo_estimado=plano.custo_estimado,
                cadeia=plano.cadeia,
                aprovacao=plano.aprovacao,
                correlation_id=plano.correlation_id,
                parent_id=plano.parent_id,
            )
            if not permitido:
                return {"executado": False, "estado": "BLOQUEADO", "motivo": motivo}

        try:
            resultado = funcao(plano)
        except Exception as exc:
            if self.controle:
                self.controle.registrar_resultado(
                    operacao=plano.acao.nome, estado="FALHOU",
                    ferramenta=ferramenta, recurso=plano.recurso,
                    custo=plano.custo_estimado, correlation_id=plano.correlation_id,
                    parent_id=plano.parent_id, detalhes={"erro": str(exc)},
                )
            raise

        if plano.aprovacao_id:
            self.politica.consumir_aprovacao(plano.aprovacao_id)

        if self.controle:
            self.controle.registrar_resultado(
                operacao=plano.acao.nome, estado="CONCLUIDO",
                ferramenta=plano.ferramenta or plano.acao.nome,
                recurso=plano.recurso, custo=plano.custo_estimado,
                correlation_id=plano.correlation_id, parent_id=plano.parent_id,
            )
        return {"executado": True, "estado": "CONCLUIDO", "resultado": resultado}
