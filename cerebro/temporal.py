from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


def _iso(value: str | None) -> datetime | None:
    if value is None:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"Data ISO-8601 inválida: {value}") from exc


@dataclass(frozen=True)
class IntervaloTemporal:
    """Separa tempo de validade do tempo em que a evidência foi registrada."""

    valid_from: str | None = None
    valid_until: str | None = None
    recorded_at: str | None = None

    def __post_init__(self) -> None:
        inicio = _iso(self.valid_from)
        fim = _iso(self.valid_until)
        _iso(self.recorded_at)
        if inicio is not None and fim is not None and fim < inicio:
            raise ValueError("valid_until não pode ser anterior a valid_from")

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid_from": self.valid_from,
            "valid_until": self.valid_until,
            "recorded_at": self.recorded_at,
        }

    def valido_em(self, instante: str) -> bool:
        ponto = _iso(instante)
        assert ponto is not None
        inicio = _iso(self.valid_from)
        fim = _iso(self.valid_until)
        return (inicio is None or ponto >= inicio) and (fim is None or ponto <= fim)


def intervalo_da_unidade(unidade: Any) -> IntervaloTemporal:
    metadata = getattr(unidade, "metadata", {}) or {}
    temporal = metadata.get("temporal", metadata)
    return IntervaloTemporal(
        valid_from=temporal.get("valid_from"),
        valid_until=temporal.get("valid_until"),
        recorded_at=temporal.get("recorded_at"),
    )


def intervalo_da_relacao(relacao: Any) -> IntervaloTemporal:
    provenance = getattr(relacao, "provenance", {}) or {}
    temporal = provenance.get("temporal", {})
    return IntervaloTemporal(
        valid_from=temporal.get("valid_from"),
        valid_until=temporal.get("valid_until"),
        recorded_at=temporal.get("recorded_at"),
    )


def valido_em(objeto: Any, instante: str) -> bool:
    if hasattr(objeto, "metadata"):
        return intervalo_da_unidade(objeto).valido_em(instante)
    return intervalo_da_relacao(objeto).valido_em(instante)


def unidades_validas_em(unidades: list[Any], instante: str) -> list[Any]:
    return [u for u in unidades if intervalo_da_unidade(u).valido_em(instante)]


def relacoes_validas_em(relacoes: list[Any], instante: str) -> list[Any]:
    return [r for r in relacoes if intervalo_da_relacao(r).valido_em(instante)]
