from abs_core.tool_learning import ToolLearningEngine
from abs_core.tool_knowledge import ToolKnowledge, ToolKnowledgeRegistry


def test_learning_records_success_and_failure_evidence() -> None:
    registry = ToolKnowledgeRegistry()
    registry.register(ToolKnowledge(id="tool", name="Tool", category="code"))

    engine = ToolLearningEngine(registry)
    learned = engine.record(
        "tool",
        success=True,
        evidence={"type": "integration", "result": "ok"},
        lesson="structured input worked",
        usage_pattern="send structured task",
    )

    assert learned.status == "validated"
    assert learned.evidence[-1]["success"] is True
    assert learned.lessons == ["structured input worked"]

    degraded = engine.record(
        "tool",
        success=False,
        evidence={"type": "integration", "error": "timeout"},
    )
    assert degraded.status == "degraded"
    assert degraded.evidence[-1]["success"] is False
