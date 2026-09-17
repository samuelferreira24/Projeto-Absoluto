from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EstadoCombinacao(str, Enum):
    NAO_TESTADA = "NAO_TESTADA"
    TESTADA = "TESTADA"
    PROMISSORA = "PROMISSORA"
    VALIDADA = "VALIDADA"
    INEFICIENTE = "INEFICIENTE"
    INCOMPATIVEL = "INCOMPATIVEL"
    CONTEXTUAL = "CONTEXTUAL"
    SUPERADA = "SUPERADA"


@dataclass(frozen=True)
class Capacidade:
    id: str
    nome: str
    entradas: tuple[str, ...] = ()
    saidas: tuple[str, ...] = ()
    recursos: tuple[str, ...] = ()
    dependencias: tuple[str, ...] = ()
    custo_estimado: float | None = None
    tempo_estimado: float | None = None
    confiabilidade: float | None = None


@dataclass(frozen=True)
class Tarefa:
    id: str
    objetivo: str
    capacidades: tuple[str, ...] = ()
    depende_de: tuple[str, ...] = ()
    recursos: tuple[str, ...] = ()

    @property
    def pode_executar_em_paralelo(self) -> bool:
        return not self.depende_de


@dataclass(frozen=True)
class Combinacao:
    id: str
    objetivo: str
    capacidades: tuple[str, ...]
    topologia: str = "SEQUENCIAL"
    estado: EstadoCombinacao = EstadoCombinacao.NAO_TESTADA
    resultado: str | None = None
    custo: float | None = None
    tempo: float | None = None
    qualidade: float | None = None
    evidencias: tuple[str, ...] = ()
    aprendizado: str | None = None
    metadados: dict[str, Any] = field(default_factory=dict)


def determinar_topologia(tarefas: tuple[Tarefa, ...]) -> str:
    """Classificação mínima: paralelo quando não há dependências entre tarefas; caso contrário, sequencial."""
    if not tarefas:
        return "VAZIA"
    if all(t.pode_executar_em_paralelo for t in tarefas):
        return "PARALELO"
    return "DEPENDENTE"


def recursos_em_conflito(tarefas: tuple[Tarefa, ...]) -> set[str]:
    """Retorna recursos compartilhados por mais de uma tarefa."""
    uso: dict[str, int] = {}
    for tarefa in tarefas:
        for recurso in tarefa.recursos:
            uso[recurso] = uso.get(recurso, 0) + 1
    return {recurso for recurso, quantidade in uso.items() if quantidade > 1}


def registrar_resultado(
    combinacao: Combinacao,
    *,
    estado: EstadoCombinacao,
    resultado: str,
    qualidade: float | None = None,
    custo: float | None = None,
    tempo: float | None = None,
    aprendizado: str | None = None,
    evidencia: str | None = None,
) -> Combinacao:
    """Cria uma nova versão do registro sem alterar a experiência anterior."""
    evidencias = combinacao.evidencias
    if evidencia and evidencia not in evidencias:
        evidencias = (*evidencias, evidencia)
    return Combinacao(
        id=combinacao.id,
        objetivo=combinacao.objetivo,
        capacidades=combinacao.capacidades,
        topologia=combinacao.topologia,
        estado=estado,
        resultado=resultado,
        custo=custo,
        tempo=tempo,
        qualidade=qualidade,
        evidencias=evidencias,
        aprendizado=aprendizado,
        metadados=dict(combinacao.metadados),
    )
