from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .capabilities import CapabilityRegistry
from .connections import ConnectionRegistry
from .orchestrator import Orchestrator
from .store import WorkStore


@dataclass(frozen=True)
class IntelligenceResource:
    """A replaceable source of cognitive capability.

    A resource may be remote, local, a CLI/runtime, another ABS intelligence,
    or any future adapter. The ABS does not depend on one provider.
    """
    id: str
    capability_id: str
    name: str
    source: str
    local: bool
    capabilities: tuple[str, ...] = ()
    status: str = "available"
    priority: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def public(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "capability_id": self.capability_id,
            "name": self.name,
            "source": self.source,
            "local": self.local,
            "capabilities": list(self.capabilities),
            "status": self.status,
            "priority": self.priority,
            "metadata": dict(self.metadata),
        }


class IntelligenceRegistry:
    """Dynamic registry of replaceable intelligence resources."""

    def __init__(self) -> None:
        self._items: dict[str, IntelligenceResource] = {}

    def register(self, resource: IntelligenceResource) -> None:
        self._items[resource.id] = resource

    def list(self) -> list[IntelligenceResource]:
        return list(self._items.values())

    def get(self, resource_id: str) -> IntelligenceResource:
        return self._items[resource_id]

    def discover_from_capabilities(
        self,
        capabilities: CapabilityRegistry,
        connections: ConnectionRegistry | None = None,
    ) -> list[IntelligenceResource]:
        connection_map = {item.id: item for item in (connections.list() if connections else [])}
        found: list[IntelligenceResource] = []
        for cap in capabilities.list():
            if cap.kind not in {"external_ai", "ai", "local_ai"} and cap.id not in {
                "codex", "openai-api", "claude", "gemini", "local-ai"
            }:
                continue
            connection = None
            for item in connection_map.values():
                if item.metadata.get("adapter") == cap.id or item.id == cap.id:
                    connection = item
                    break
            local = cap.id in {"codex", "local-ai"} or (connection is not None and connection.transport in {"local-http", "cli-termux"})
            status = connection.status if connection else "available"
            capabilities_hint = tuple(connection.capabilities) if connection else ()
            resource = IntelligenceResource(
                id=f"intelligence:{cap.id}",
                capability_id=cap.id,
                name=cap.name,
                source="local" if local else "remote",
                local=local,
                capabilities=capabilities_hint,
                status=status,
                priority=10.0 if local else 5.0,
                metadata={"connection_id": connection.id if connection else None, "conversational": cap.id not in {"codex"}},
            )
            self.register(resource)
            found.append(resource)
        return found


