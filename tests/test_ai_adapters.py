from abs_core.ai_adapters import ClaudeCapability, GeminiCapability
from abs_core.local_ai_adapter import LocalAICapability


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

def test_local_ai_adapter_applies_bounded_generation_options(monkeypatch) -> None:
    captured = {}

    def fake_post(url, headers, payload, timeout):
        captured.update({"url": url, "headers": headers, "payload": payload, "timeout": timeout})
        return {
            "model": "qwen3.5:0.8b",
            "message": {"role": "assistant", "content": "LOCAL_OK"},
            "done": True,
        }

    monkeypatch.setattr("abs_core.local_ai_adapter._post_json", fake_post)
    adapter = LocalAICapability(endpoint="http://127.0.0.1:11434", model="qwen3.5:0.8b")
    result = adapter.execute(
        "hello",
        {"max_tokens": 32, "temperature": 0, "think": False, "keep_alive": 0},
    )

    assert result["final_response"] == "LOCAL_OK"
    assert captured["url"] == "http://127.0.0.1:11434/api/chat"
    assert captured["payload"]["model"] == "qwen3.5:0.8b"
    assert captured["payload"]["options"]["num_predict"] == 32
    assert captured["payload"]["options"]["temperature"] == 0.0
    assert captured["payload"]["think"] is False
    assert captured["payload"]["keep_alive"] == 0

