from __future__ import annotations

import json
import sqlite3
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class ABSDataLayer:
    """Logical ABS data layer over the current SQLite implementation.

    The rest of ABS talks to this contract instead of depending on a future
    database vendor. SQLite is the V1 implementation; another backend can be
    introduced later without changing the logical memory contract.
    """

    def __init__(self, path: str | Path = "abs.db") -> None:
        self.path = str(path)
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.lock = threading.RLock()
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS abs_memory ("
            "id TEXT PRIMARY KEY, kind TEXT NOT NULL, key TEXT, content TEXT NOT NULL, "
            "metadata TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL)"
        )
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_abs_memory_kind_key ON abs_memory(kind, key)")
        self.conn.commit()

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def put(self, kind: str, content: Any, *, key: str | None = None, metadata: dict[str, Any] | None = None) -> str:
        now = self._now()
        item_id = str(uuid.uuid4())
        with self.lock:
            self.conn.execute(
                "INSERT INTO abs_memory VALUES (?, ?, ?, ?, ?, ?, ?)",
                (item_id, kind, key, json.dumps(content, ensure_ascii=False),
                 json.dumps(metadata or {}, ensure_ascii=False), now, now),
            )
            self.conn.commit()
        return item_id

    def search(self, kind: str | None = None, query: str | None = None, limit: int = 50) -> list[dict[str, Any]]:
        sql = "SELECT id, kind, key, content, metadata, created_at, updated_at FROM abs_memory"
        clauses: list[str] = []
        params: list[Any] = []
        if kind:
            clauses.append("kind=?")
            params.append(kind)
        if query:
            clauses.append("(content LIKE ? OR key LIKE ?)")
            token = f"%{query}%"
            params.extend([token, token])
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " ORDER BY updated_at DESC LIMIT ?"
        params.append(limit)
        with self.lock:
            rows = self.conn.execute(sql, params).fetchall()
        return [
            {"id": r[0], "kind": r[1], "key": r[2], "content": json.loads(r[3]),
             "metadata": json.loads(r[4]), "created_at": r[5], "updated_at": r[6]}
            for r in rows
        ]

    def record_work_result(self, work_id: str, objective: str, result: Any, state: str) -> str:
        return self.put("work_result", {"work_id": work_id, "objective": objective, "result": result, "state": state}, key=work_id)

    def record_conversation(self, session_id: str, messages: list[dict[str, Any]]) -> str:
        return self.put("conversation", messages, key=session_id)

    def close(self) -> None:
        with self.lock:
            self.conn.close()
