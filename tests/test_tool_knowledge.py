from abs_core.tool_knowledge import ToolKnowledge, ToolKnowledgeRegistry


def test_tool_knowledge_can_learn_from_evidence() -> None:
    registry = ToolKnowledgeRegistry()
    registry.register(ToolKnowledge(
        id="example",
        name="Example Tool",
        category="code",
    ))

    learned = registry.learn(
        "example",
        capabilities=["code", "analysis"],
        connection_ids=["api-http"],
        usage_pattern="send structured task and parse result",
        lesson="requires structured input",
        evidence={"type": "test", "passed": True},
        status="validated",
    )

    assert learned.status == "validated"
    assert set(learned.capabilities) == {"code", "analysis"}
    assert learned.connection_ids == ["api-http"]
    assert learned.evidence[0]["passed"] is True


def test_tool_knowledge_searches_capabilities() -> None:
    registry = ToolKnowledgeRegistry()
    registry.register(ToolKnowledge(
        id="a", name="A", category="ai", capabilities=["reasoning"]
    ))
    registry.register(ToolKnowledge(
        id="b", name="B", category="code", capabilities=["code"]
    ))

    assert [item.id for item in registry.find_by_capability("reasoning")] == ["a"]
