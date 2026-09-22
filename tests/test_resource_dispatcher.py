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


class FailingCapability:
    id = "claude"
    name = "Claude"
    def __init__(self, responses):
        self.responses = list(responses)
    def execute(self, objective, context):
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def test_dispatcher_falls_back_after_execution_failure() -> None:
    connections = ConnectionRegistry.defaults()
    connections.update_status("claude-api", "configured", configured=True)
    connections.update_status("gemini-api", "configured", configured=True)
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("claude", "Claude", "external_ai", FailingCapability([RuntimeError("down")])))
    registry.register(CapabilityRecord("gemini", "Gemini", "external_ai", FakeCapability()))
    knowledge = default_tool_knowledge()
    router = ResourceRouter(connections)
    dispatcher = ResourceDispatcher(router, ToolPlanner(knowledge, router), registry, knowledge)
    orch = Orchestrator(registry, WorkStore(":memory:"))

    result = dispatcher.dispatch(
        "fallback",
        ResourceRouteRequest(
            objective="fallback",
            required_capabilities=("reasoning",),
            preferred_categories=("ai",),
            require_configured=True,
        ),
        approved=True,
        orchestrator=orch,
    )

    assert result.selected_connection == "gemini-api"
    assert [attempt.status for attempt in result.attempts] == ["failed", "completed"]
    assert knowledge.get("claude").reliability() == 0.0
    assert knowledge.get("gemini").reliability() == 1.0


def test_learning_changes_planning_order() -> None:
    connections = ConnectionRegistry.defaults()
    connections.update_status("claude-api", "configured", configured=True)
    connections.update_status("gemini-api", "configured", configured=True)
    knowledge = default_tool_knowledge()
    knowledge.learn("claude", evidence={"success": False}, status="degraded")
    knowledge.learn("gemini", evidence={"success": True}, status="validated")
    planner = ToolPlanner(knowledge, ResourceRouter(connections))

    plans = planner.plan(
        "choose reliable reasoning",
        ("reasoning",),
        preferred_categories=("ai",),
        require_configured=True,
    )
    ids = [plan.tool_id for plan in plans]
    assert ids[0] == "gemini"
    assert ids.index("gemini") < ids.index("claude")
