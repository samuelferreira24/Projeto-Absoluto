from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .capabilities import CapabilityRegistry
from .connections import ConnectionRegistry
from .orchestrator import Orchestrator
from .store import WorkStore
from .data_layer import ABSDataLayer
from .conversational_tools import ConversationalToolRuntime


@dataclass(frozen=True)
class IntelligenceResource:
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
            "id": self.id, "capability_id": self.capability_id, "name": self.name,
            "source": self.source, "local": self.local, "capabilities": list(self.capabilities),
            "status": self.status, "priority": self.priority, "metadata": dict(self.metadata),
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

    def discover_from_capabilities(self, capabilities: CapabilityRegistry, connections: ConnectionRegistry | None = None) -> list[IntelligenceResource]:
        connection_map = {item.id: item for item in (connections.list() if connections else [])}
        found: list[IntelligenceResource] = []
        for cap in capabilities.list():
            if cap.kind not in {"external_ai", "ai", "local_ai"} and cap.id not in {"codex", "openai-api", "claude", "gemini", "local-ai"} and not cap.id.startswith("local-ai:"):
                continue
            connection = next((item for item in connection_map.values() if item.metadata.get("adapter") == cap.id or item.id == cap.id), None)
            local = cap.kind == "local_ai" or (connection is not None and connection.transport in {"local-http", "cli-termux"})
            # Registration is not proof that an adapter is reachable. Without a
            # matching connection health signal, expose local resources as configured
            # and remote resources as unverified rather than falsely available.
            status = connection.status if connection else ("configured" if local else "unverified")
            capabilities_hint = tuple(connection.capabilities) if connection else tuple(cap.metadata.get("capabilities") or ())
            metadata = {"connection_id": connection.id if connection else None, "conversational": cap.id not in {"codex"}}
            metadata.update(cap.metadata)
            resource = IntelligenceResource(
                id=f"intelligence:{cap.id}", capability_id=cap.id, name=cap.name,
                source="local" if local else "remote", local=local,
                capabilities=capabilities_hint, status=status,
                priority=float(metadata.get("priority", 10.0 if local else 5.0)), metadata=metadata,
            )
            self.register(resource)
            found.append(resource)
        return found


