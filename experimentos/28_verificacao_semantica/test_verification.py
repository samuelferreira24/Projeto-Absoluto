def verify(execution_status, evidence, criteria):
    if execution_status != "SUCCESS":
        return False
    if not criteria:
        return False
    return all(evidence.get(key) == expected for key, expected in criteria.items())


def test_executor_success_without_goal_evidence_fails():
    assert verify("SUCCESS", {"ran": True}, {"goal_achieved": True}) is False


def test_goal_evidence_can_complete():
    assert verify("SUCCESS", {"goal_achieved": True}, {"goal_achieved": True}) is True


def test_empty_criteria_is_not_verifiable():
    assert verify("SUCCESS", {"anything": True}, {}) is False


def test_failed_execution_never_completes():
    assert verify("FAILED", {"goal_achieved": True}, {"goal_achieved": True}) is False
