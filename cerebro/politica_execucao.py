from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from typing import Iterable, Sequence
import os
import shutil
import uuid
from datetime import datetime, timedelta, timezone


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
        comando = argv[0]
        executavel_resolvido = Path(comando).resolve() if Path(comando).is_absolute() else Path(shutil.which(comando) or "").resolve()
        if not str(executavel_resolvido) or not executavel_resolvido.exists():
            return False, f"executável não encontrado: {comando}"

        permitidos: set[Path] = set()
        for permitido in self.executaveis_permitidos:
            resolvido = Path(permitido).resolve() if Path(permitido).is_absolute() else Path(shutil.which(permitido) or "").resolve()
            if str(resolvido) and resolvido.exists():
                permitidos.add(resolvido)

        if executavel_resolvido not in permitidos:
            return False, f"executável não permitido pelo escopo: {comando}"
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
        self._aprovacoes: dict[str, dict[str, object]] = {}

    def emitir_aprovacao(self, acao: Acao, *, ferramenta: str | None = None, recurso: str | None = None,
                         custo_maximo: float = 0.0, cadeia_maxima: int = 1, validade_segundos: int = 300) -> str:
        if validade_segundos <= 0 or custo_maximo < 0 or cadeia_maxima < 1:
            raise ValueError("limites de aprovação inválidos")
        agora = datetime.now(timezone.utc)
        token = f"APV-{uuid.uuid4().hex}"
        self._aprovacoes[token] = {
            "acao": acao.nome, "nivel": int(acao.nivel), "ferramenta": ferramenta,
            "recurso": recurso, "custo_maximo": custo_maximo, "cadeia_maxima": cadeia_maxima,
            "expira_em": (agora + timedelta(seconds=validade_segundos)).isoformat(), "utilizada": False,
        }
        return token

    def autorizada(self, acao: Acao, *, ferramenta: str | None = None, recurso: str | None = None,
                   custo_estimado: float = 0.0, cadeia: int = 1, aprovacao_id: str | None = None) -> bool:
        if acao.nivel > self.nivel_maximo:
            return False
        if not acao.reversivel and acao.nivel >= NivelAutonomia.ALTO_IMPACTO:
            return False
        if acao.exige_autorizacao:
            aprovacao = self._aprovacoes.get(aprovacao_id or "")
            if not aprovacao or aprovacao["utilizada"]:
                return False
            if datetime.fromisoformat(str(aprovacao["expira_em"])) <= datetime.now(timezone.utc):
                return False
            if aprovacao["acao"] != acao.nome or int(aprovacao["nivel"]) != int(acao.nivel):
                return False
            if aprovacao["ferramenta"] != ferramenta or aprovacao["recurso"] != recurso:
                return False
            if custo_estimado > float(aprovacao["custo_maximo"]) or cadeia > int(aprovacao["cadeia_maxima"]):
                return False
        return True

    def consumir_aprovacao(self, aprovacao_id: str | None) -> None:
        if not aprovacao_id:
            return
        aprovacao = self._aprovacoes.get(aprovacao_id)
        if aprovacao is None:
            raise ValueError("aprovação inexistente")
        aprovacao["utilizada"] = True

    def validar_executor_externo(self, acao: Acao, argv: Sequence[str], *, aprovacao_id: str | None = None) -> tuple[bool, str]:
        if not self.autorizada(acao, aprovacao_id=aprovacao_id):
            return False, "ação fora da política de autonomia"
        if not self.escopo.autorizado:
            return False, "executor externo sem escopo técnico autorizado"
        return self.escopo.validar_comando(argv)

    def filtrar(self, acoes: Iterable[Acao]) -> list[Acao]:
        return [acao for acao in acoes if self.autorizada(acao)]
