from abs_core.ai_adapters import ClaudeCapability, GeminiCapability


def test_claude_adapter_parses_text(monkeypatch) -> None:
    def fake_post(*args, **kwargs):
        return {
            "id": "msg-test",
            "model": "claude-test",
            "content": [{"type": "text", "text": "CLAUDE_OK"}],
        }
    monkeypatch.setenv("ANTHROPIC_API_KEY", "key")
    monkeypatch.setattr("abs_core.ai_adapters._post_json", fake_post)
    result = ClaudeCapability().execute("hello", {})
    assert result["final_response"] == "CLAUDE_OK"
    assert result["message_id"] == "msg-test"


def test_gemini_adapter_parses_interaction_output(monkeypatch) -> None:
    def fake_post(*args, **kwargs):
        return {
            "id": "interaction-test",
            "model": "gemini-test",
            "output_text": "GEMINI_OK",
        }
    monkeypatch.setenv("GEMINI_API_KEY", "key")
    monkeypatch.setattr("abs_core.ai_adapters._post_json", fake_post)
    result = GeminiCapability().execute("hello", {})
    assert result["final_response"] == "GEMINI_OK"
    assert result["interaction_id"] == "interaction-test"
