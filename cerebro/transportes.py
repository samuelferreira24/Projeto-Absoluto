from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Transporte:
    """Meio de comunicação disponível entre nós.

    O Cérebro não assume Internet como transporte padrão. Um nó pode
    anunciar vários meios simultaneamente e o executor decide qual usar.
    """

    id: str
    tipo: str
    alcance: str
    conectado: bool = True
    custo: float = 0.0
    energia: float = 0.0
    largura_banda: float | None = None
    latencia: float | None = None
    internet_necessaria: bool = False
    bidirecional: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id or not self.tipo or not self.alcance:
            raise ValueError("id, tipo e alcance são obrigatórios")
        if self.custo < 0 or self.energia < 0:
            raise ValueError("custo e energia não podem ser negativos")


def transportes_viaveis(
    transportes: list[Transporte],
    *,
    exigir_internet: bool = False,
    exigir_bidirecional: bool = False,
) -> list[Transporte]:
    """Filtra os meios compatíveis com a necessidade atual."""
    return [
        t for t in transportes
        if t.conectado
        and (not exigir_internet or t.internet_necessaria)
        and (not exigir_bidirecional or t.bidirecional)
    ]


def selecionar_transporte(
    transportes: list[Transporte],
    *,
    exigir_internet: bool = False,
    exigir_bidirecional: bool = False,
) -> Transporte | None:
    """Escolhe um meio viável priorizando baixo custo/energia e baixa latência.

    Isto é uma heurística inicial, não uma regra fixa da arquitetura.
    """
    candidatos = transportes_viaveis(
        transportes,
        exigir_internet=exigir_internet,
        exigir_bidirecional=exigir_bidirecional,
    )
    if not candidatos:
        return None

    def chave(t: Transporte) -> tuple[float, float, float]:
        latencia = t.latencia if t.latencia is not None else 999999.0
        return (t.custo + t.energia, latencia, -(t.largura_banda or 0.0))

    return min(candidatos, key=chave)
