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


def test_v3_candidate_maps_to_real_capability_id():
    from types import SimpleNamespace
    from abs_core.v3 import ABSV3Orchestrator, CostClass
    cap=SimpleNamespace(id="local-ai", kind="local_ai", metadata={})
    candidate=ABSV3Orchestrator._candidate.__get__(object.__new__(ABSV3Orchestrator), ABSV3Orchestrator)(cap)
    assert candidate.id=="local-ai"
    assert candidate.cost_class is CostClass.FREE_LOCAL
    assert "chat" in candidate.capabilities


def test_v3_explicit_unknown_capability_is_denied_even_when_critical():
    from abs_core.v3 import ABSV3Orchestrator, WorkDisposition, CapacitySnapshot, CapacityState
    from abs_core.capabilities import CapabilityRegistry
    from abs_core.store import WorkStore
    o=ABSV3Orchestrator(CapabilityRegistry(), WorkStore(":memory:"))
    critical=CapacitySnapshot(3,1.0,1,0,1,CapacityState.CRITICAL,1,0.0)
    o.capacity.admission=lambda priority,depth:(critical,False)
    w=o.create("test", {})
    d=o._gate(w, {"capability_id":"does-not-exist"})
    assert d.disposition is WorkDisposition.DENY


def test_v3_explicit_echo_executes_when_capacity_is_critical():
    from abs_core.runtime import build_runtime
    from abs_core.v3 import CapacitySnapshot, CapacityState
    rt=build_runtime(":memory:")
    critical=CapacitySnapshot(3,1.0,1,0,1,CapacityState.CRITICAL,1,0.0)
    rt.orchestrator.capacity.admission=lambda priority,depth:(critical,False)
    work=rt.orchestrator.create("V3 safe echo under pressure", {"capability_id":"echo"})
    done=rt.orchestrator.run(work.id, "echo")
    assert done.state.value=="completed"


def test_v3_explicit_echo_executes_end_to_end():
    from abs_core.runtime import build_runtime
    rt=build_runtime(":memory:")
    work=rt.orchestrator.create("V3 echo integration", {"capability_id":"echo"})
    done=rt.orchestrator.run(work.id, "echo")
    assert done.state.value=="completed"
    assert done.result["type"]=="v2_result"
    assert done.result["verification"]["accepted"] is True


def test_llama_lifecycle_adapter_calls_load_unload():
    from abs_core.v3 import LlamaCppModelAdapter
    calls=[]
    a=LlamaCppModelAdapter("http://127.0.0.1:8080")
    a._post=lambda path,model: calls.append((path,model)) or {"success":True}
    assert a.load("qwen")["success"] is True
    assert a.unload("qwen")["success"] is True
    assert calls==[("/models/load","qwen"),("/models/unload","qwen")]


def test_operational_intelligence_validates_model_plan():
    from abs_core.operational_intelligence import OperationalIntelligence
    from abs_core.capabilities import CapabilityRegistry, CapabilityRecord
    class FakeAdapter:
        def execute(self, objective, context):
            return {"final_response": '{"understanding":"do echo","mode":"direct","steps":[{"objective":"hello","capability_id":"echo","executor":"direct"}],"success_criteria":["echo completes"],"unknowns":[]}'}
    reg=CapabilityRegistry()
    reg.register(CapabilityRecord("echo","Echo","test",FakeAdapter()))
    reg.register(CapabilityRecord("planner","Planner","external_ai",FakeAdapter(),metadata={"cost_class":"free_external","capabilities":["reasoning"]}))
    oi=OperationalIntelligence(reg, IntelligenceSelector(), CostPolicyEngine())
    plan=oi.plan("do echo",{})
    assert plan.steps[0].capability_id=="echo"
    assert plan.mode=="direct"

def test_operational_intelligence_rejects_unknown_capability():
    from abs_core.operational_intelligence import OperationalIntelligence
    from abs_core.capabilities import CapabilityRegistry, CapabilityRecord
    class FakeAdapter:
        def execute(self, objective, context):
            return {"final_response": '{"understanding":"x","mode":"direct","steps":[{"objective":"x","capability_id":"invented"}]}'}
    reg=CapabilityRegistry()
    reg.register(CapabilityRecord("planner","Planner","external_ai",FakeAdapter(),metadata={"cost_class":"free_external","capabilities":["reasoning"]}))
    oi=OperationalIntelligence(reg, IntelligenceSelector(), CostPolicyEngine())
    plan=oi.plan("x",{})
    assert plan.steps[0].capability_id is None
    assert plan.unknowns

