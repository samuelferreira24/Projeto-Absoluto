from typing import Any
from datetime import datetime, timezone
import uuid

from .capabilities import CapabilityRegistry
from .models import Work, WorkState
from .store import WorkStore


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Orchestrator:
    def __init__(
        self,
        registry: CapabilityRegistry,
        store: WorkStore,
        continuity=None,
        knowledge_runtime=None,
    ) -> None:
        self.registry = registry
        self.store = store
        self.continuity = continuity
        self.knowledge_runtime = knowledge_runtime

    def create(self, objective: str, context: dict[str, Any] | None = None) -> Work:
        work = Work(objective, context or {})
        work.emit("work.created", objective=objective)
        self.store.save(work)
        return work

    def _checkpoint(self) -> None:
        if self.continuity is not None:
            self.continuity.checkpoint()

    def _record_execution(self, work: Work, capability_id: str, status: str, detail: str) -> None:
        recorder = self.knowledge_runtime
        if recorder is None or not hasattr(recorder, "record_execution"):
            return
        recorder.record_execution(
            path_id=f"PATH-ABS-{capability_id.upper()}",
            operation=f"work:{work.id}",
            status=status,
            detail=detail,
            source=f"ABS Orchestrator ({capability_id})",
        )

    def run(self, work_id: str, capability_id: str | None = None, approved: bool = False) -> Work:
        work = self.store.load(work_id)
        cap = self.registry.choose(capability_id or work.capability_id)
        if cap.kind != "test" and not approved:
            work.emit("work.denied", capability_id=cap.id, reason="imperator_approval_required")
            self.store.save(work)
            self._checkpoint()
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
                "provenance_id": str(uuid.uuid4()),
                "work_id": work.id,
                "objective": work.objective,
                "capability_id": cap.id,
                "capability_name": cap.name,
                "session": work.sessions.get(cap.id),
                "recorded_at": _now(),
                "state": work.state.value,
                "result_type": result.get("type") if isinstance(result, dict) else type(result).__name__,
                "context_keys": sorted(work.context.keys()),
                "mission_id": work.context.get("cerebro_missao_id"),
                "cycle_id": (work.context.get("_execucao") or {}).get("ciclo_id"),
                "idempotency_key": (work.context.get("_execucao") or {}).get("idempotency_key"),
            })
            work.emit("work.completed", capability_id=cap.id)
            self._record_execution(work, cap.id, "operational", "Capability execution completed successfully.")
        except Exception as exc:
            work.state = WorkState.FAILED
            work.result = {"type": "error", "error": str(exc), "error_type": type(exc).__name__}
            work.provenance.append({
                "provenance_id": str(uuid.uuid4()),
                "work_id": work.id,
                "objective": work.objective,
                "capability_id": cap.id,
                "capability_name": cap.name,
                "recorded_at": _now(),
                "state": work.state.value,
                "result_type": "error",
                "error_type": type(exc).__name__,
            })
            work.emit("work.failed", capability_id=cap.id, error=repr(exc))
            self._record_execution(work, cap.id, "failure", f"{type(exc).__name__}: {exc}")
        self.store.save(work)
        self._checkpoint()
        return work

    def pause(self, work_id: str) -> Work:
        work = self.store.load(work_id)
        work.state = WorkState.PAUSED
        work.emit("work.paused")
        self.store.save(work)
        self._checkpoint()
        return work

    def resume(self, work_id: str, capability_id: str | None = None, approved: bool = False) -> Work:
        return self.run(work_id, capability_id, approved)
