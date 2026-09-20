from dataclasses import dataclass, field
from typing import Any, Protocol

class Capability(Protocol):
    id: str
    name: str
    def execute(self, objective: str, context: dict[str, Any]) -> Any: ...

@dataclass
class CapabilityRecord:
    id: str
    name: str
    kind: str
    adapter: Capability
    metadata: dict[str, Any] = field(default_factory=dict)

class CapabilityRegistry:
    def __init__(self) -> None:
        self._items: dict[str, CapabilityRecord] = {}

    def register(self, record: CapabilityRecord) -> None:
        if record.id in self._items:
            raise ValueError(f"Capability already registered: {record.id}")
        self._items[record.id] = record

    def get(self, capability_id: str) -> CapabilityRecord:
        return self._items[capability_id]

    def list(self) -> list[CapabilityRecord]:
        return list(self._items.values())

    def choose(self, capability_id: str | None = None) -> CapabilityRecord:
        if capability_id:
            return self.get(capability_id)
        if not self._items:
            raise RuntimeError("No capability registered")
        return next(iter(self._items.values()))
