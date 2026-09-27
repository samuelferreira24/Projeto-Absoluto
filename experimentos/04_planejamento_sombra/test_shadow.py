from shadow_planner import ShadowMission, build_shadow_plan, evaluate_plan
from abs_core.capabilities import CapabilityRecord, CapabilityRegistry
from abs_core.connections import ConnectionRecord, ConnectionRegistry
from abs_core.resource_router import ResourceRouter


class FakeCapability:
    def __init__(self, ident):
        self.id = ident
        self.name = ident

    def execute(self, objective, context):
        return {"type": "fake", "capability": self.id}


def fixture():
    caps = CapabilityRegistry()
    caps.register(CapabilityRecord(
        "direct", "direct", "test", FakeCapability("direct"),
        metadata={"capabilities": ("execute",)},
    ))
    caps.register(CapabilityRecord(
        "research", "research", "test", FakeCapability("research"),
        metadata={"capabilities": ("research",)},
    ))

    connections = ConnectionRegistry()
    connections.register(ConnectionRecord(
        id="phone", name="phone", category="device", transport="local",
        status="available", configured=True, capabilities=("execute", "research"),
    ))
    connections.register(ConnectionRecord(
        id="vps", name="vps", category="server", transport="http",
        status="available", configured=True, capabilities=("execute",),
    ))
    return caps, ResourceRouter(connections)


def test_shadow_separates_mode_from_resource():
    caps, router = fixture()
    p1 = build_shadow_plan(ShadowMission("x", {"high_uncertainty": True}), caps, router)
    p2 = build_shadow_plan(ShadowMission("x", {"high_uncertainty": True, "resource": "vps"}), caps, router)
    assert p1.mode == p2.mode == "RESEARCH"


def test_shadow_detects_missing_capability_without_execution():
    caps, router = fixture()
    p = build_shadow_plan(ShadowMission("x", {"open_ended": True}), caps, router)
    result = evaluate_plan(p, caps, router)
    assert result["mode"] == "AGENT"
    assert result["executable"] is False


def test_shadow_finds_existing_research_path():
    caps, router = fixture()
    p = build_shadow_plan(ShadowMission("x", {"high_uncertainty": True}), caps, router)
    result = evaluate_plan(p, caps, router)
    assert result["mode"] == "RESEARCH"
    assert result["executable"] is True


if __name__ == "__main__":
    test_shadow_separates_mode_from_resource()
    test_shadow_detects_missing_capability_without_execution()
    test_shadow_finds_existing_research_path()
    print("EXPERIMENTO_04: PASS — planejamento em sombra")
