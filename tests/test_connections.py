from abs_core.connections import ConnectionRegistry


def test_default_connections_cover_multiple_transport_families() -> None:
    registry = ConnectionRegistry.defaults()
    ids = {item.id for item in registry.list()}
    assert {"codex-termux", "chatgpt-connector", "claude-api", "gemini-api",
            "internet-http", "api-http", "github-api", "github-termux",
            "local-ai", "local-network", "remote-device"} <= ids


def test_connection_registry_is_extensible() -> None:
    from abs_core.connections import ConnectionRecord
    registry = ConnectionRegistry.defaults()
    registry.register(ConnectionRecord(
        id="custom-tool",
        name="Custom Tool",
        category="service",
        transport="mcp",
        capabilities=["custom"],
    ))
    assert registry.get("custom-tool").transport == "mcp"


def test_connection_public_data_never_contains_secret_value(monkeypatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "secret-value")
    registry = ConnectionRegistry.defaults()
    public = registry.get("claude-api").public()
    assert public["configured"] is True
    assert "secret-value" not in str(public)
    assert public["metadata"]["credential_env"] == "ANTHROPIC_API_KEY"
