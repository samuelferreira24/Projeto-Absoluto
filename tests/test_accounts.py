from abs_core.accounts import AccountRecord, AccountRegistry


def test_multiple_accounts_same_provider_are_distinct():
    registry = AccountRegistry()
    registry.register(AccountRecord(
        id="chatgpt-1", provider="chatgpt", name="ChatGPT 1",
        connection_id="chatgpt-connector",
        credential_ref="secret://chatgpt/1",
    ))
    registry.register(AccountRecord(
        id="chatgpt-2", provider="chatgpt", name="ChatGPT 2",
        connection_id="chatgpt-connector",
        credential_ref="secret://chatgpt/2",
    ))

    accounts = registry.by_provider("chatgpt")
    assert [a.id for a in accounts] == ["chatgpt-1", "chatgpt-2"]
    public = registry.public()
    assert all(item["credential_ref"] is True for item in public)
    assert "secret://chatgpt/1" not in str(public)


def test_account_can_use_different_connection_paths():
    registry = AccountRegistry()
    registry.register(AccountRecord(
        id="claude-api-1", provider="claude", name="Claude API 1",
        connection_id="claude-api", capabilities=["reasoning"],
    ))
    registry.register(AccountRecord(
        id="claude-local-1", provider="claude", name="Claude Local",
        connection_id="local-network", capabilities=["reasoning"],
    ))
    assert {a.connection_id for a in registry.by_provider("claude")} == {
        "claude-api", "local-network"
    }


def test_public_account_does_not_expose_metadata():
    registry = AccountRegistry(":memory:")
    registry.register(AccountRecord(
        id="safe-1",
        provider="example",
        name="Safe",
        connection_id="api-http",
        credential_ref="secret://safe",
        metadata={"token": "DO_NOT_EXPOSE"},
    ))
    public = registry.public()[0]
    assert "metadata" not in public
    assert "DO_NOT_EXPOSE" not in str(public)
