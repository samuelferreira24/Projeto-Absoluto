def verify_goal(executor_status, evidence, criteria):
    if executor_status != "success":
        return False
    if not criteria:
        return False
    return all(evidence.get(k) == v for k, v in criteria.items())


def test_executor_success_is_not_goal_success():
    assert verify_goal("success", {"action_done": True, "goal_achieved": False}, {"goal_achieved": True}) is False


def test_explicit_success_criteria():
    assert verify_goal("success", {"goal_achieved": True}, {"goal_achieved": True}) is True


def test_ambiguous_goal_requires_criteria():
    assert verify_goal("success", {"action_done": True}, {}) is False
