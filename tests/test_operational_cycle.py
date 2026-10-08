from types import SimpleNamespace

from abs_core.operational_intelligence import OperationalIntelligence, OperationalPlan, OperationalStep


class _DummyOrchestrator:
    def __init__(self):
        self.calls = 0

    def create(self, objective, context):
        return SimpleNamespace(id=f"w{self.calls + 1}", objective=objective, context=context)

    def run(self, work_id, capability_id=None, approved=False):
        self.calls += 1
        if self.calls == 1:
            return SimpleNamespace(
                id=work_id,
                state=SimpleNamespace(value="failed"),
                capability_id=capability_id,
                result={"type": "error", "error": "first_executor_failed"},
            )
        return SimpleNamespace(
            id=work_id,
            state=SimpleNamespace(value="completed"),
            capability_id=capability_id,
            result={"type": "ok", "final_response": "recovered"},
        )


def _engine():
    engine = OperationalIntelligence(
        registry=SimpleNamespace(),
        selector=SimpleNamespace(),
        cost_policy=SimpleNamespace(),
    )
    plans = iter([
        OperationalPlan(
            objective="do it",
            understanding="first strategy",
            mode="direct",
            steps=(OperationalStep("attempt one", capability_id="a"),),
        ),
        OperationalPlan(
            objective="do it",
            understanding="replanned strategy",
            mode="direct",
            steps=(OperationalStep("attempt two", capability_id="b"),),
        ),
    ])
    engine.plan = lambda objective, context: next(plans)
    return engine


def test_operational_cycle_replans_after_verified_failure():
    engine = _engine()
    orchestrator = _DummyOrchestrator()

    result = engine.execute("do it", {"max_replans": 1}, orchestrator)

    assert result["completed"] is True
    assert len(result["cycles"]) == 2
    assert result["cycles"][0]["failed_step"] == 1
    assert result["cycles"][1]["failed_step"] is None
    assert orchestrator.calls == 2
    assert result["cycles"][1]["plan"]["understanding"] == "replanned strategy"
