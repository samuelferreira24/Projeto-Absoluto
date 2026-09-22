from __future__ import annotations

from dataclasses import asdict, dataclass, field
from threading import RLock
from typing import Any
import json
import os
import sqlite3


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

    def __init__(self, path: str | None = None) -> None:
        self._lock = RLock()
        self._items: dict[str, AccountRecord] = {}
        self.path = path or os.getenv("ABS_DB_PATH", "abs.db")
        self._conn = sqlite3.connect(self.path, check_same_thread=False)
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS accounts "
            "(id TEXT PRIMARY KEY, provider TEXT NOT NULL, name TEXT NOT NULL, "
            "connection_id TEXT NOT NULL, status TEXT NOT NULL, credential_ref TEXT, "
            "capabilities TEXT NOT NULL, metadata TEXT NOT NULL)"
        )
        self._conn.commit()
        self._load()

    def _load(self) -> None:
        rows = self._conn.execute(
            "SELECT id, provider, name, connection_id, status, credential_ref, capabilities, metadata FROM accounts"
        ).fetchall()
        for row in rows:
            self._items[row[0]] = AccountRecord(
                id=row[0], provider=row[1], name=row[2], connection_id=row[3],
                status=row[4], credential_ref=row[5],
                capabilities=json.loads(row[6]), metadata=json.loads(row[7]),
            )

    def _persist(self, account: AccountRecord) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (account.id, account.provider, account.name, account.connection_id,
             account.status, account.credential_ref, json.dumps(account.capabilities),
             json.dumps(account.metadata)),
        )
        self._conn.commit()

    def register(self, account: AccountRecord) -> AccountRecord:
        with self._lock:
            if account.id in self._items:
                raise ValueError(f"Account already registered: {account.id}")
            self._items[account.id] = account
            self._persist(account)
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
            self._persist(item)
            return AccountRecord(**asdict(item))

    def by_provider(self, provider: str) -> list[AccountRecord]:
        return [item for item in self.list() if item.provider == provider]
