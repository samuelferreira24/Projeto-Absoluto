from __future__ import annotations

from threading import RLock

from abs_core.models import Work, WorkState
from abs_core.v3 import (
    ABSV3Orchestrator,
    CapacitySnapshot,
    CapacityState,
    CostClass,
    CostPolicy,
    V3Decision,
    WorkDisposition,
)


class FakeStore:
    def __init__(self, work):
        self.work = work

    def load(self, work_id):
        return self.work

    def save(self, work):
        self.work = work


class FakeState:
    def __init__(self):
        self.events = []
        self.learned = []

    def event(self, *args):
        self.events.append(args)

    def cost(self, *args, **kwargs):
        pass

    def learn(self, *args):
        self.learned.append(args)


class FakeTelemetry:
    def inc(self, *args, **kwargs):
        pass

    def observe(self, *args, **kwargs):
        pass


def _decision(candidate_id: str) -> V3Decision:
    return V3Decision(
        WorkDisposition.EXECUTE,
        candidate_id,
        CostClass.FREE_EXTERNAL,
        "test",
        CapacitySnapshot(1, 0.1, 0, 1, 2, CapacityState.HEALTHY, 2, 0.0),
        CostPolicy.FREE_FIRST,
    )


def test_v3_replans_after_verified_failure(monkeypatch):
    work = Work("objective", {"max_replans": 1})
    store = FakeStore(work)
    state = FakeState()

    runtime = ABSV3Orchestrator.__new__(ABSV3Orchestrator)
    runtime.store = store
    runtime.v3_state = state
    runtime.telemetry = FakeTelemetry()
    runtime._v3_lock = RLock()
    runtime._active = 0
    runtime._tickets = {}
    runtime._ticket_seq = 0
    runtime.capacity = type("Capacity", (), {"admission": lambda *_: (
        CapacitySnapshot(1, 0.1, 0, 1, 2, CapacityState.HEALTHY, 2, 0.0), True
    )})()
    runtime.cost_policy = type("Policy", (), {
        "policy": lambda *_: CostPolicy.FREE_FIRST,
    })()
    runtime.queue = type("Queue", (), {"depth": lambda *_: 0, "push": lambda *_: None})()
    runtime.selector = type("Selector", (), {"learning": {}})()

    runtime._acquire_slot = lambda *args: None
    runtime._release_slot = lambda *args: None
    runtime._gate = lambda *args: _decision("first")
    runtime._rerank_with_learning = lambda: None
    runtime._replan_candidates = lambda work, context, failed: [
        type("Candidate", (), {"id": "second"})()
    ] if failed == "first" else []
    runtime._candidate = lambda cap: None

    calls = []

    def fake_v2_run(self, work_id, capability_id=None, approved=False):
        calls.append(capability_id)
        if len(calls) == 1:
            work.state = WorkState.FAILED
            work.result = {"type": "error", "error": "verification_failed"}
        else:
            work.state = WorkState.COMPLETED
            work.result = {"final_response": "recovered"}
        return work

    monkeypatch.setattr("abs_core.v2.ABSV2Orchestrator.run", fake_v2_run)

    result = runtime.run(work.id, approved=True)

    assert result.state is WorkState.COMPLETED
    assert calls == ["first", "second"]
    assert state.learned[0][0] == "first"
    assert state.learned[0][1] is False
    assert any(event[1] == "verification_failure" for event in state.events)
    assert work.context["_v3"]["replanned_from"] == "first"
    assert work.context["_v3"]["selected_intelligence"] == "second"


def test_v3_can_resume_persisted_failed_work(monkeypatch):
    work = Work("retry me", {"max_replans": 0})
    store = FakeStore(work)
    state = FakeState()

    runtime = ABSV3Orchestrator.__new__(ABSV3Orchestrator)
    runtime.store = store
    runtime.v3_state = state
    runtime.telemetry = FakeTelemetry()
    runtime._v3_lock = RLock()
    runtime._active = 0
    runtime._tickets = {}
    runtime._ticket_seq = 0
    runtime.capacity = type("Capacity", (), {"admission": lambda *_: (
        CapacitySnapshot(1, 0.1, 0, 1, 2, CapacityState.HEALTHY, 2, 0.0), True
    )})()
    runtime.cost_policy = type("Policy", (), {
        "policy": lambda *_: CostPolicy.FREE_FIRST,
    })()
    runtime.queue = type("Queue", (), {"depth": lambda *_: 0, "push": lambda *_: None})()
    runtime.selector = type("Selector", (), {"learning": {}})()
    runtime._acquire_slot = lambda *args: None
    runtime._release_slot = lambda *args: None
    runtime._gate = lambda *args: _decision("first")
    runtime._rerank_with_learning = lambda: None
    runtime._replan_candidates = lambda *args: []
    runtime._candidate = lambda cap: None

    calls = []
    def fake_v2_run(self, work_id, capability_id=None, approved=False):
        calls.append(capability_id)
        if len(calls) == 1:
            work.state = WorkState.FAILED
            work.result = {"type": "error", "error": "persisted_failure"}
        else:
            work.state = WorkState.COMPLETED
            work.result = {"final_response": "recovered_on_resume"}
        return work

    monkeypatch.setattr("abs_core.v2.ABSV2Orchestrator.run", fake_v2_run)

    first = runtime.run(work.id, approved=True)
    assert first.state is WorkState.FAILED
    assert first.result["error"] == "persisted_failure"

    second = runtime.run(work.id, approved=True)
    assert second.state is WorkState.COMPLETED
    assert second.result["final_response"] == "recovered_on_resume"
    assert calls == ["first", "first"]