def test_operational_intelligence_executes_integrated_objective():
    from abs_core.operational_intelligence import OperationalIntelligence
    from abs_core.runtime import build_runtime
    rt=build_runtime(":memory:")
    class Planner:
        def execute(self, objective, context):
            return {"final_response": '{"understanding":"echo it","mode":"direct","steps":[{"objective":"V3 operational echo","capability_id":"echo","executor":"direct"}],"success_criteria":["completed"],"unknowns":[]}'}
    rt.registry.register(__import__("abs_core.capabilities",fromlist=["CapabilityRecord"]).CapabilityRecord(
        "planner","Planner","external_ai",Planner(),metadata={"cost_class":"free_external","capabilities":["reasoning"]}))
    rt.intelligence.register(__import__("abs_core.intelligence",fromlist=["IntelligenceResource"]).IntelligenceResource(
        "intelligence:planner","planner","Planner","remote",False,("reasoning",)))
    rt.operational_intelligence = OperationalIntelligence(rt.registry, rt.orchestrator.selector, rt.orchestrator.cost_policy)
    result=rt.operational_intelligence.execute("V3 operational echo",{},rt.orchestrator)
    assert result["completed"] is True
    assert result["steps"][0]["state"]=="completed"

def test_capacity_wait_does_not_leave_phantom_queue_entry():
    from abs_core.runtime import build_runtime
    from abs_core.v3 import CapacitySnapshot, CapacityState

    rt = build_runtime(":memory:")
    critical = CapacitySnapshot(3, 1.0, 1, 0, 1, CapacityState.CRITICAL, 1, 0.0)
    rt.orchestrator.capacity.admission = lambda priority, depth: (critical, False)
    work = rt.orchestrator.create(
        "Defer non-lightweight work while capacity is critical",
        {"capability_id": "internet-http"},
    )

    paused = rt.orchestrator.run(work.id, "internet-http")
    assert paused.state.value == "paused"
    assert paused.context["_v3"]["status"] == "waiting"
    assert paused.context["_v3"]["retryable"] is True
    assert rt.orchestrator.queue.depth() == 0



def test_v3_status_does_not_claim_unverified_local_ai_available():
    from abs_core.v3 import ABSV3Orchestrator
    from abs_core.capabilities import CapabilityRecord, CapabilityRegistry
    from abs_core.store import WorkStore

    registry = CapabilityRegistry()
    registry.register(CapabilityRecord(
        "local-ai:qwen3.5-0.8b",
        "Qwen 0.8B",
        "local_ai",
        object(),
        metadata={
            "cost_class": "free_local",
            "capabilities": ["chat"],
            "capabilities_unverified": ["reasoning", "tools"],
        },
    ))
    orchestrator = ABSV3Orchestrator(registry, WorkStore(":memory:"))
    item = next(x for x in orchestrator.status()["intelligence"] if x["id"] == "local-ai:qwen3.5-0.8b")
    assert item["status"] == "configured"
    assert item["capabilities"] == ["chat"]
    assert item["capabilities_unverified"] == ["reasoning", "tools"]


def _critical_v3_with_local_model():
    from abs_core.v3 import ABSV3Orchestrator
    from abs_core.capabilities import CapabilityRecord, CapabilityRegistry
    from abs_core.store import WorkStore

    registry = CapabilityRegistry()
    registry.register(CapabilityRecord(
        "local-ai:qwen3.5-0.8b",
        "Qwen 0.8B",
        "local_ai",
        object(),
        metadata={
            "cost_class": "free_local",
            "capabilities": ["chat"],
            "estimated_memory_mb": 1800,
        },
    ))
    orchestrator = ABSV3Orchestrator(registry, WorkStore(":memory:"))
    critical = CapacitySnapshot(
        3, 1.1, 100_000_000, 4_200_000_000, 6_100_000_000,
        CapacityState.CRITICAL, 1, 0.0,
    )
    orchestrator.capacity.admission = lambda priority, depth: (critical, False)
    return orchestrator


def test_v3_critical_cpu_pressure_allows_single_local_ai_with_ram_reserve(monkeypatch):
    import io
    from types import SimpleNamespace
    from abs_core.v3 import WorkDisposition

    orchestrator = _critical_v3_with_local_model()
    monkeypatch.setattr(
        "builtins.open",
        lambda *args, **kwargs: io.StringIO("MemAvailable: 4200000 kB\\n"),
    )
    decision = orchestrator._gate(
        SimpleNamespace(),
        {"capability_id": "local-ai:qwen3.5-0.8b"},
    )
    assert decision.disposition is WorkDisposition.EXECUTE
    assert decision.reason == "explicit_intelligence"


def test_v3_critical_cpu_pressure_blocks_local_ai_without_ram_reserve(monkeypatch):
    import io
    from types import SimpleNamespace
    from abs_core.v3 import WorkDisposition

    orchestrator = _critical_v3_with_local_model()
    monkeypatch.setattr(
        "builtins.open",
        lambda *args, **kwargs: io.StringIO("MemAvailable: 2000000 kB\\n"),
    )
    decision = orchestrator._gate(
        SimpleNamespace(),
        {"capability_id": "local-ai:qwen3.5-0.8b"},
    )
    assert decision.disposition is WorkDisposition.WAIT
    assert decision.reason == "capacity_critical"
