MODES = ("DIRECT", "WORKFLOW", "RESEARCH", "AGENT", "MULTIAGENT", "RECOVERY")


def transition(mode, failure):
    if failure == "capability_missing":
        return "DISCOVER"
    if failure == "resource_unavailable":
        return "RESOURCE_UNAVAILABLE"
    if failure in ("executor_failure", "verification_failure"):
        return "RECOVERY"
    return mode


def test_failure_matrix_has_explicit_transitions():
    for mode in MODES:
        assert transition(mode, "capability_missing") == "DISCOVER"
        assert transition(mode, "resource_unavailable") == "RESOURCE_UNAVAILABLE"
        assert transition(mode, "executor_failure") == "RECOVERY"
        assert transition(mode, "verification_failure") == "RECOVERY"


def test_failures_never_silently_become_direct():
    for mode in MODES:
        for failure in ("capability_missing", "resource_unavailable", "executor_failure", "verification_failure"):
            assert transition(mode, failure) != "DIRECT"
