from abs_core.capabilities import CapabilityRecord, CapabilityRegistry
from abs_core.connections import ConnectionRegistry
from abs_core.orchestrator import Orchestrator
from abs_core.resource_dispatcher import ResourceDispatcher
from abs_core.resource_router import ResourceRouteRequest, ResourceRouter
from abs_core.store import WorkStore
from abs_core.tool_catalog import default_tool_knowledge
from abs_core.tool_planner import ToolPlanner


class FakeCapability:
    id = "fake"
    name = "Fake"
    def execute(self, objective, context):
        return {"type": "fake", "final_response": "ok"}


def test_dispatcher_selects_executable_connection() -> None:
    connections = ConnectionRegistry.defaults()
    connections.update_status("claude-api", "configured", configured=True)
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("claude", "Claude", "external_ai", FakeCapability()))
    knowledge = default_tool_knowledge()
    router = ResourceRouter(connections)
    planner = ToolPlanner(knowledge, router)
    dispatcher = ResourceDispatcher(router, planner, registry, knowledge)
    orch = Orchestrator(registry, WorkStore(":memory:"))

    result = dispatcher.dispatch(
        "test",
        ResourceRouteRequest(
            objective="test",
            required_capabilities=("reasoning",),
            preferred_categories=("ai",),
            require_configured=True,
        ),
        approved=True,
        orchestrator=orch,
    )

    assert result.selected_connection == "claude-api"
    assert result.work.state.value == "completed"
    assert result.attempts[-1].status == "completed"


def test_dispatcher_requires_authorization_for_external_capability() -> None:
    connections = ConnectionRegistry.defaults()
    connections.update_status("claude-api", "configured", configured=True)
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("claude", "Claude", "external_ai", FakeCapability()))
    knowledge = default_tool_knowledge()
    router = ResourceRouter(connections)
    dispatcher = ResourceDispatcher(router, ToolPlanner(knowledge, router), registry, knowledge)
    orch = Orchestrator(registry, WorkStore(":memory:"))

    try:
        dispatcher.dispatch(
            "test",
            ResourceRouteRequest(
                objective="test",
                required_capabilities=("reasoning",),
                require_configured=True,
            ),
            approved=False,
            orchestrator=orch,
        )
    except PermissionError:
        return
    assert False, "external dispatch must preserve Imperator approval"
