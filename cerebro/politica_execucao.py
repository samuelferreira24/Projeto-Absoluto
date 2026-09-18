from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from typing import Iterable, Sequence
import os


class NivelAutonomia(IntEnum):
    OBSERVAR = 0
    PESQUISAR = 1
    ACOES_REVERSIVEIS = 2
    DELEGAR = 3
    ALTERAR_SISTEMAS_AUTORIZADOS = 4
    PROPOR_ESTRATEGIA = 5
    ALTO_IMPACTO = 6


@dataclass(frozen=True)
class EscopoExecucao:
    executaveis_permitidos: tuple[str, ...] = ()
    diretorio_trabalho: str | None = None
    variaveis_ambiente_permitidas: tuple[str, ...] = ()
    timeout_segundos: int = 900

    def __post_init__(self) -> None:
        if self.timeout_segundos <= 0:
            raise ValueError("timeout_segundos deve ser positivo")

    @property
    def autorizado(self) -> bool:
        return bool(self.executaveis_permitidos)

    def validar_comando(self, argv: Sequence[str]) -> tuple[bool, str]:
        if not argv:
            return False, "comando vazio"
        executavel = Path(argv[0]).name
        permitidos = {Path(item).name for item in self.executaveis_permitidos}
        if executavel not in permitidos:
            return False, f"executável não permitido pelo escopo: {executavel}"
        if self.diretorio_trabalho is not None and not Path(self.diretorio_trabalho).is_dir():
            return False, f"diretório de trabalho inexistente: {self.diretorio_trabalho}"
        return True, "OK"

    def ambiente(self) -> dict[str, str]:
        return {nome: os.environ[nome] for nome in self.variaveis_ambiente_permitidas if nome in os.environ}


@dataclass(frozen=True)
class Acao:
    nome: str
    nivel: NivelAutonomia
    reversivel: bool = True
    exige_autorizacao: bool = False


class PoliticaExecucao:
    """Limite de autonomia independente do agente que executa a ação."""

    def __init__(
        self,
        nivel_maximo: NivelAutonomia = NivelAutonomia.ACOES_REVERSIVEIS,
        *,
        escopo: EscopoExecucao | None = None,
    ) -> None:
        self.nivel_maximo = nivel_maximo
        self.escopo = escopo or EscopoExecucao()

    def autorizada(self, acao: Acao) -> bool:
        if acao.exige_autorizacao:
            return False
        if acao.nivel > self.nivel_maximo:
            return False
        if not acao.reversivel and acao.nivel >= NivelAutonomia.ALTO_IMPACTO:
            return False
        return True

    def validar_executor_externo(self, acao: Acao, argv: Sequence[str]) -> tuple[bool, str]:
        if not self.autorizada(acao):
            return False, "ação fora da política de autonomia"
        if not self.escopo.autorizado:
            return False, "executor externo sem escopo técnico autorizado"
        return self.escopo.validar_comando(argv)

    def filtrar(self, acoes: Iterable[Acao]) -> list[Acao]:
        return [acao for acao in acoes if self.autorizada(acao)]
