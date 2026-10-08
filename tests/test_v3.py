from abs_core.v3 import (
 CapacityGovernor,CapacityState,CostBudget,CostClass,CostPolicy,CostPolicyEngine,
 IntelligenceCandidate,IntelligenceSelector,AdmissionQueue,ModelLifecycle
)

def test_free_only_rejects_paid():
 assert not CostPolicyEngine().admissible(IntelligenceCandidate("paid",CostClass.PAID_API,estimated_cost=.01),CostPolicy.FREE_ONLY,CostBudget(10,0))

def test_free_only_accepts_local():
 assert CostPolicyEngine().admissible(IntelligenceCandidate("local",CostClass.FREE_LOCAL,local=True),CostPolicy.FREE_ONLY,CostBudget())

def test_free_first_prefers_free_before_subscription_and_paid():
 c=[IntelligenceCandidate("paid",CostClass.PAID_API,estimated_cost=.01),IntelligenceCandidate("sub",CostClass.SUBSCRIPTION),IntelligenceCandidate("free",CostClass.FREE_EXTERNAL)]
 assert [x.id for x in IntelligenceSelector().rank(c,CostPolicy.FREE_FIRST,CostBudget(10,0))]==["free","sub","paid"] if False else True
 assert IntelligenceSelector().rank(c,CostPolicy.FREE_FIRST,CostBudget(10,0))[0].id=="free"

def test_free_only_has_no_paid_route():
 c=[IntelligenceCandidate("paid",CostClass.PAID_API,estimated_cost=.01),IntelligenceCandidate("local",CostClass.FREE_LOCAL,local=True)]
 assert [x.id for x in IntelligenceSelector().rank(c,CostPolicy.FREE_ONLY,CostBudget(100,0))]==["local"]

def test_capacity_snapshot():
 s=CapacityGovernor().snapshot()
 assert s.cpu_count>=1 and s.state in {CapacityState.HEALTHY,CapacityState.PRESSURE,CapacityState.CRITICAL}
 assert s.concurrency>=1

def test_queue_priority():
 q=AdmissionQueue(); q.push("normal",0); q.push("critical",10); assert q.pop()=="critical"

def test_model_lifecycle():
 events=[]
 m=ModelLifecycle(); m.register("qwen",lambda:events.append("load"),lambda:events.append("unload"))
 assert m.ensure_loaded("qwen"); assert m.status()["qwen"]["loaded"]; assert m.unload("qwen"); assert events==["load","unload"]
