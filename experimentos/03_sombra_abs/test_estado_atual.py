"""Experimento 03 — controle contra o ABS atual.

Não altera abs_core. Mede uma propriedade concreta do código atual:
CapabilityRegistry.choose() sem capability_id escolhe o primeiro registro.
Isso é deliberadamente usado como baseline contra o seletor de moldes.
"""

from abs_core.capabilities import CapabilityRecord, CapabilityRegistry


class FakeCapability:
    def __init__(self, name):
        self.id = name
        self.name = name

    def execute(self, objective, context):
        return {"type": "fake", "capability": self.id}


def test_current_registry_is_not_strategy_selector():
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("direct-cap", "Direct", "test", FakeCapability("direct-cap"),
                                       metadata={"mode": "DIRECT"}))
    registry.register(CapabilityRecord("agent-cap", "Agent", "test", FakeCapability("agent-cap"),
                                       metadata={"mode": "AGENT"}))

    chosen = registry.choose()
    assert chosen.id == "direct-cap"

    # Even with an open-ended mission represented in the metadata, the current
    # registry does not inspect context and does not choose AGENT.
    chosen_again = registry.choose()
    assert chosen_again.metadata["mode"] == "DIRECT"


def test_explicit_capability_selection_exists():
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("direct-cap", "Direct", "test", FakeCapability("direct-cap"),
                                       metadata={"mode": "DIRECT"}))
    registry.register(CapabilityRecord("agent-cap", "Agent", "test", FakeCapability("agent-cap"),
                                       metadata={"mode": "AGENT"}))

    assert registry.choose("agent-cap").id == "agent-cap"


if __name__ == "__main__":
    test_current_registry_is_not_strategy_selector()
    test_explicit_capability_selection_exists()
    print("EXPERIMENTO_03: PASS — baseline atual confirmado")
