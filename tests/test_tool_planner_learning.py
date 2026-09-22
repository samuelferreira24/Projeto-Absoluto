from abs_core.connections import ConnectionRegistry
from abs_core.resource_router import ResourceRouter
from abs_core.tool_catalog import default_tool_knowledge
from abs_core.tool_learning import ToolLearningEngine
from abs_core.tool_planner import ToolPlanner


def test_tool_planner_uses_knowledge_and_route() -> None:
    knowledge = default_tool_knowledge()
    connections = ConnectionRegistry.defaults()
    connections.update_status("claude-api", "configured", configured=True)

    plans = ToolPlanner(knowledge, ResourceRouter(connections)).plan(
        "analisar texto",
        ("reasoning",),
        preferred_categories=("ai",),
        require_configured=True,
    )

    assert plans
    assert any(plan.tool_id == "claude" for plan in plans)
    assert plans[0].routes


def test_learning_engine_records_explicit_evidence() -> None:
    knowledge = default_tool_knowledge()
    engine = ToolLearningEngine(knowledge)

    learned = engine.record(
        "codex",
        success=True,
        evidence={"type": "smoke-test", "result": "ok"},
        lesson="Codex can execute the validated coding path.",
        usage_pattern="send an approved coding objective through the CLI adapter",
    )

    assert learned.status == "validated"
    assert learned.evidence[-1]["success"] is True
    assert learned.lessons
