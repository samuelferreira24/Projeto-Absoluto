from abs_core.tool_discovery import ToolDiscovery, ToolDiscoveryCandidate


def test_tool_discovery_requires_valid_source() -> None:
    discovery = ToolDiscovery()
    candidate = discovery.from_url("https://example.com/tool", category="ai")
    assert candidate.name == "example.com"
    assert candidate.category == "ai"
    assert discovery.validate_candidate(candidate) == []


def test_tool_discovery_rejects_invalid_url() -> None:
    discovery = ToolDiscovery()
    try:
        discovery.from_url("not-a-url")
    except ValueError:
        return
    assert False, "invalid source URL must be rejected"


def test_candidate_preserves_capabilities_and_hints() -> None:
    discovery = ToolDiscovery()
    candidate = ToolDiscoveryCandidate(
        name="Example",
        category="code",
        source="https://example.com",
        capabilities=("code", "analysis"),
        connection_hints=("api", "browser"),
    )
    payload = discovery.from_candidate(candidate)
    assert payload["capabilities"] == ["code", "analysis"]
    assert payload["connection_hints"] == ["api", "browser"]
    assert payload["state"] == "discovered"


def test_tool_discovery_lifecycle_requires_evidence() -> None:
    discovery = ToolDiscovery()
    candidate = discovery.from_url("https://example.com/tool", category="ai")
    researched = discovery.transition(
        candidate,
        current_state="discovered",
        next_state="researched",
        evidence={"source_checked": True},
    )
    assert researched["state"] == "researched"
    validated = discovery.transition(
        candidate,
        current_state="researched",
        next_state="validated",
        evidence={"contract_checked": True},
    )
    assert validated["state"] == "validated"


def test_tool_discovery_lifecycle_rejects_skipped_gate() -> None:
    discovery = ToolDiscovery()
    candidate = discovery.from_url("https://example.com/tool")
    try:
        discovery.transition(
            candidate,
            current_state="discovered",
            next_state="approved",
            evidence={"ok": True},
        )
    except ValueError:
        return
    assert False, "discovery lifecycle must not skip trust gates"
