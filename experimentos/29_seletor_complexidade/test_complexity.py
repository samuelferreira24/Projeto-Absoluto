def choose(context):
    if context.get("recovery_required"):
        return "RECOVERY"
    if context.get("authorization_required"):
        return "WAIT_AUTH"
    if context.get("context_incomplete"):
        return "OBSERVE"
    if context.get("parallelizable"):
        return "MULTIAGENT"
    if context.get("open_ended"):
        return "AGENT"
    if context.get("defined_steps"):
        return "WORKFLOW"
    return "DIRECT"


def test_same_objective_simple_context_is_direct():
    assert choose({}) == "DIRECT"


def test_same_objective_open_context_becomes_agent():
    assert choose({"open_ended": True}) == "AGENT"


def test_parallel_context_uses_parallel_mode():
    assert choose({"parallelizable": True}) == "MULTIAGENT"


def test_blocking_context_precedes_execution_mode():
    assert choose({"open_ended": True, "authorization_required": True}) == "WAIT_AUTH"
