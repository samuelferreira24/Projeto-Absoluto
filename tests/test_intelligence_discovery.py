from abs_core.capabilities import CapabilityRecord, CapabilityRegistry
from abs_core.intelligence import IntelligenceRegistry


def test_codex_is_not_classified_as_local_and_metadata_capabilities_are_used():
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord(
        "codex", "Codex", "external_ai", object(),
        metadata={"capabilities": ["reasoning", "coding", "tools"]},
    ))
    registry.register(CapabilityRecord(
        "local-ai:qwen3.5-0.8b", "Qwen", "local_ai", object(),
        metadata={"capabilities": ["reasoning", "chat", "tools"]},
    ))
    intelligence = IntelligenceRegistry()
    found = intelligence.discover_from_capabilities(registry)
    codex = next(x for x in found if x.capability_id == "codex")
    qwen = next(x for x in found if x.capability_id.startswith("local-ai:"))
    assert codex.local is False
    assert "coding" in codex.capabilities
    assert qwen.local is True
    assert "chat" in qwen.capabilities
