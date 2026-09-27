from dataclasses import dataclass, field
from typing import Any


@dataclass
class Mission:
    objective: str
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionResult:
    status: str
    evidence: dict[str, Any] = field(default_factory=dict)


class ScriptedExecutor:
    """Deterministic sandbox executor; no external side effects."""

    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = []

    def execute(self, mode, mission):
        self.calls.append(mode)
        outcome = self.outcomes.pop(0) if self.outcomes else "success"
        if outcome == "success":
            return ExecutionResult("success", {"mode": mode})
        if outcome == "failure":
            return ExecutionResult("failure", {"error": "executor_failed", "mode": mode})
        if outcome == "verification_failure":
            return ExecutionResult("verification_failure", {"mode": mode})
        if outcome == "state_changed":
            mission.context["open_ended"] = True
            return ExecutionResult("state_changed", {"mode": mode})
        if outcome == "capability_missing":
            mission.context["required_capability_missing"] = True
            return ExecutionResult("capability_missing", {"mode": mode})
        if outcome == "authorization":
            mission.context["authorization_required"] = True
            mission.context["authorized"] = False
            return ExecutionResult("authorization", {"mode": mode})
        raise ValueError(outcome)


class CandidateA:
    """State-controller implementation."""

    def choose(self, mission):
        c = mission.context
        if c.get("recovery_required"):
            return "RECOVERY"
        if c.get("authorization_required") and not c.get("authorized"):
            return "WAIT_AUTH"
        if c.get("required_capability_missing"):
            return "DISCOVER"
        if c.get("context_incomplete"):
            return "OBSERVE"
        if c.get("research_required") or c.get("high_uncertainty"):
            return "RESEARCH"
        if c.get("parallelizable") and c.get("independent_parts", 1) > 1:
            return "MULTIAGENT"
        if c.get("open_ended"):
            return "AGENT"
        if c.get("defined_steps"):
            return "WORKFLOW"
        return "DIRECT"

    def run(self, mission, executor, max_steps=12):
        trace = []
        for _ in range(max_steps):
            mode = self.choose(mission)
            trace.append(mode)
            if mode == "WAIT_AUTH":
                if mission.context.get("grant_authorization"):
                    mission.context["authorized"] = True
                    mission.context["authorization_required"] = False
                    continue
                return trace, "WAIT_AUTH"
            if mode == "DISCOVER":
                mission.context["required_capability_missing"] = False
                mission.context["capability_acquired"] = True
                continue
            if mode == "OBSERVE":
                mission.context["context_incomplete"] = False
                mission.context["observed"] = True
                continue
            result = executor.execute(mode, mission)
            if result.status == "success":
                return trace, "COMPLETE"
            if result.status in {"failure", "verification_failure"}:
                mission.context["recovery_required"] = True
                continue
            if result.status == "state_changed":
                continue
            if result.status == "capability_missing":
                continue
            if result.status == "authorization":
                continue
        return trace, "BLOCKED"


class CandidateB:
    """Graph-like transition implementation."""

    def next_mode(self, mission, previous=None):
        c = mission.context
        if c.get("recovery_required"):
            return "RECOVERY"
        if c.get("authorization_required") and not c.get("authorized"):
            return "WAIT_AUTH"
        if c.get("required_capability_missing"):
            return "DISCOVER"
        if c.get("context_incomplete"):
            return "OBSERVE"
        if c.get("research_required") or c.get("high_uncertainty"):
            return "RESEARCH"
        if c.get("parallelizable") and c.get("independent_parts", 1) > 1:
            return "MULTIAGENT"
        if c.get("open_ended"):
            return "AGENT"
        if c.get("defined_steps"):
            return "WORKFLOW"
        return "DIRECT"

    def run(self, mission, executor, max_steps=12):
        trace = []
        previous = None
        for _ in range(max_steps):
            mode = self.next_mode(mission, previous)
            trace.append(mode)
            if mode == "WAIT_AUTH":
                if mission.context.get("grant_authorization"):
                    mission.context["authorized"] = True
                    mission.context["authorization_required"] = False
                    previous = mode
                    continue
                return trace, "WAIT_AUTH"
            if mode == "DISCOVER":
                mission.context["required_capability_missing"] = False
                mission.context["capability_acquired"] = True
                previous = mode
                continue
            if mode == "OBSERVE":
                mission.context["context_incomplete"] = False
                mission.context["observed"] = True
                previous = mode
                continue
            result = executor.execute(mode, mission)
            if result.status == "success":
                return trace, "COMPLETE"
            if result.status in {"failure", "verification_failure"}:
                mission.context["recovery_required"] = True
            elif result.status == "state_changed":
                pass
            elif result.status in {"capability_missing", "authorization"}:
                pass
            previous = mode
        return trace, "BLOCKED"


def assert_same(name, a, b):
    assert a == b, f"{name}: {a!r} != {b!r}"


def run():
    scenarios = [
        ("simple", Mission("simple"), ["success"], "COMPLETE"),
        ("failure recovery", Mission("x"), ["failure", "success"], "COMPLETE"),
        ("verification recovery", Mission("x"), ["verification_failure", "success"], "COMPLETE"),
        ("state change", Mission("x", {"defined_steps": True}), ["state_changed", "success"], "COMPLETE"),
        ("capability discovery", Mission("x", {"required_capability_missing": True}), ["success"], "COMPLETE"),
        ("authorization", Mission("x", {"authorization_required": True, "grant_authorization": True}), ["success"], "COMPLETE"),
        ("research", Mission("x", {"high_uncertainty": True}), ["success"], "COMPLETE"),
        ("parallel", Mission("x", {"parallelizable": True, "independent_parts": 3}), ["success"], "COMPLETE"),
    ]

    for name, mission, outcomes, expected in scenarios:
        a = CandidateA()
        b = CandidateB()
        ta, sa = a.run(Mission(mission.objective, dict(mission.context)), ScriptedExecutor(outcomes.copy()))
        tb, sb = b.run(Mission(mission.objective, dict(mission.context)), ScriptedExecutor(outcomes.copy()))
        assert_same(name + "/status", sa, expected)
        assert_same(name + "/status-b", sb, expected)
        assert ta and tb

    # Both implementations must keep a recovery transition after failure.
    a = CandidateA()
    trace, status = a.run(Mission("x"), ScriptedExecutor(["failure", "success"]))
    assert trace[:2] == ["DIRECT", "RECOVERY"]
    assert status == "COMPLETE"

    b = CandidateB()
    trace, status = b.run(Mission("x"), ScriptedExecutor(["failure", "success"]))
    assert trace[:2] == ["DIRECT", "RECOVERY"]
    assert status == "COMPLETE"

    print("EXPERIMENTO_06: PASS")
    print("Protótipo executável A: PASS")
    print("Protótipo executável B: PASS")
    print("Cenários executados:", len(scenarios))


if __name__ == "__main__":
    run()
