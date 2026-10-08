from abs_core.v3 import CapacityGovernor, CapacityState, CostBudget, CostClass, CostPolicy, CostPolicyEngine, IntelligenceCandidate, IntelligenceSelector

def test_free_only_rejects_paid():
    assert not CostPolicyEngine().admissible(IntelligenceCandidate("paid", CostClass.PAID_API, estimated_cost=.01), CostPolicy.FREE_ONLY, CostBudget(10,0))

def test_free_only_accepts_local():
    assert CostPolicyEngine().admissible(IntelligenceCandidate("local", CostClass.FREE_LOCAL, local=True), CostPolicy.FREE_ONLY, CostBudget())

def test_selector_prefers_local():
    r=IntelligenceSelector().rank([
        IntelligenceCandidate("paid", CostClass.PAID_API, estimated_cost=.01),
        IntelligenceCandidate("local", CostClass.FREE_LOCAL, local=True),
        IntelligenceCandidate("free", CostClass.FREE_EXTERNAL),
    ], CostPolicy.PAID_ALLOWED, CostBudget(10,0))
    assert r[0].id=="local"

def test_capacity_snapshot():
    s=CapacityGovernor().snapshot()
    assert s.cpu_count>=1
    assert s.state in {CapacityState.HEALTHY, CapacityState.PRESSURE, CapacityState.CRITICAL}
