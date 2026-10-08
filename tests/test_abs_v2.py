from __future__ import annotations

from abs_core.adapters import EchoCapability
from abs_core.capabilities import CapabilityRecord, CapabilityRegistry
from abs_core.models import WorkState
from abs_core.store import WorkStore
from abs_core.v2 import ABSV2Orchestrator, V2Mode, PolicyEngine


def build():
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("echo", "Echo", "test", EchoCapability()))
    return registry


def test_v2_direct_path_is_verified():
    registry = build()
    store = WorkStore(":memory:")
    orch = ABSV2Orchestrator(registry, store)
    work = orch.create("hello", {"capability_id": "echo"})
    result = orch.run(work.id, approved=True)
    assert result.state == WorkState.COMPLETED
    assert result.context["_v2"]["status"] == "verified"
    assert result.result["verification"]["accepted"] is True
    assert result.result["mode"] == V2Mode.DIRECT.value


def test_v2_unknown_never_becomes_success():
    class Bad:
        id = "bad"
        name = "Bad"
        def execute(self, objective, context):
            return {"type": "error", "error": "nope"}

    registry = build()
    registry.register(CapabilityRecord("bad", "Bad", "external", Bad()))
    orch = ABSV2Orchestrator(registry, WorkStore(":memory:"))
    work = orch.create("bad", {"capability_id": "bad", "max_attempts": 1})
    result = orch.run(work.id, approved=True)
    assert result.state == WorkState.FAILED
    assert result.result["type"] == "v2_failure"


def test_v2_idempotency_replays_completed_result():
    registry = build()
    orch = ABSV2Orchestrator(registry, WorkStore(":memory:"))
    first = orch.create("same", {"capability_id": "echo", "idempotency_key": "k1"})
    first = orch.run(first.id, approved=True)
    second = orch.create("same", {"capability_id": "echo", "idempotency_key": "k1"})
    second = orch.run(second.id, approved=True)
    assert second.state == WorkState.COMPLETED
    assert second.result == first.result


def test_v2_high_risk_waits_for_approval():
    registry = build()
    orch = ABSV2Orchestrator(registry, WorkStore(":memory:"))
    work = orch.create("delete production data", {"capability_id": "echo", "risk": "critical"})
    result = orch.run(work.id, approved=False)
    assert result.state == WorkState.PAUSED
    assert result.context["_v2"]["status"] == "waiting_approval"


def test_v2_policy_blocks_non_imperator_authority():
    registry = build()
    orch = ABSV2Orchestrator(registry, WorkStore(":memory:"))
    work = orch.create("x", {"capability_id": "echo", "authority_actor": "agent"})
    result = orch.run(work.id, approved=True)
    assert result.state == WorkState.FAILED
    assert "authority" in result.result["error"]
