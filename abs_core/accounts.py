from __future__ import annotations

from dataclasses import asdict, dataclass, field
from threading import RLock
from typing import Any


@dataclass
class AccountRecord:
    """A logical identity for a service connection.

    Secrets are never stored in this record. credential_ref points to an
    external secret/credential store and may be rotated independently.
    """

    id: str
    provider: str
    name: str
    connection_id: str
    status: str = "configured"
    credential_ref: str | None = None
    capabilities: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def public(self) -> dict[str, Any]:
        data = asdict(self)
        data["credential_ref"] = bool(self.credential_ref)
        return data


class AccountRegistry:
    """Extensible registry for multiple accounts per provider/service."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._items: dict[str, AccountRecord] = {}

    def register(self, account: AccountRecord) -> AccountRecord:
        with self._lock:
            if account.id in self._items:
                raise ValueError(f"Account already registered: {account.id}")
            self._items[account.id] = account
            return AccountRecord(**asdict(account))

    def get(self, account_id: str) -> AccountRecord:
        with self._lock:
            return AccountRecord(**asdict(self._items[account_id]))

    def list(self) -> list[AccountRecord]:
        with self._lock:
            return [AccountRecord(**asdict(item)) for item in self._items.values()]

    def public(self) -> list[dict[str, Any]]:
        return [item.public() for item in self.list()]

    def update_status(self, account_id: str, status: str) -> AccountRecord:
        with self._lock:
            item = self._items[account_id]
            item.status = status
            return AccountRecord(**asdict(item))

    def by_provider(self, provider: str) -> list[AccountRecord]:
        return [item for item in self.list() if item.provider == provider]
