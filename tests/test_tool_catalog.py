from abs_core.tool_catalog import default_tool_knowledge


def test_default_catalog_contains_multiple_tool_families() -> None:
    registry = default_tool_knowledge()
    items = {item.id: item for item in registry.list()}

    assert {"chatgpt", "codex", "claude", "gemini", "perplexity", "sora", "suno"} <= set(items)
    assert items["codex"].status == "catalogued"
    assert "code" in items["codex"].capabilities
