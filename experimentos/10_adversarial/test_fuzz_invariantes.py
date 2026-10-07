import random

MODES = {"DIRECT", "WORKFLOW", "RESEARCH", "AGENT", "MULTIAGENT", "RECOVERY"}

def choose(c):
    if c.get("recovery_required"): return "RECOVERY"
    if c.get("authorization_required") and not c.get("authorized"): return "WAIT_AUTH"
    if c.get("required_capability_missing"): return "DISCOVER"
    if c.get("context_incomplete"): return "OBSERVE"
    if c.get("research_required") or c.get("high_uncertainty"): return "RESEARCH"
    if c.get("parallelizable") and c.get("independent_parts", 1) > 1: return "MULTIAGENT"
    if c.get("open_ended"): return "AGENT"
    if c.get("defined_steps"): return "WORKFLOW"
    return "DIRECT"

def test_random_invariants():
    rng = random.Random(20260927)
    keys = [
        "recovery_required","authorization_required","authorized",
        "required_capability_missing","context_incomplete","research_required",
        "high_uncertainty","parallelizable","open_ended","defined_steps",
    ]
    for _ in range(5000):
        c = {k: bool(rng.getrandbits(1)) for k in keys}
        c["independent_parts"] = rng.randint(0, 8)
        mode = choose(c)
        if c["recovery_required"]:
            assert mode == "RECOVERY"
        elif c["authorization_required"] and not c["authorized"]:
            assert mode == "WAIT_AUTH"
        elif c["required_capability_missing"]:
            assert mode == "DISCOVER"
        elif c["context_incomplete"]:
            assert mode == "OBSERVE"
        else:
            assert mode in MODES

if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-q"]))
