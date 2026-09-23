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
