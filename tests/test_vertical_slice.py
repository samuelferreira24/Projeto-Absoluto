import tempfile
from abs_core.adapters import EchoCapability
from abs_core.capabilities import CapabilityRecord, CapabilityRegistry
from abs_core.orchestrator import Orchestrator
from abs_core.store import WorkStore

def test_create_run_persist_resume():
    with tempfile.NamedTemporaryFile(suffix=".db") as f:
        store = WorkStore(f.name)
        registry = CapabilityRegistry()
        registry.register(CapabilityRecord("echo", "Echo", "test", EchoCapability()))
        orch = Orchestrator(registry, store)
        work = orch.create("prove the execution loop", {"source": "test"})
        result = orch.run(work.id)
        loaded = store.load(work.id)
        assert result.state.value == "completed"
        assert loaded.result["objective"] == "prove the execution loop"
        assert [e.type for e in loaded.events] == ["work.created", "work.started", "work.completed"]
        resumed = orch.resume(work.id, "echo")
        assert resumed.state.value == "completed"
        assert len(resumed.provenance) == 2

def test_capability_can_be_replaced_between_runs():
    class Second(EchoCapability):
        id = "second"
        name = "Second capability"
    store = WorkStore()
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("echo", "Echo", "test", EchoCapability()))
    registry.register(CapabilityRecord("second", "Second", "test", Second()))
    orch = Orchestrator(registry, store)
    work = orch.create("transfer me")
    first = orch.run(work.id, "echo")
    second = orch.resume(work.id, "second")
    assert first.provenance[-1]["capability_id"] == "echo"
    assert second.provenance[-1]["capability_id"] == "second"

def test_external_capability_requires_approval():
    class External:
        id = "external"
        name = "External"
        def execute(self, objective, context):
            return {"ok": True}
    store = WorkStore()
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("external", "External", "external_ai", External()))
    orch = Orchestrator(registry, store)
    work = orch.create("protected")
    try:
        orch.run(work.id, "external")
    except PermissionError:
        pass
    else:
        raise AssertionError("external capability executed without approval")
    assert store.load(work.id).events[-1].type == "work.denied"

def test_capability_session_is_persisted_and_reused():
    class SessionCapability:
        id = "session"
        name = "Session capability"
        def __init__(self):
            self.received = []
        def execute(self, objective, context):
            self.received.append(context.get("_codex_thread_id"))
            return {"thread_id": "thread-123", "turn": len(self.received)}

    with tempfile.NamedTemporaryFile(suffix=".db") as f:
        store = WorkStore(f.name)
        registry = CapabilityRegistry()
        adapter = SessionCapability()
        registry.register(CapabilityRecord("session", "Session", "test", adapter))
        orch = Orchestrator(registry, store)
        work = orch.create("continue me")
        orch.run(work.id, "session")
        persisted = store.load(work.id)
        assert persisted.sessions["session"]["thread_id"] == "thread-123"
        orch.resume(work.id, "session")
        assert adapter.received == [None, "thread-123"]
