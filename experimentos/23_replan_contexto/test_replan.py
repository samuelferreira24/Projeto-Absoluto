def plan(context):
    if context.get("context_incomplete"):
        return ("OBSERVE",)
    if context.get("open_ended"):
        return ("AGENT",)
    if context.get("defined_steps"):
        return ("WORKFLOW",)
    return ("DIRECT",)


def test_context_change_invalidates_old_plan():
    before = plan({"defined_steps": True})
    after = plan({"defined_steps": True, "open_ended": True})
    assert before == ("WORKFLOW",)
    assert after == ("AGENT",)
    assert after != before


def test_new_uncertainty_requires_observation():
    before = plan({"defined_steps": True})
    after = plan({"defined_steps": True, "context_incomplete": True})
    assert before == ("WORKFLOW",)
    assert after == ("OBSERVE",)
