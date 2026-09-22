from abs_core.resource_router import ResourceRouter
from abs_core.connections import ConnectionRegistry
from abs_core.tool_catalog import default_tool_knowledge
from abs_core.tool_planner import ToolPlanner


def test_tool_planner_connects_tool_knowledge_to_routes() -> None:
    connections = ConnectionRegistry.defaults()
    connections.update_status("claude-api", "configured", configured=True)
    knowledge = default_tool_knowledge()
    planner = ToolPlanner(knowledge, ResourceRouter(connections))

    plans = planner.plan(
        "analisar texto",
        ("reasoning",),
        preferred_categories=("ai",),
        require_configured=True,
    )

    assert plans
    assert any(plan.tool_id in {"chatgpt", "claude", "gemini"} for plan in plans)
    assert all(plan.routes for plan in plans)


def test_tool_planner_requires_all_capabilities() -> None:
    connections = ConnectionRegistry.defaults()
    connections.update_status("claude-api", "configured", configured=True)
    knowledge = default_tool_knowledge()
    planner = ToolPlanner(knowledge, ResourceRouter(connections))
    plans = planner.plan("complex task", ("reasoning", "code"), require_configured=True)
    assert plans == []