class CognitiveRuntime:
    """Conversational runtime over replaceable intelligence resources."""
    def __init__(self, capabilities: CapabilityRegistry, intelligence: IntelligenceRegistry,
                 orchestrator: Orchestrator | None = None, *, store_path: str = "abs.db",
                 max_history: int = 24, data_layer: ABSDataLayer | None = None) -> None:
        import sqlite3, json, threading
        self.capabilities = capabilities
        self.intelligence = intelligence
        self.orchestrator = orchestrator
        self.max_history = max_history
        self.store_path = store_path
        self.data_layer = data_layer
        self.tool_runtime: ConversationalToolRuntime | None = None
        self._lock = threading.RLock()
        self._json = json
        self._conn = sqlite3.connect(store_path, check_same_thread=False)
        self._conn.execute("CREATE TABLE IF NOT EXISTS cognitive_sessions (id TEXT PRIMARY KEY, created_at TEXT NOT NULL, updated_at TEXT NOT NULL, preferred_resource TEXT, context TEXT NOT NULL, messages TEXT NOT NULL)")
        self._conn.commit()

    def _new_id(self) -> str:
        import uuid
        return str(uuid.uuid4())

    def create_session(self, context: dict[str, Any] | None = None, preferred_resource: str | None = None) -> str:
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()
        session_id = self._new_id()
        with self._lock:
            self._conn.execute("INSERT INTO cognitive_sessions VALUES (?, ?, ?, ?, ?, ?)", (session_id, now, now, preferred_resource, self._json.dumps(context or {}, ensure_ascii=False), "[]"))
            self._conn.commit()
        return session_id

    def _load(self, session_id: str) -> dict[str, Any]:
        row = self._conn.execute("SELECT id, created_at, updated_at, preferred_resource, context, messages FROM cognitive_sessions WHERE id=?", (session_id,)).fetchone()
        if not row:
            raise KeyError(session_id)
        return {"id": row[0], "created_at": row[1], "updated_at": row[2], "preferred_resource": row[3], "context": self._json.loads(row[4]), "messages": self._json.loads(row[5])}

    def _save(self, session: dict[str, Any]) -> None:
        from datetime import datetime, timezone
        session["updated_at"] = datetime.now(timezone.utc).isoformat()
        session["messages"] = session["messages"][-self.max_history:]
        self._conn.execute("UPDATE cognitive_sessions SET updated_at=?, preferred_resource=?, context=?, messages=? WHERE id=?", (session["updated_at"], session.get("preferred_resource"), self._json.dumps(session.get("context", {}), ensure_ascii=False), self._json.dumps(session["messages"], ensure_ascii=False), session["id"]))
        self._conn.commit()

    def list_sessions(self) -> list[dict[str, Any]]:
        with self._lock:
            rows = self._conn.execute("SELECT id, created_at, updated_at, preferred_resource FROM cognitive_sessions ORDER BY updated_at DESC").fetchall()
        return [{"id": r[0], "created_at": r[1], "updated_at": r[2], "preferred_resource": r[3]} for r in rows]

    def _rank_resources(self, session: dict[str, Any], preferred_resource: str | None = None) -> list[IntelligenceResource]:
        preferred = preferred_resource or session.get("preferred_resource")
        requested_capability = session.get("context", {}).get("capability_id")
        if not preferred and requested_capability:
            preferred = str(requested_capability)
            if not preferred.startswith("intelligence:"):
                preferred = f"intelligence:{preferred}"
        resources = [r for r in self.intelligence.list() if r.status not in {"offline", "planned"}]
        if session.get("context", {}).get("offline") is True:
            resources = [r for r in resources if r.local]
        required = tuple(session.get("context", {}).get("required_capabilities") or ())

        def available_memory_mb() -> float:
            try:
                with open("/proc/meminfo", "r", encoding="utf-8") as handle:
                    values = {line.split(":", 1)[0]: float(line.split()[1]) for line in handle if ":" in line}
                return values.get("MemAvailable", 0.0) / 1024.0
            except (OSError, ValueError, IndexError):
                return 0.0

        memory_mb = available_memory_mb()
        # Hard preflight, not merely a ranking penalty. Keep 768 MiB available for
        # the ABS service, Ollama overhead, and transient allocations. An explicit
        # preference must never override this safety gate.
        import os
        safety_reserve_mb = float(os.getenv("ABS_LOCAL_AI_MEMORY_RESERVE_MB", "768"))
        if memory_mb > 0:
            resources = [
                resource for resource in resources
                if not resource.local
                or not float(resource.metadata.get("estimated_memory_mb", 0.0) or 0.0)
                or float(resource.metadata.get("estimated_memory_mb", 0.0) or 0.0) <= max(0.0, memory_mb - safety_reserve_mb)
            ]

        def score(resource: IntelligenceResource) -> tuple[float, str]:
            availability = {"configured": 30.0, "available": 20.0, "degraded": 5.0}.get(resource.status, 0.0)
            capability_match = sum(1.0 for item in required if item in resource.capabilities)
            locality = 20.0 if session.get("context", {}).get("offline") is True and resource.local else 0.0
            preferred_bonus = 1000.0 if preferred == resource.id else 0.0
            memory_need = float(resource.metadata.get("estimated_memory_mb", 0.0) or 0.0)
            memory_penalty = 0.0
            if resource.local and memory_need and memory_mb:
                deficit = max(0.0, memory_need - memory_mb)
                memory_penalty = min(120.0, deficit / 40.0)
            return (preferred_bonus + capability_match * 100.0 + locality + availability + resource.priority - memory_penalty, resource.id)

        return sorted(resources, key=lambda item: (-score(item)[0], score(item)[1]))

    def _choose(self, session: dict[str, Any], preferred_resource: str | None = None) -> IntelligenceResource:
        resources = self._rank_resources(session, preferred_resource)
        if not resources:
            raise RuntimeError("no_intelligence_resource_available")
        return resources[0]

    @staticmethod
    def _extract_final_response(result: Any) -> Any:
        if isinstance(result, dict):
            direct = result.get("final_response")
            if direct is not None:
                return direct
            nested = result.get("result")
            if isinstance(nested, dict):
                inner = nested.get("final_response")
                if inner is not None:
                    return inner
            if nested is not None and not isinstance(nested, dict):
                return nested
        return result

    def turn(self, message: str, *, session_id: str | None = None, preferred_resource: str | None = None,
             context: dict[str, Any] | None = None, approved: bool = False) -> dict[str, Any]:
        message = str(message or "").strip()
        if not message:
            raise ValueError("message_required")
        with self._lock:
            sid = session_id or self.create_session(context=context, preferred_resource=preferred_resource)
            session = self._load(sid)

            incoming_messages = list((context or {}).get("conversation", {}).get("messages") or [])
            if not session["messages"] and incoming_messages:
                session["messages"] = [
                    item for item in incoming_messages
                    if isinstance(item, dict) and item.get("role") in {"system", "user", "assistant"}
                ][-self.max_history:]

            if context:
                session["context"].update({
                    k: v for k, v in context.items()
                    if v is not None and k != "conversation"
                })

            resource = self._choose(session, preferred_resource)
            cap = self.capabilities.get(resource.capability_id)
            if cap.kind != "test" and not approved and not resource.metadata.get("conversational", False):
                raise PermissionError(f"Imperator approval required for intelligence: {cap.id}")

            if not session["messages"] or not (
                isinstance(session["messages"][-1], dict)
                and session["messages"][-1].get("role") == "user"
                and session["messages"][-1].get("content") == message
            ):
                session["messages"].append({"role": "user", "content": message})

            session["context"]["external_results"] = []
            external_result = self.tool_runtime.execute(message) if self.tool_runtime is not None else None
            if external_result is not None:
                session["context"]["external_results"] = [external_result]

            session["context"]["_capabilities"] = [
                {"id": item.id, "name": item.name, "kind": item.kind}
                for item in self.capabilities.list()
            ]
            execution_context = {
                **session["context"],
                "conversation": {"session_id": sid, "messages": list(session["messages"])},
            }
            if self.orchestrator is None:
                self.orchestrator = Orchestrator(self.capabilities, WorkStore(self.store_path), data_layer=self.data_layer)
            ranked_resources = self._rank_resources(session, preferred_resource)
            if not ranked_resources:
                raise RuntimeError("no_intelligence_resource_available")

            work = None
            result = None
            fallback_attempts: list[dict[str, Any]] = []
            for candidate in ranked_resources:
                candidate_cap = self.capabilities.get(candidate.capability_id)
                if (
                    candidate_cap.kind != "test"
                    and not approved
                    and not candidate.metadata.get("conversational", False)
                ):
                    if candidate is ranked_resources[0]:
                        raise PermissionError(
                            f"Imperator approval required for intelligence: {candidate_cap.id}"
                        )
                    continue
                candidate_work = self.orchestrator.create(
                    message,
                    {**execution_context, "ai_resource": candidate.public()},
                )
                candidate_work = self.orchestrator.run(
                    candidate_work.id,
                    candidate.capability_id,
                    approved=(approved or candidate.metadata.get("conversational", False)),
                )
                candidate_result = candidate_work.result
                fallback_attempts.append({
                    "resource": candidate.public(),
                    "work_id": candidate_work.id,
                    "state": candidate_work.state.value,
                })
                work = candidate_work
                result = candidate_result
                if candidate_work.state.value != "failed":
                    resource = candidate
                    break
            if work is None or result is None:
                raise RuntimeError("no_approved_intelligence_resource_available")
            if work.state.value == "failed":
                final_response = result.get("error", "intelligence_execution_failed") if isinstance(result, dict) else str(result)
            else:
                final_response = self._extract_final_response(result)
            actual_capability = getattr(work, "capability_id", None)
            if actual_capability and resource.capability_id != actual_capability:
                try:
                    resource = self.intelligence.get(f"intelligence:{actual_capability}")
                except KeyError:
                    pass
            session["messages"].append({"role": "assistant", "content": final_response})
            session["preferred_resource"] = preferred_resource or session.get("preferred_resource")
            self._save(session)
            if self.data_layer is not None:
                self.data_layer.record_conversation(sid, session["messages"])
            return {"session_id": sid, "work_id": work.id, "work_state": work.state.value,
                    "provenance": work.provenance, "resource": resource.public(),
                    "response": final_response, "result": result,
                    "fallback_attempts": fallback_attempts,
                    "message_count": len(session["messages"])}
