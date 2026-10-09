from abs_core.intelligence import CognitiveRuntime, IntelligenceRegistry, IntelligenceResource


def _runtime_with_resources():
    registry = IntelligenceRegistry()
    registry.register(IntelligenceResource(
        id="intelligence:local-ai:qwen3.5-0.8b",
        capability_id="local-ai:qwen3.5-0.8b",
        name="Qwen 0.8B",
        source="local",
        local=True,
        capabilities=("reasoning", "chat"),
        priority=10,
        metadata={"estimated_memory_mb": 1200},
    ))
    registry.register(IntelligenceResource(
        id="intelligence:local-ai:qwen3.5-4b",
        capability_id="local-ai:qwen3.5-4b",
        name="Qwen 4B",
        source="local",
        local=True,
        capabilities=("reasoning", "chat"),
        priority=25,
        metadata={"estimated_memory_mb": 4200},
    ))
    return registry


def test_explicit_capability_selection_is_honored(monkeypatch, tmp_path):
    monkeypatch.setattr(CognitiveRuntime, "_new_id", staticmethod(lambda: "test-session"))
    monkeypatch.setattr(CognitiveRuntime, "_load", lambda self, sid: {
        "id": sid, "created_at": "", "updated_at": "", "preferred_resource": None,
        "context": {"capability_id": "local-ai:qwen3.5-0.8b"}, "messages": [],
    })
    runtime = CognitiveRuntime.__new__(CognitiveRuntime)
    runtime.intelligence = _runtime_with_resources()
    session = {"context": {"capability_id": "local-ai:qwen3.5-0.8b"}, "preferred_resource": None}
    ranked = runtime._rank_resources(session)
    assert ranked[0].capability_id == "local-ai:qwen3.5-0.8b"


def test_memory_pressure_reduces_large_local_model_priority(monkeypatch):
    runtime = CognitiveRuntime.__new__(CognitiveRuntime)
    runtime.intelligence = _runtime_with_resources()
    monkeypatch.setattr(
        "builtins.open",
        lambda *args, **kwargs: __import__("io").StringIO("MemAvailable:       2600000 kB\n"),
    )
    ranked = runtime._rank_resources({"context": {}, "preferred_resource": None})
    assert ranked[0].capability_id == "local-ai:qwen3.5-0.8b"



def test_explicit_large_model_preference_cannot_bypass_memory_gate(monkeypatch):
    runtime = CognitiveRuntime.__new__(CognitiveRuntime)
    runtime.intelligence = _runtime_with_resources()
    monkeypatch.setattr(
        "builtins.open",
        lambda *args, **kwargs: __import__("io").StringIO("MemAvailable:       2600000 kB\\n"),
    )
    ranked = runtime._rank_resources(
        {"context": {"capability_id": "local-ai:qwen3.5-4b"}, "preferred_resource": None}
    )
    assert all(item.capability_id != "local-ai:qwen3.5-4b" for item in ranked)
    assert ranked and ranked[0].capability_id == "local-ai:qwen3.5-0.8b"


def test_unknown_memory_fails_closed_for_sized_local_models(monkeypatch):
    runtime = CognitiveRuntime.__new__(CognitiveRuntime)
    runtime.intelligence = _runtime_with_resources()

    def unavailable(*args, **kwargs):
        raise OSError("meminfo unavailable")

    monkeypatch.setattr("builtins.open", unavailable)
    ranked = runtime._rank_resources({"context": {}, "preferred_resource": None})
    assert ranked == []


def test_turn_routes_to_the_exact_explicit_capability(monkeypatch):
    import threading
    from types import SimpleNamespace
    from abs_core.intelligence import CognitiveRuntime, IntelligenceRegistry, IntelligenceResource

    caps = {
        "local-ai:a": SimpleNamespace(id="local-ai:a", kind="local_ai", metadata={"conversational": True}),
        "local-ai:b": SimpleNamespace(id="local-ai:b", kind="local_ai", metadata={"conversational": True}),
    }

    class CapabilitySet:
        def get(self, capability_id):
            return caps[capability_id]

        def list(self):
            return list(caps.values())

    class FakeOrchestrator:
        def __init__(self):
            self.seen = []

        def create(self, objective, context):
            return SimpleNamespace(id="work-1")

        def run(self, work_id, capability_id, approved=False):
            self.seen.append(capability_id)
            return SimpleNamespace(
                id=work_id,
                state=SimpleNamespace(value="completed"),
                result={"final_response": "ok"},
                provenance=[{"capability_id": capability_id}],
                capability_id=capability_id,
            )

    intelligence = IntelligenceRegistry()
    intelligence.register(IntelligenceResource(
        id="intelligence:local-ai:a", capability_id="local-ai:a", name="A",
        source="local", local=True, capabilities=("chat",), status="configured",
        priority=100, metadata={"estimated_memory_mb": 100, "conversational": True},
    ))
    intelligence.register(IntelligenceResource(
        id="intelligence:local-ai:b", capability_id="local-ai:b", name="B",
        source="local", local=True, capabilities=("chat",), status="configured",
        priority=1, metadata={"estimated_memory_mb": 100, "conversational": True},
    ))
    orchestrator = FakeOrchestrator()
    runtime = CognitiveRuntime.__new__(CognitiveRuntime)
    runtime.capabilities = CapabilitySet()
    runtime.intelligence = intelligence
    runtime.orchestrator = orchestrator
    runtime._lock = threading.RLock()
    runtime.max_history = 24
    runtime.tool_runtime = None
    runtime.data_layer = None
    session = {
        "id": "session-1", "created_at": "", "updated_at": "",
        "preferred_resource": None, "context": {}, "messages": [],
    }
    runtime._load = lambda sid: session
    runtime._save = lambda current: None

    result = runtime.turn(
        "test explicit routing", session_id="session-1",
        context={"capability_id": "local-ai:b"}, approved=True,
    )

    assert result["work_state"] == "completed"
    assert orchestrator.seen == ["local-ai:b"]
    assert result["resource"]["capability_id"] == "local-ai:b"
