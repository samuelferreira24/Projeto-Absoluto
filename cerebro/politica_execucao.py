from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Iterable


class NivelAutonomia(IntEnum):
    OBSERVAR = 0
    PESQUISAR = 1
    ACOES_REVERSIVEIS = 2
    DELEGAR = 3
    ALTERAR_SISTEMAS_AUTORIZADOS = 4
    PROPOR_ESTRATEGIA = 5
    ALTO_IMPACTO = 6


@dataclass(frozen=True)
class Acao:
    nome: str
    nivel: NivelAutonomia
    reversivel: bool = True
    exige_autorizacao: bool = False


class PoliticaExecucao:
    """Limite de autonomia independente do agente que executa a ação."""

    def __init__(self, nivel_maximo: NivelAutonomia = NivelAutonomia.ACOES_REVERSIVEIS) -> None:
        self.nivel_maximo = nivel_maximo

    def autorizada(self, acao: Acao) -> bool:
        if acao.exige_autorizacao:
            return False
        if acao.nivel > self.nivel_maximo:
            return False
        if not acao.reversivel and acao.nivel >= NivelAutonomia.ALTO_IMPACTO:
            return False
        return True

    def filtrar(self, acoes: Iterable[Acao]) -> list[Acao]:
        return [acao for acao in acoes if self.autorizada(acao)]
