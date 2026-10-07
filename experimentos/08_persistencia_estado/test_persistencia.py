from abs_core.capabilities import CapabilityRecord, CapabilityRegistry
from abs_core.models import WorkState
from abs_core.store import WorkStore


class Fake:
    def __init__(self, ident="direct"):
        self.id = ident
        self.name = ident

    def execute(self, objective, context):
        return {"type": "sandbox", "status": "success"}


def test_plan_state_survives_reload(tmp_path):
    path = tmp_path / "abs-sandbox.db"
    store = WorkStore(path)
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("direct", "Direct", "test", Fake(), metadata={"mode": "DIRECT"}))

    from abs_core.orchestrator import Orchestrator
    orch = Orchestrator(registry, store)

    work = orch.create("persistent mission", {"mode": "DIRECT", "plan_id": "P1"})
    work = orch.run(work.id, "direct", approved=True)

    reloaded = store.load(work.id)
    assert reloaded.objective == "persistent mission"
    assert reloaded.context["plan_id"] == "P1"
    assert reloaded.state == WorkState.COMPLETED
    assert reloaded.result["status"] == "success"
    assert reloaded.provenance


def test_running_work_is_recovered_after_restart(tmp_path):
    path = tmp_path / "abs-recovery.db"
    store = WorkStore(path)
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("direct", "Direct", "test", Fake(), metadata={"mode": "DIRECT"}))

    work = __import__("abs_core.models", fromlist=["Work"]).Work("interrupted", {"mode": "DIRECT"})
    work.state = WorkState.RUNNING
    store.save(work)

    restarted = WorkStore(path)
    recovered = restarted.recover_interrupted()
    assert work.id in recovered
    assert restarted.load(work.id).state == WorkState.PAUSED


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-q"]))
