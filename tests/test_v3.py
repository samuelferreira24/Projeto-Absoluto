from abs_core.v3 import (
 CapacityGovernor, CapacityState, CostBudget, CostClass, CostPolicy, CostPolicyEngine,
 IntelligenceCandidate, IntelligenceSelector, AdmissionQueue, ModelLifecycle, V3StateStore
)

def test_free_only_rejects_paid():
    c=IntelligenceCandidate("paid",CostClass.PAID_API,estimated_cost=.01)
    assert not CostPolicyEngine().admissible(c,CostPolicy.FREE_ONLY,CostBudget(10,0))

def test_paid_requires_explicit_policy_and_known_cost():
    e=CostPolicyEngine()
    assert not e.admissible(IntelligenceCandidate("unknown",CostClass.PAID_API,estimated_cost=0),CostPolicy.PAID_ALLOWED,CostBudget(10,0))
    assert e.admissible(IntelligenceCandidate("paid",CostClass.PAID_API,estimated_cost=.01),CostPolicy.PAID_ALLOWED,CostBudget(10,0))
    assert not e.admissible(IntelligenceCandidate("paid",CostClass.PAID_API,estimated_cost=11),CostPolicy.PAID_ALLOWED,CostBudget(10,0))

def test_free_only_accepts_local():
    assert CostPolicyEngine().admissible(IntelligenceCandidate("local",CostClass.FREE_LOCAL,local=True),CostPolicy.FREE_ONLY,CostBudget())

def test_free_first_prefers_free():
    c=[IntelligenceCandidate("paid",CostClass.PAID_API,estimated_cost=.01),IntelligenceCandidate("sub",CostClass.SUBSCRIPTION),IntelligenceCandidate("free",CostClass.FREE_EXTERNAL)]
    assert IntelligenceSelector().rank(c,CostPolicy.FREE_FIRST,CostBudget(10,0))[0].id=="free"

def test_free_only_has_no_paid_route():
    c=[IntelligenceCandidate("paid",CostClass.PAID_API,estimated_cost=.01),IntelligenceCandidate("local",CostClass.FREE_LOCAL,local=True)]
    assert [x.id for x in IntelligenceSelector().rank(c,CostPolicy.FREE_ONLY,CostBudget(100,0))]==["local"]

def test_learning_changes_reliability_rank():
    c=[IntelligenceCandidate("a",CostClass.FREE_EXTERNAL,quality=.5),IntelligenceCandidate("b",CostClass.FREE_EXTERNAL,quality=.5)]
    s=IntelligenceSelector({"a":{"successes":0,"failures":5},"b":{"successes":5,"failures":0}})
    assert s.rank(c,CostPolicy.FREE_FIRST,CostBudget())[0].id=="b"

def test_capacity_snapshot():
    s=CapacityGovernor().snapshot()
    assert s.cpu_count>=1 and s.state in {CapacityState.HEALTHY,CapacityState.PRESSURE,CapacityState.CRITICAL}
    assert s.concurrency>=1

def test_queue_priority():
    q=AdmissionQueue(); q.push("normal",0); q.push("critical",10)
    assert q.pop()=="critical"

def test_model_lifecycle():
    events=[]; m=ModelLifecycle()
    m.register("qwen",lambda:events.append("load"),lambda:events.append("unload"))
    assert m.ensure_loaded("qwen"); assert m.status()["qwen"]["loaded"]
    assert m.unload("qwen"); assert events==["load","unload"]

def test_state_store_learning(tmp_path):
    db=V3StateStore(str(tmp_path/"v3.db"))
    db.learn("local",True,.5); db.learn("local",False,1.5)
    x=db.learning("local")
    assert x["attempts"]==2 and x["successes"]==1 and x["failures"]==1
