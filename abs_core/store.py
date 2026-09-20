import json
import sqlite3
from pathlib import Path
from typing import Any
from .models import Work, WorkState

class WorkStore:
    def __init__(self, path: str | Path = ":memory:") -> None:
        self.conn = sqlite3.connect(str(path))
        self.conn.execute("CREATE TABLE IF NOT EXISTS works (id TEXT PRIMARY KEY, objective TEXT NOT NULL, context TEXT NOT NULL, state TEXT NOT NULL, capability_id TEXT, result TEXT)")
        self.conn.execute("CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY, work_id TEXT NOT NULL, type TEXT NOT NULL, timestamp TEXT NOT NULL, payload TEXT NOT NULL)")
        self.conn.execute("CREATE TABLE IF NOT EXISTS provenance (work_id TEXT NOT NULL, seq INTEGER NOT NULL, capability_id TEXT, capability_name TEXT, data TEXT NOT NULL, PRIMARY KEY(work_id, seq))")
        self.conn.execute("CREATE TABLE IF NOT EXISTS sessions (work_id TEXT NOT NULL, capability_id TEXT NOT NULL, data TEXT NOT NULL, PRIMARY KEY(work_id, capability_id))")
        self.conn.commit()

    def save(self, work: Work) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO works VALUES (?, ?, ?, ?, ?, ?)",
            (work.id, work.objective, json.dumps(work.context), work.state.value, work.capability_id, json.dumps(work.result)),
        )
        self.conn.execute("DELETE FROM events WHERE work_id=?", (work.id,))
        self.conn.execute("DELETE FROM provenance WHERE work_id=?", (work.id,))
        self.conn.execute("DELETE FROM sessions WHERE work_id=?", (work.id,))
        self.conn.executemany(
            "INSERT INTO events VALUES (?, ?, ?, ?, ?)",
            [(e.id, e.work_id, e.type, e.timestamp, json.dumps(e.payload)) for e in work.events],
        )
        self.conn.executemany(
            "INSERT INTO provenance VALUES (?, ?, ?, ?, ?)",
            [(work.id, i, p.get("capability_id"), p.get("capability_name"), json.dumps(p)) for i, p in enumerate(work.provenance)],
        )
        self.conn.executemany(
            "INSERT INTO sessions VALUES (?, ?, ?)",
            [(work.id, capability_id, json.dumps(data)) for capability_id, data in work.sessions.items()],
        )
        self.conn.commit()

    def load(self, work_id: str) -> Work:
        row = self.conn.execute(
            "SELECT id, objective, context, state, capability_id, result FROM works WHERE id=?",
            (work_id,),
        ).fetchone()
        if not row:
            raise KeyError(work_id)
        work = Work(
            row[1],
            json.loads(row[2]),
            id=row[0],
            state=WorkState(row[3]),
            capability_id=row[4],
            result=json.loads(row[5]) if row[5] else None,
        )
        for r in self.conn.execute("SELECT id, type, timestamp, payload FROM events WHERE work_id=? ORDER BY timestamp", (work_id,)):
            from .models import Event
            work.events.append(Event(r[1], work_id, json.loads(r[3]), r[2], r[0]))
        work.provenance = [
            json.loads(r[4])
            for r in self.conn.execute(
                "SELECT seq, work_id, capability_id, capability_name, data FROM provenance WHERE work_id=? ORDER BY seq",
                (work_id,),
            )
        ]
        work.sessions = {
            r[0]: json.loads(r[1])
            for r in self.conn.execute("SELECT capability_id, data FROM sessions WHERE work_id=?", (work_id,))
        }
        return work
