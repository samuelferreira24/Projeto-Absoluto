from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable

from .semantica import RelacaoSemantica, UnidadeSemantica


@dataclass(frozen=True)
class IntervaloTemporal:
    """Janela de validade de uma unidade ou relação.

    `valid_from` e `valid_until` representam quando o fato é válido no mundo
    observado. `recorded_at` representa quando o sistema registrou a evidência.
    Assim, tempo do acontecimento não é confundido com tempo da ingestão.
    """

    valid_from: str | None = None
    valid_until: str | None = None
    recorded_at: str | None = None

    def __post_init__(self) -> None:
        inicio = _parse(self.valid_from)
        fim = _parse(self.valid_until)
        _parse(self.recorded_at)
        if inicio and fim and fim < inicio:
            raise ValueError("valid_until não pode ser anterior a valid_from")


def _parse(value: str | None) -> datetime | None:
    if value is None:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"Timestamp ISO-8601 inválido: {value}") from exc


def intervalo_da_unidade(unidade: UnidadeSemantica) -> IntervaloTemporal:
    meta = unidade.metadata.get("temporal", {})
    if not isinstance(meta, dict):
        raise ValueError("metadata.temporal deve ser um objeto")
    return IntervaloTemporal(
        valid_from=meta.get("valid_from"),
        valid_until=meta.get("valid_until"),
        recorded_at=meta.get("recorded_at"),
    )


def intervalo_da_relacao(relacao: RelacaoSemantica) -> IntervaloTemporal:
    meta = relacao.provenance.get("temporal", {})
    if not isinstance(meta, dict):
        raise ValueError("provenance.temporal deve ser um objeto")
    return IntervaloTemporal(
        valid_from=meta.get("valid_from"),
        valid_until=meta.get("valid_until"),
        recorded_at=meta.get("recorded_at"),
    )


def valido_em(intervalo: IntervaloTemporal, instante: str) -> bool:
    ponto = _parse(instante)
    if ponto is None:
        raise ValueError("instante é obrigatório")
    if intervalo.valid_from and ponto < _parse(intervalo.valid_from):
        return False
    if intervalo.valid_until and ponto > _parse(intervalo.valid_until):
        return False
    return True


def unidades_validas_em(unidades: Iterable[UnidadeSemantica], instante: str) -> list[UnidadeSemantica]:
    return [u for u in unidades if valido_em(intervalo_da_unidade(u), instante)]


def relacoes_validas_em(relacoes: Iterable[RelacaoSemantica], instante: str) -> list[RelacaoSemantica]:
    return [r for r in relacoes if valido_em(intervalo_da_relacao(r), instante)]
