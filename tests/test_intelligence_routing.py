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
