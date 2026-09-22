from abs_core.tool_knowledge import ToolKnowledge, ToolKnowledgeRegistry
from abs_core.tool_knowledge_store import ToolKnowledgeStore


def test_tool_knowledge_store_survives_registry_reload(tmp_path) -> None:
    path = tmp_path / "knowledge.db"
    store = ToolKnowledgeStore(path)

    first = ToolKnowledgeRegistry()
    first.register(ToolKnowledge(
        id="codex",
        name="Codex",
        category="code",
        capabilities=["code"],
        status="validated",
        lessons=["use approved execution path"],
    ))
    assert store.save_registry(first) == 1

    second = ToolKnowledgeRegistry()
    assert store.load_into(second) == 1
    restored = second.get("codex")
    assert restored.status == "validated"
    assert restored.lessons == ["use approved execution path"]
