import os

from abs_core.openai_adapter import OpenAICapability


def test_openai_capability_requires_key() -> None:
    capability = OpenAICapability(api_key="")
    try:
        capability.execute("test", {})
    except RuntimeError as exc:
        assert "OPENAI_API_KEY" in str(exc)
        return
    assert False, "OpenAI capability must require explicit credentials"


def test_openai_capability_configuration_is_replaceable(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("ABS_OPENAI_MODEL", "test-model")
    capability = OpenAICapability()
    assert capability.model == "test-model"
    assert capability.api_key == "test-key"
