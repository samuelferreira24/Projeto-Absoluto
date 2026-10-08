from __future__ import annotations

from abs_core.adapters import EchoCapability
from abs_core.capabilities import CapabilityRecord, CapabilityRegistry
from abs_core.models import WorkState
from abs_core.store import WorkStore
from abs_core.v2 import ABSV2Orchestrator


def registry():
    r = CapabilityRegistry()
    r.register(CapabilityRecord("echo", "Echo", "test", EchoCapability()))
    return r


def test_workflow_mode_executes_all_steps():
    orch = ABSV2Orchestrator(registry(), WorkStore(":memory:"))
    work = orch.create("workflow", {
        "steps": [
            {"objective": "one", "capability_id": "echo"},
            {"objective": "two", "capability_id": "echo"},
        ],
        "workflow": True,
        "approved": True,
    })
    result = orch.run(work.id, approved=True)
    assert result.state == WorkState.COMPLETED
    assert result.result["executor"] == "workflow"
    assert result.result["result"]["type"] == "workflow"
    assert result.result["result"]["count"] == 2


def test_multiagent_mode_has_admission_and_executes_subtasks():
    orch = ABSV2Orchestrator(registry(), WorkStore(":memory:"))
    work = orch.create("multi", {
        "subagents": 2,
        "max_subagents": 2,
        "subtasks": [
            {"objective": "one", "capability_id": "echo"},
            {"objective": "two", "capability_id": "echo"},
        ],
        "approved": True,
    })
    result = orch.run(work.id, approved=True)
    assert result.state == WorkState.COMPLETED
    assert result.result["executor"] == "multiagent"
    assert result.result["result"]["count"] == 2


def test_multiagent_admission_blocks_excess():
    orch = ABSV2Orchestrator(registry(), WorkStore(":memory:"))
    work = orch.create("multi", {
        "subagents": 3,
        "max_subagents": 2,
        "subtasks": ["one", "two", "three"],
        "approved": True,
    })
    result = orch.run(work.id, approved=True)
    assert result.state == WorkState.FAILED
    assert result.result["type"] == "budget_error"
