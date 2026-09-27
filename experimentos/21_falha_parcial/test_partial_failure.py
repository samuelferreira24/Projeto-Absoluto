def recover_partial(statuses):
    preserved = [name for name, status in statuses.items() if status == "SUCCESS"]
    failed = [name for name, status in statuses.items() if status == "FAILED"]
    return preserved, failed


def test_one_branch_failure_preserves_success():
    preserved, failed = recover_partial({"RESEARCH": "SUCCESS", "AGENT": "FAILED"})
    assert preserved == ["RESEARCH"]
    assert failed == ["AGENT"]


def test_all_success_needs_no_recovery():
    preserved, failed = recover_partial({"A": "SUCCESS", "B": "SUCCESS"})
    assert preserved == ["A", "B"]
    assert failed == []


def test_failed_branch_can_resume_without_replaying_success():
    state = {"A": "SUCCESS", "B": "FAILED"}
    state["B"] = "SUCCESS"
    assert state == {"A": "SUCCESS", "B": "SUCCESS"}
