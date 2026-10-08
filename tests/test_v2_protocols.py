from __future__ import annotations

from abs_core.v2 import ModeSelector, RiskGovernor, V2Mode
from abs_core.v2_protocols import ProtocolRegistry, ProtocolTarget


def test_protocol_registry_is_optional_and_empty_by_default(monkeypatch):
    monkeypatch.delenv("ABS_MCP_ENDPOINT", raising=False)
    monkeypatch.delenv("ABS_A2A_ENDPOINT", raising=False)
    registry = ProtocolRegistry()
    registry.discover_from_env()
    assert registry.public() == {"mcp": [], "a2a": []}


def test_protocol_targets_are_replaceable():
    registry = ProtocolRegistry()
    registry.register_mcp(ProtocolTarget("mcp:test", "http://127.0.0.1:9991"))
    registry.register_a2a(ProtocolTarget("a2a:test", "http://127.0.0.1:9992"))
    public = registry.public()
    assert public["mcp"][0]["id"] == "mcp:test"
    assert public["a2a"][0]["id"] == "a2a:test"


def test_mode_selector_prefers_smallest_sufficient_mechanism():
    selector = ModeSelector()
    risk = RiskGovernor().profile("x", {})
    assert selector.choose("x", {}, risk)[0] == V2Mode.DIRECT
    assert selector.choose("x", {"steps": ["a", "b"]}, risk)[0] == V2Mode.WORKFLOW
    assert selector.choose("x", {"adaptive": True}, risk)[0] == V2Mode.AGENT
    assert selector.choose("x", {"subagents": 2}, risk)[0] == V2Mode.MULTIAGENT
