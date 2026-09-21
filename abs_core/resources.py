from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from threading import RLock
from typing import Any
from uuid import uuid4


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Device:
    id: str
    name: str
    kind: str = "unknown"
    status: str = "online"
    endpoint: str | None = None
    capabilities: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    last_seen: str = field(default_factory=_now)

    def public(self) -> dict[str, Any]:
        return asdict(self)


class ResourceManager:
    """Small V1 resource registry.

    It deliberately separates the concept of a device/resource from a
    capability implementation. Remote execution is not implied by registration.
    """

    def __init__(self, node_name: str = "ABS local") -> None:
        self._lock = RLock()
        self._devices: dict[str, Device] = {}
        self.local_id = f"local-{uuid4().hex[:8]}"
        self.register(
            name=node_name,
            kind="local",
            status="online",
            capabilities=[],
            device_id=self.local_id,
            metadata={"managed_by": "abs-core"},
        )

    def register(
        self,
        name: str,
        kind: str = "unknown",
        status: str = "online",
        endpoint: str | None = None,
        capabilities: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        device_id: str | None = None,
    ) -> Device:
        with self._lock:
            device = Device(
                id=device_id or f"dev-{uuid4().hex[:10]}",
                name=name.strip() or "Unnamed device",
                kind=kind,
                status=status,
                endpoint=endpoint,
                capabilities=sorted(set(capabilities or [])),
                metadata=metadata or {},
            )
            self._devices[device.id] = device
            return device

    def list(self) -> list[Device]:
        with self._lock:
            return [Device(**asdict(d)) for d in self._devices.values()]

    def get(self, device_id: str) -> Device:
        with self._lock:
            return Device(**asdict(self._devices[device_id]))

    def heartbeat(self, device_id: str, status: str = "online") -> Device:
        with self._lock:
            device = self._devices[device_id]
            device.status = status
            device.last_seen = _now()
            return Device(**asdict(device))

    def remove(self, device_id: str) -> None:
        with self._lock:
            if device_id == self.local_id:
                raise ValueError("local_device_cannot_be_removed")
            del self._devices[device_id]

    def summary(self) -> dict[str, int]:
        devices = self.list()
        return {
            "total": len(devices),
            "online": sum(d.status == "online" for d in devices),
            "offline": sum(d.status == "offline" for d in devices),
            "degraded": sum(d.status == "degraded" for d in devices),
        }
