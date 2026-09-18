from __future__ import annotations

from typing import Any

from .ativacao_portas import AtivadorPortas
from .ciclo_operacional import DecisaoOperacional, ResultadoOperacional
from .orquestrador import Missao


class ExecutorOperacionalPortas:
    """Adaptador entre decisões do ciclo e capacidades realmente ativadas.

    A decisão escolhe ferramenta/ação e argumentos; o adaptador resolve a
    implementação registrada nas portas e devolve evidência ao ciclo.
    """

    def __init__(self, ativador: AtivadorPortas) -> None:
        self.ativador = ativador

    def executar(self, missao: Missao, decisao: DecisaoOperacional) -> ResultadoOperacional:
        capacidade = decisao.ferramenta or decisao.acao
        if not capacidade:
            return ResultadoOperacional(
                sucesso=False,
                observacao="decisão não especificou ferramenta ou ação executável",
            )

        argumentos = dict(decisao.argumentos)
        ambiente = argumentos.pop("_ambiente", None)
        porta_id = argumentos.pop("_porta_id", None)

        resultado = self.ativador.executar(
            capacidade,
            ambiente=ambiente,
            porta_id=porta_id,
            missao=missao,
            decisao=decisao,
            **argumentos,
        )
        if not resultado.sucesso:
            return ResultadoOperacional(
                sucesso=False,
                observacao=resultado.erro or "falha na capacidade",
                dados={"porta_id": resultado.porta_id, "capacidade": resultado.capacidade},
            )

        dados: dict[str, Any]
        if isinstance(resultado.resultado, dict):
            dados = dict(resultado.resultado)
        else:
            dados = {"resultado": resultado.resultado}

        dados.update({"porta_id": resultado.porta_id, "capacidade": resultado.capacidade})
        return ResultadoOperacional(
            sucesso=True,
            observacao="capacidade executada através da porta ativa",
            dados=dados,
            evidencia=f"porta:{resultado.porta_id}",
        )
