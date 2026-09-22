from __future__ import annotations

import json
import sqlite3
import threading
from pathlib import Path

from .tool_knowledge import ToolKnowledge, ToolKnowledgeRegistry


class ToolKnowledgeStore:
    """SQLite persistence for tool knowledge.

    Knowledge survives process restart and remains separate from model memory.
    """

    def __init__(self, path: str | Path = "abs.db") -> None:
        self.path = Path(path).expanduser().resolve()
        self.conn = sqlite3.connect(str(self.path), check_same_thread=False)
        self._lock = threading.RLock()
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tool_knowledge (
                id TEXT PRIMARY KEY,
                data TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    def save(self, tool: ToolKnowledge) -> None:
        with self._lock:
            self.conn.execute(
                "INSERT OR REPLACE INTO tool_knowledge (id, data) VALUES (?, ?)",
                (tool.id, json.dumps(tool.public(), ensure_ascii=False)),
            )
            self.conn.commit()

    def load_into(self, registry: ToolKnowledgeRegistry) -> int:
        with self._lock:
            rows = self.conn.execute(
                "SELECT data FROM tool_knowledge ORDER BY id"
            ).fetchall()
        count = 0
        for (raw,) in rows:
            data = json.loads(raw)
            registry.upsert(ToolKnowledge(**data))
            count += 1
        return count

    def save_registry(self, registry: ToolKnowledgeRegistry) -> int:
        items = registry.list()
        for item in items:
            self.save(item)
        return len(items)
