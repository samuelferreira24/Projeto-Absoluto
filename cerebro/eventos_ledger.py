"""Ledger append-only de eventos para continuidade e rastreabilidade operacional."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable
import json

from .eventos import Evento


class LedgerEventos:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, evento: Evento) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(evento.__dict__, ensure_ascii=False, sort_keys=True) + "\n")

    def iterar(self) -> Iterable[dict]:
        if not self.path.exists():
            return iter(())
        def _gen():
            with self.path.open(encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        yield json.loads(line)
        return _gen()

    def por_correlacao(self, correlation_id: str) -> list[dict]:
        return [x for x in self.iterar() if x.get("correlation_id") == correlation_id]

    def por_causacao(self, causation_id: str) -> list[dict]:
        return [x for x in self.iterar() if x.get("causation_id") == causation_id]

    def ids(self) -> set[str]:
        return {x["event_id"] for x in self.iterar()}

    def validar_integridade(self) -> list[str]:
        erros: list[str] = []
        vistos: set[str] = set()
        for i, item in enumerate(self.iterar(), 1):
            event_id = item.get("event_id")
            if not event_id:
                erros.append(f"linha {i}: event_id ausente")
            elif event_id in vistos:
                erros.append(f"linha {i}: event_id duplicado: {event_id}")
            else:
                vistos.add(event_id)
            if not item.get("correlation_id"):
                erros.append(f"linha {i}: correlation_id ausente")
        return erros
