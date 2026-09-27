def resolve(required, available):
    missing = [cap for cap in required if cap not in available]
    if missing:
        return "DISCOVER"
    return "EXECUTE"


def test_missing_capability_triggers_discovery():
    assert resolve(["reasoning"], {"execute"}) == "DISCOVER"


def test_available_capability_allows_execution():
    assert resolve(["execute"], {"execute", "reasoning"}) == "EXECUTE"


def test_discovery_does_not_change_required_capability():
    required = ["reasoning"]
    assert resolve(required, {"execute"}) == "DISCOVER"
    assert required == ["reasoning"]
