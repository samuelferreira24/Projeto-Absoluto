from dataclasses import dataclass, field
from typing import Any, ClassVar

from abs_core.capabilities import CapabilityRecord, CapabilityRegistry
from abs_core.connections import ConnectionRecord, ConnectionRegistry
from abs_core.resource_router import ResourceRouter, ResourceRouteRequest


@dataclass
class Mission:
    objective: str
    mode: str
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class SandboxResult:
    status: str
    capability: str
    resource: str
    evidence: dict[str, Any]


class SandboxCapability:
    def __init__(self, ident: str, outcomes=None):
        self.id = ident
        self.name = ident
        self.outcomes = list(outcomes or ["success"])

    def execute(self, objective, context):
        outcome = self.outcomes.pop(0)
        return {"status": outcome, "objective": objective, "context": context}


class SandboxRuntime:
    MODE_CAPABILITIES = {
        "DIRECT": ("execute",),
        "WORKFLOW": ("workflow",),
        "RESEARCH": ("research",),
        "AGENT": ("reasoning",),
        "MULTIAGENT": ("parallel",),
        "RECOVERY": ("recovery",),
    }

    def __init__(self, capabilities, router):
        self.capabilities = capabilities
        self.router = router

    def run(self, mission: Mission) -> SandboxResult:
        required = self.MODE_CAPABILITIES[mission.mode]
        caps = [c for c in self.capabilities.list()
                if set(required).issubset(set(c.metadata.get("capabilities", ())))]
        if not caps:
            return SandboxResult("CAPABILITY_MISSING", "", "", {"required": required})

        request = ResourceRouteRequest(
            objective=mission.objective,
            required_capabilities=required,
            context=mission.context,
        )
        routes = self.router.rank(request)
        if not routes:
            return SandboxResult("RESOURCE_UNAVAILABLE", caps[0].id, "", {"required": required})

        cap = caps[0]
        route = routes[0]
        result = cap.adapter.execute(mission.objective, mission.context)
        return SandboxResult(
            result["status"], cap.id, route.connection_id,
            {"mode": mission.mode, "required": required},
        )


def fixture():
    caps = CapabilityRegistry()
    for ident, ability in [
        ("direct", "execute"),
        ("workflow", "workflow"),
        ("research", "research"),
        ("agent", "reasoning"),
        ("multiagent", "parallel"),
        ("recovery", "recovery"),
    ]:
        caps.register(CapabilityRecord(
            ident, ident, "test", SandboxCapability(ident),
            metadata={"capabilities": (ability,)},
        ))

    connections = ConnectionRegistry()
    connections.register(ConnectionRecord(
        id="phone", name="phone", category="device", transport="local",
        status="available", configured=True,
        capabilities=("execute", "workflow", "research", "reasoning", "parallel", "recovery"),
    ))
    connections.register(ConnectionRecord(
        id="vps", name="vps", category="server", transport="http",
        status="available", configured=True,
        capabilities=("execute", "research"),
    ))
    return caps, ResourceRouter(connections)


def run():
    caps, router = fixture()
    rt = SandboxRuntime(caps, router)

    direct_phone = rt.run(Mission("simple", "DIRECT"))
    research_phone = rt.run(Mission("investigate", "RESEARCH"))
    agent = rt.run(Mission("open problem", "AGENT"))
    missing_resource = SandboxRuntime(
        caps,
        ResourceRouter(ConnectionRegistry())
    ).run(Mission("open problem", "AGENT"))

    assert direct_phone.status == "success"
    assert research_phone.status == "success"
    assert agent.status == "success"
    assert direct_phone.resource == "phone"
    assert research_phone.resource == "phone"
    assert agent.resource == "phone"
    assert missing_resource.status == "RESOURCE_UNAVAILABLE"

    # Resource changes must not change the mold itself.
    assert rt.run(Mission("investigate", "RESEARCH", {"resource": "vps"})).status == "success"

    print("EXPERIMENTO_07: PASS")
    print("Real CapabilityRegistry + ResourceRouter: PASS")
    print("Sandbox executor: PASS")
    print("Resource fallback/absence: PASS")


if __name__ == "__main__":
    run()
