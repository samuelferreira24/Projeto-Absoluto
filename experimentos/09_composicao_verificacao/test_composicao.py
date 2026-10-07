from dataclasses import dataclass, field
from typing import Any


@dataclass
class Mission:
    objective: str
    context: dict[str, Any] = field(default_factory=dict)


class CompositionPlanner:
    def plan(self, mission):
        c = mission.context
        steps = []
        if c.get("research_required"):
            steps.append("RESEARCH")
        if c.get("parallelizable") and c.get("independent_parts", 1) > 1:
            steps.append("MULTIAGENT")
        if c.get("defined_steps"):
            steps.append("WORKFLOW")
        if c.get("open_ended"):
            steps.append("AGENT")
        return steps or ["DIRECT"]


class Verifier:
    def verify(self, mission, result):
        # Sandbox contract: executor success is not enough.
        return result.get("status") == "success" and result.get("goal_achieved") is True


def execute_plan(mission, plan, scripted):
    trace = []
    for mode in plan:
        trace.append(mode)
        result = scripted.pop(0)
        if not Verifier().verify(mission, result):
            return trace, "REPLAN_OR_RECOVERY"
    return trace, "COMPLETE"


def test_research_then_parallel():
    m = Mission("research and split", {"research_required": True, "parallelizable": True, "independent_parts": 3})
    plan = CompositionPlanner().plan(m)
    assert plan == ["RESEARCH", "MULTIAGENT"]
    trace, status = execute_plan(m, plan, [
        {"status": "success", "goal_achieved": True},
        {"status": "success", "goal_achieved": True},
    ])
    assert trace == plan and status == "COMPLETE"


def test_workflow_then_agent():
    m = Mission("structured but open", {"defined_steps": True, "open_ended": True})
    plan = CompositionPlanner().plan(m)
    assert plan == ["WORKFLOW", "AGENT"]


def test_false_positive_executor_success():
    m = Mission("real goal")
    trace, status = execute_plan(m, ["DIRECT"], [{"status": "success", "goal_achieved": False}])
    assert trace == ["DIRECT"]
    assert status == "REPLAN_OR_RECOVERY"


def test_composition_can_be_replanned():
    m = Mission("adaptive", {"defined_steps": True})
    plan = CompositionPlanner().plan(m)
    assert plan == ["WORKFLOW"]
    m.context["open_ended"] = True
    replanned = CompositionPlanner().plan(m)
    assert replanned == ["WORKFLOW", "AGENT"]


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-q"]))
