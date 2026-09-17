"""Modelo mínimo de eventos para rastreabilidade entre agentes e sistemas."""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


def agora() -> str:
    return datetime.now(timezone.utc).isoformat()


def _id(prefixo: str) -> str:
    return f"{prefixo}-{uuid.uuid4().hex[:16]}"


def _idempotencia(evento: dict) -> str:
    base = {k: v for k, v in evento.items() if k not in {"event_id", "timestamp"}}
    bruto = json.dumps(base, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(bruto.encode("utf-8")).hexdigest()


@dataclass
class Evento:
    """Unidade rastreável de uma ação no Projeto."""

    origem: str
    tipo: str
    destino: str | None = None
    payload: dict = field(default_factory=dict)
    correlation_id: str | None = None
    causation_id: str | None = None
    event_id: str = field(default_factory=lambda: _id("PA-EVENTO"))
    timestamp: str = field(default_factory=agora)
    versao: int = 1
    status: str = "CRIADO"
    idempotency_key: str | None = None

    def __post_init__(self) -> None:
        if not self.origem or not self.tipo:
            raise ValueError("origem e tipo são obrigatórios")
        if self.versao < 1:
            raise ValueError("versao deve ser >= 1")
        if self.status not in {"CRIADO", "EM_PROCESSAMENTO", "CONCLUIDO", "FALHOU", "CANCELADO"}:
            raise ValueError("status de evento inválido")
        if self.idempotency_key is None:
            self.idempotency_key = self.calcular_idempotencia()

    def calcular_idempotencia(self) -> str:
        return _idempotencia(self.to_dict(include_idempotency=False))

    def to_dict(self, *, include_idempotency: bool = True) -> dict:
        data = {
            "event_id": self.event_id,
            "correlation_id": self.correlation_id,
            "causation_id": self.causation_id,
            "origem": self.origem,
            "destino": self.destino,
            "tipo": self.tipo,
            "timestamp": self.timestamp,
            "versao": self.versao,
            "status": self.status,
            "payload": self.payload,
        }
        if include_idempotency:
            data["idempotency_key"] = self.idempotency_key
        return data
