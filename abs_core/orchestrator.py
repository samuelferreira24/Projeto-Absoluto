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

    def run(self, work_id: str, capability_id: str | None = None) -> Work:
        work = self.store.load(work_id)
        cap = self.registry.choose(capability_id or work.capability_id)
        work.capability_id = cap.id
        work.state = WorkState.RUNNING
        work.emit("work.started", capability_id=cap.id)
        self.store.save(work)
        try:
            result = cap.adapter.execute(work.objective, work.context)
            work.result = result
            work.state = WorkState.COMPLETED
            work.provenance.append({"capability_id": cap.id, "capability_name": cap.name})
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

    def resume(self, work_id: str, capability_id: str | None = None) -> Work:
        return self.run(work_id, capability_id)
