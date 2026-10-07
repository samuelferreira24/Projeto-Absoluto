from abs_core.capabilities import CapabilityRecord, CapabilityRegistry
from abs_core.intelligence import CognitiveRuntime, IntelligenceRegistry, IntelligenceResource
from abs_core.orchestrator import Orchestrator
from abs_core.store import WorkStore


class FakeChat:
    id = "fake-chat"
    name = "Fake Chat"

    def execute(self, objective, context):
        messages = context["conversation"]["messages"]
        return {
            "type": "fake-chat",
            "final_response": f"resposta:{objective}:turns={len(messages)}",
        }


def test_cognitive_runtime_keeps_open_conversation() -> None:
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("fake-chat", "Fake Chat", "test", FakeChat()))
    intelligence = IntelligenceRegistry()
    intelligence.register(IntelligenceResource(
        id="intelligence:fake-chat",
        capability_id="fake-chat",
        name="Fake Chat",
        source="local",
        local=True,
        capabilities=("conversation", "reasoning"),
        status="available",
    ))
    runtime = CognitiveRuntime(registry, intelligence, Orchestrator(registry, WorkStore(":memory:")), store_path=":memory:")
    first = runtime.turn("quero conversar", approved=True)
    second = runtime.turn("continue a ideia", session_id=first["session_id"], approved=True)

    assert second["session_id"] == first["session_id"]
    assert second["message_count"] == 4
    assert second["result"]["type"] == "fake-chat"


def test_cognitive_runtime_allows_explicit_resource_without_fixed_command() -> None:
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("fake-chat", "Fake Chat", "test", FakeChat()))
    intelligence = IntelligenceRegistry()
    intelligence.register(IntelligenceResource(
        id="intelligence:fake-chat", capability_id="fake-chat",
        name="Fake Chat", source="local", local=True, status="available",
    ))
    runtime = CognitiveRuntime(registry, intelligence, store_path=":memory:")
    result = runtime.turn("pesquise isto", preferred_resource="intelligence:fake-chat", approved=True)
    assert result["response"].startswith("resposta:pesquise isto")


def test_conversational_resource_does_not_require_action_approval() -> None:
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("fake-chat", "Fake Chat", "external_ai", FakeChat()))
    intelligence = IntelligenceRegistry()
    intelligence.register(IntelligenceResource(
        id="intelligence:fake-chat", capability_id="fake-chat",
        name="Fake Chat", source="local", local=True, status="available",
        metadata={"conversational": True},
    ))
    runtime = CognitiveRuntime(registry, intelligence, store_path=":memory:")
    result = runtime.turn("vamos conversar", approved=False)
    assert result["work_state"] == "completed"
    assert result["response"].startswith("resposta:vamos conversar")


class FailingChat:
    id = "failing-chat"
    name = "Failing Chat"

    def execute(self, objective, context):
        raise RuntimeError("simulated_provider_failure")


def test_cognitive_runtime_falls_back_to_next_available_intelligence() -> None:
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("failing-chat", "Failing Chat", "external_ai", FailingChat()))
    registry.register(CapabilityRecord("fake-chat", "Fake Chat", "external_ai", FakeChat()))
    intelligence = IntelligenceRegistry()
    intelligence.register(IntelligenceResource(
        id="intelligence:failing-chat", capability_id="failing-chat",
        name="Failing Chat", source="remote", local=False, status="available",
        priority=20.0, metadata={"conversational": True},
    ))
    intelligence.register(IntelligenceResource(
        id="intelligence:fake-chat", capability_id="fake-chat",
        name="Fake Chat", source="remote", local=False, status="available",
        priority=5.0, metadata={"conversational": True},
    ))
    runtime = CognitiveRuntime(registry, intelligence, store_path=":memory:")
    result = runtime.turn("teste de fallback")
    assert result["work_state"] == "completed"
    assert result["resource"]["capability_id"] == "fake-chat"
    assert len(result["fallback_attempts"]) == 2
    assert result["fallback_attempts"][0]["state"] == "failed"
    assert result["fallback_attempts"][1]["state"] == "completed"


def test_cognitive_runtime_offline_mode_filters_remote_intelligence() -> None:
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("fake-chat", "Fake Chat", "test", FakeChat()))
    intelligence = IntelligenceRegistry()
    intelligence.register(IntelligenceResource(
        id="intelligence:remote", capability_id="fake-chat",
        name="Remote", source="remote", local=False, status="available", priority=50.0,
    ))
    intelligence.register(IntelligenceResource(
        id="intelligence:local", capability_id="fake-chat",
        name="Local", source="local", local=True, status="available", priority=1.0,
    ))
    runtime = CognitiveRuntime(registry, intelligence, store_path=":memory:")
    result = runtime.turn("modo offline", context={"offline": True}, approved=True)
    assert result["resource"]["id"] == "intelligence:local"
