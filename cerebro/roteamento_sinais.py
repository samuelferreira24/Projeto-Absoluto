from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .sinais import Sinal


@dataclass(frozen=True)
class Canal:
    """Contrato de transporte/acesso entre uma porta e o Cérebro.

    Canal não define a origem do dado. A mesma origem pode usar internet,
    rede local, processo, arquivo, interface ou outro meio.
    """

    id: str
    nome: str
    meio: str
    entrada: bool = True
    saida: bool = True
    bidirecional: bool = False
    seguro: bool | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class RoteadorSinais:
    """Roteia sinais por capacidade sem acoplar o Cérebro ao transporte."""

    def __init__(self) -> None:
        self.canais: dict[str, Canal] = {}
        self.historico: list[dict[str, Any]] = []

    def registrar_canal(self, canal: Canal) -> None:
        self.canais[canal.id] = canal

    def canais_entrada(self) -> list[Canal]:
        return [c for c in self.canais.values() if c.entrada]

    def canais_saida(self) -> list[Canal]:
        return [c for c in self.canais.values() if c.saida]

    def rotear(self, sinal: Sinal, canal_id: str | None = None) -> dict[str, Any]:
        canal = self.canais.get(canal_id) if canal_id else None
        if canal is not None and not canal.entrada:
            raise ValueError(f"canal não aceita entrada: {canal_id}")
        evento = {
            "sinal_id": sinal.id,
            "tipo": sinal.tipo,
            "origem": sinal.origem,
            "canal": canal.id if canal else sinal.canal,
            "destino": sinal.destino,
        }
        self.historico.append(evento)
        return evento