class CognitiveRuntime:
    """Open-ended conversational runtime over replaceable intelligence resources.

    It deliberately does not translate messages into a fixed command grammar.
    A turn can remain a conversation, request information, use an execution
    capability, or evolve into a larger objective. The selected intelligence
    receives the conversation context and decides the next response.
    """

    def __init__(
        self,
        capabilities: CapabilityRegistry,
        intelligence: IntelligenceRegistry,
        orchestrator: Orchestrator | None = None,
        *,
        store_path: str = "abs.db",
        max_history: int = 24,
    ) -> None:
        import sqlite3
        import json
        import threading

        self.capabilities = capabilities
        self.intelligence = intelligence
        self.orchestrator = orchestrator
        self.max_history = max_history
        self.store_path = store_path
        self._lock = threading.RLock()
        self._json = json
        self._conn = sqlite3.connect(store_path, check_same_thread=False)
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS cognitive_sessions ("
            "id TEXT PRIMARY KEY, created_at TEXT NOT NULL, updated_at TEXT NOT NULL, "
            "preferred_resource TEXT, context TEXT NOT NULL, messages TEXT NOT NULL)"
        )
        self._conn.commit()

    def _new_id(self) -> str:
        import uuid
        return str(uuid.uuid4())

    def create_session(self, context: dict[str, Any] | None = None, preferred_resource: str | None = None) -> str:
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()
        session_id = self._new_id()
        with self._lock:
            self._conn.execute(
                "INSERT INTO cognitive_sessions VALUES (?, ?, ?, ?, ?, ?)",
                (session_id, now, now, preferred_resource, self._json.dumps(context or {}, ensure_ascii=False), "[]"),
            )
            self._conn.commit()
        return session_id

    def _load(self, session_id: str) -> dict[str, Any]:
        row = self._conn.execute(
            "SELECT id, created_at, updated_at, preferred_resource, context, messages "
            "FROM cognitive_sessions WHERE id=?", (session_id,)
        ).fetchone()
        if not row:
            raise KeyError(session_id)
        return {
            "id": row[0],
            "created_at": row[1],
            "updated_at": row[2],
            "preferred_resource": row[3],
            "context": self._json.loads(row[4]),
            "messages": self._json.loads(row[5]),
        }

    def _save(self, session: dict[str, Any]) -> None:
        from datetime import datetime, timezone
        session["updated_at"] = datetime.now(timezone.utc).isoformat()
        session["messages"] = session["messages"][-self.max_history:]
        self._conn.execute(
            "UPDATE cognitive_sessions SET updated_at=?, preferred_resource=?, context=?, messages=? WHERE id=?",
            (
                session["updated_at"],
                session.get("preferred_resource"),
                self._json.dumps(session.get("context", {}), ensure_ascii=False),
                self._json.dumps(session["messages"], ensure_ascii=False),
                session["id"],
            ),
        )
        self._conn.commit()

    def list_sessions(self) -> list[dict[str, Any]]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT id, created_at, updated_at, preferred_resource FROM cognitive_sessions ORDER BY updated_at DESC"
            ).fetchall()
        return [
            {"id": r[0], "created_at": r[1], "updated_at": r[2], "preferred_resource": r[3]}
            for r in rows
        ]

    def _choose(self, session: dict[str, Any], preferred_resource: str | None = None) -> IntelligenceResource:
        preferred = preferred_resource or session.get("preferred_resource")
        resources = [r for r in self.intelligence.list() if r.status not in {"offline", "planned"}]
        if preferred:
            try:
                chosen = self.intelligence.get(preferred)
                if chosen.status not in {"offline", "planned"}:
                    return chosen
            except KeyError:
                pass
        if not resources:
            raise RuntimeError("no_intelligence_resource_available")

        def score(resource: IntelligenceResource) -> tuple[float, str]:
            # Keep selection deterministic but not tied to a provider.
            availability = {"configured": 30.0, "available": 20.0, "degraded": 5.0}.get(resource.status, 0.0)
            return (availability + resource.priority, resource.id)

        return sorted(resources, key=lambda item: (-score(item)[0], score(item)[1]))[0]

    def turn(
        self,
        message: str,
        *,
        session_id: str | None = None,
        preferred_resource: str | None = None,
        context: dict[str, Any] | None = None,
        approved: bool = False,
    ) -> dict[str, Any]:
        message = str(message or "").strip()
        if not message:
            raise ValueError("message_required")
        with self._lock:
            sid = session_id or self.create_session(context=context, preferred_resource=preferred_resource)
            session = self._load(sid)
            if context:
                session["context"].update(context)
            resource = self._choose(session, preferred_resource)
            cap = self.capabilities.get(resource.capability_id)
            # The normal ABS authorization boundary remains authoritative.
            if cap.kind != "test" and not approved and not resource.metadata.get("conversational", False):
                raise PermissionError(f"Imperator approval required for intelligence: {cap.id}")

            session["messages"].append({"role": "user", "content": message})
            execution_context = {
                **session["context"],
                "conversation": {
                    "session_id": sid,
                    "messages": list(session["messages"]),
                },
            }
            if self.orchestrator is None:
                self.orchestrator = Orchestrator(self.capabilities, WorkStore(self.store_path))
            work = self.orchestrator.create(message, execution_context)
            work = self.orchestrator.run(work.id, resource.capability_id, approved=(approved or resource.metadata.get("conversational", False)))
            result = work.result
            final_response = result.get("final_response") if isinstance(result, dict) else result
            if work.state.value == "failed":
                final_response = result.get("error", "intelligence_execution_failed") if isinstance(result, dict) else str(result)
            session["messages"].append({"role": "assistant", "content": final_response})
            session["preferred_resource"] = preferred_resource or session.get("preferred_resource")
            self._save(session)
            return {
                "session_id": sid,
                "work_id": work.id,
                "work_state": work.state.value,
                "provenance": work.provenance,
                "resource": resource.public(),
                "response": final_response,
                "result": result,
                "message_count": len(session["messages"]),
            }
