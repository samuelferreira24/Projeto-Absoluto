from typing import Any
from .capabilities import CapabilityRegistry
from .models import Work, WorkState
from .store import WorkStore

class Orchestrator:
    def __init__(self, registry: CapabilityRegistry, store: WorkStore) -> None:
        self.registry = registry
        self.store = store

    def create(self, objective: str, context: dict[str, Any] | None = None) -> Work:
        work = Work(objective, context or {})
        work.emit("work.created", objective=objective)
        self.store.save(work)
        return work

    def run(self, work_id: str, capability_id: str | None = None, approved: bool = False) -> Work:
        work = self.store.load(work_id)
        cap = self.registry.choose(capability_id or work.capability_id)
        if cap.kind != "test" and not approved:
            work.emit("work.denied", capability_id=cap.id, reason="imperator_approval_required")
            self.store.save(work)
            raise PermissionError(f"Imperator approval required for capability: {cap.id}")

        work.capability_id = cap.id
        work.state = WorkState.RUNNING
        work.emit("work.started", capability_id=cap.id)
        self.store.save(work)
        try:
            execution_context = dict(work.context)
            session = work.sessions.get(cap.id)
            if session and session.get("thread_id"):
                execution_context["_codex_thread_id"] = session["thread_id"]
            result = cap.adapter.execute(work.objective, execution_context)
            work.result = result
            work.state = WorkState.COMPLETED
            if isinstance(result, dict) and result.get("thread_id"):
                work.sessions[cap.id] = {"thread_id": result["thread_id"]}
            work.provenance.append({
                "capability_id": cap.id,
                "capability_name": cap.name,
                "session": work.sessions.get(cap.id),
            })
            work.emit("work.completed", capability_id=cap.id)
        except Exception as exc:
            work.state = WorkState.FAILED
            work.emit("work.failed", capability_id=cap.id, error=repr(exc))
        self.store.save(work)
        return work

    def pause(self, work_id: str) -> Work:
        work = self.store.load(work_id)
        work.state = WorkState.PAUSED
        work.emit("work.paused")
        self.store.save(work)
        return work

    def resume(self, work_id: str, capability_id: str | None = None, approved: bool = False) -> Work:
        return self.run(work_id, capability_id, approved)
