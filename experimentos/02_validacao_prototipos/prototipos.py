from dataclasses import dataclass, field
from typing import Any


MODES = ("DIRECT", "WORKFLOW", "AGENT", "MULTIAGENT", "RESEARCH", "RECOVERY")
CONTROL = ("OBSERVE", "WAIT_AUTH", "DISCOVER", "BLOCKED", "COMPLETE", "REPLAN")


@dataclass
class Mission:
    objective: str
    context: dict[str, Any] = field(default_factory=dict)
    explicit_modes: list[str] | None = None


@dataclass
class Decision:
    modes: list[str]
    control: str = "EXECUTE"
    reason: str = ""
    complexity: int = 0


@dataclass
class Event:
    kind: str
    data: dict[str, Any] = field(default_factory=dict)


class MoldSelectorA:
    """Prototype A: explicit control state + adaptive mode selection."""

    weights = {"DIRECT": 1, "WORKFLOW": 2, "RESEARCH": 2, "RECOVERY": 2, "AGENT": 3, "MULTIAGENT": 4}

    def choose(self, mission: Mission) -> Decision:
        c = mission.context

        if mission.explicit_modes:
            unknown = [m for m in mission.explicit_modes if m not in MODES]
            if unknown:
                raise ValueError("unknown_mode:" + ",".join(unknown))
            return Decision(list(mission.explicit_modes), reason="imperador_override",
                            complexity=max(self.weights[m] for m in mission.explicit_modes))

        if c.get("recovery_required"):
            return Decision(["RECOVERY"], reason="recovery_required", complexity=2)

        if c.get("authorization_required") and not c.get("authorized"):
            return Decision([], control="WAIT_AUTH", reason="authorization_required")

        if c.get("required_capability_missing"):
            return Decision([], control="DISCOVER", reason="capability_missing")

        if c.get("context_incomplete"):
            return Decision([], control="OBSERVE", reason="insufficient_context")

        candidates = []
        if c.get("research_required") or c.get("high_uncertainty"):
            candidates.append("RESEARCH")
        if c.get("defined_steps"):
            candidates.append("WORKFLOW")
        if c.get("open_ended"):
            candidates.append("AGENT")
        if c.get("parallelizable") and c.get("independent_parts", 1) > 1:
            candidates.append("MULTIAGENT")

        if not candidates:
            candidates = ["DIRECT"]

        forbidden = set(c.get("forbid_modes", []))
        candidates = [m for m in candidates if m not in forbidden]

        max_complexity = c.get("max_complexity")
        if max_complexity is not None:
            candidates = [m for m in candidates if self.weights[m] <= max_complexity]

        if not candidates:
            return Decision([], control="BLOCKED", reason="no_feasible_mode")

        return Decision(candidates, reason="criteria_composition",
                        complexity=max(self.weights[m] for m in candidates))


class ControllerA:
    def __init__(self):
        self.selector = MoldSelectorA()

    def step(self, mission: Mission, event: Event | None = None) -> Decision:
        c = dict(mission.context)
        if event:
            c.update(event.data)
            if event.kind in {"executor_failed", "verification_failed"}:
                c["recovery_required"] = True
            if event.kind == "state_changed":
                return Decision([], control="REPLAN", reason="state_changed")
            if event.kind == "goal_verified":
                return Decision([], control="COMPLETE", reason="goal_verified")
        return self.selector.choose(Mission(mission.objective, c, mission.explicit_modes))


@dataclass
class Node:
    name: str
    kind: str
    next_on_success: str | None = None
    next_on_failure: str | None = None


class MoldGraphB:
    """Prototype B: executable mold graph with state-driven transitions."""

    def __init__(self):
        self.nodes = {
            "DIRECT": Node("DIRECT", "mode"),
            "WORKFLOW": Node("WORKFLOW", "mode"),
            "AGENT": Node("AGENT", "mode"),
            "MULTIAGENT": Node("MULTIAGENT", "mode"),
            "RESEARCH": Node("RESEARCH", "mode"),
            "RECOVERY": Node("RECOVERY", "mode"),
            "OBSERVE": Node("OBSERVE", "control"),
            "WAIT_AUTH": Node("WAIT_AUTH", "control"),
            "DISCOVER": Node("DISCOVER", "control"),
            "BLOCKED": Node("BLOCKED", "control"),
            "COMPLETE": Node("COMPLETE", "terminal"),
        }

    def plan(self, mission: Mission) -> list[str]:
        c = mission.context

        if mission.explicit_modes:
            for mode in mission.explicit_modes:
                if mode not in self.nodes or self.nodes[mode].kind != "mode":
                    raise ValueError("unknown_mode:" + mode)
            return list(mission.explicit_modes)

        if c.get("recovery_required"):
            return ["RECOVERY"]
        if c.get("authorization_required") and not c.get("authorized"):
            return ["WAIT_AUTH"]
        if c.get("required_capability_missing"):
            return ["DISCOVER"]
        if c.get("context_incomplete"):
            return ["OBSERVE"]

        modes = []
        if c.get("research_required") or c.get("high_uncertainty"):
            modes.append("RESEARCH")
        if c.get("defined_steps"):
            modes.append("WORKFLOW")
        if c.get("open_ended"):
            modes.append("AGENT")
        if c.get("parallelizable") and c.get("independent_parts", 1) > 1:
            modes.append("MULTIAGENT")
        if not modes:
            modes = ["DIRECT"]

        forbidden = set(c.get("forbid_modes", []))
        modes = [m for m in modes if m not in forbidden]
        if not modes:
            return ["BLOCKED"]

        max_complexity = c.get("max_complexity")
        weights = {"DIRECT":1, "WORKFLOW":2, "RESEARCH":2, "AGENT":3, "MULTIAGENT":4}
        if max_complexity is not None:
            modes = [m for m in modes if weights[m] <= max_complexity]
        return modes or ["BLOCKED"]

    def transition(self, plan: list[str], event: Event) -> list[str]:
        if event.kind == "goal_verified":
            return ["COMPLETE"]
        if event.kind in {"executor_failed", "verification_failed"}:
            return ["RECOVERY"]
        if event.kind == "state_changed":
            return ["OBSERVE"]
        return plan


def check(name, actual, expected):
    assert actual == expected, f"{name}: expected {expected!r}, got {actual!r}"


def run_suite():
    a = ControllerA()
    b = MoldGraphB()

    cases = [
        ("simple", Mission("known datum"), ["DIRECT"], "EXECUTE"),
        ("workflow", Mission("migration", {"defined_steps": True}), ["WORKFLOW"], "EXECUTE"),
        ("agent", Mission("unknown problem", {"open_ended": True}), ["AGENT"], "EXECUTE"),
        ("multiagent", Mission("parallel", {"parallelizable": True, "independent_parts": 3}), ["MULTIAGENT"], "EXECUTE"),
        ("research+parallel", Mission("research", {"high_uncertainty": True, "parallelizable": True, "independent_parts": 3}), ["RESEARCH", "MULTIAGENT"], "EXECUTE"),
        ("workflow+agent", Mission("adaptive workflow", {"defined_steps": True, "open_ended": True}), ["WORKFLOW", "AGENT"], "EXECUTE"),
        ("incomplete", Mission("ambiguous", {"context_incomplete": True}), [], "OBSERVE"),
        ("authorization", Mission("deploy", {"authorization_required": True}), [], "WAIT_AUTH"),
        ("missing capability", Mission("new operation", {"required_capability_missing": True}), [], "DISCOVER"),
        ("impossible after AV", Mission("parallel", {"parallelizable": True, "independent_parts": 4, "forbid_modes": ["MULTIAGENT"], "max_complexity": 1}), [], "BLOCKED"),
    ]

    for name, mission, expected_modes, expected_control in cases:
        da = a.step(mission)
        check("A/" + name + "/modes", da.modes, expected_modes)
        check("A/" + name + "/control", da.control, expected_control)

        pb = b.plan(mission)
        expected_b = expected_modes if expected_control == "EXECUTE" else [expected_control]
        check("B/" + name, pb, expected_b)

    base = Mission("adaptive", {"defined_steps": True})
    check("A/state-change", a.step(base, Event("state_changed")).control, "REPLAN")
    check("A/failure", a.step(base, Event("executor_failed")).modes, ["RECOVERY"])
    check("A/verification", a.step(base, Event("verification_failed")).modes, ["RECOVERY"])
    check("A/success", a.step(base, Event("goal_verified")).control, "COMPLETE")

    pb = b.plan(base)
    check("B/state-change", b.transition(pb, Event("state_changed")), ["OBSERVE"])
    check("B/failure", b.transition(pb, Event("executor_failed")), ["RECOVERY"])
    check("B/verification", b.transition(pb, Event("verification_failed")), ["RECOVERY"])
    check("B/success", b.transition(pb, Event("goal_verified")), ["COMPLETE"])

    check("A/resource-independence",
          a.step(Mission("x", {"resource": "phone"})).modes,
          a.step(Mission("x", {"resource": "vps"})).modes)
    check("B/resource-independence",
          b.plan(Mission("x", {"resource": "phone"})),
          b.plan(Mission("x", {"resource": "vps"})))

    check("A/override", a.step(Mission("x", explicit_modes=["AGENT"])).modes, ["AGENT"])
    check("B/override", b.plan(Mission("x", explicit_modes=["RESEARCH", "WORKFLOW"])), ["RESEARCH", "WORKFLOW"])

    print("EXPERIMENTO_02: PASS")
    print("Protótipo A: PASS")
    print("Protótipo B: PASS")
    print("Casos de missão:", len(cases))
    print("Transições adicionais: 4 por protótipo")
    print("Invariantes de recurso/override: PASS")


if __name__ == "__main__":
    run_suite()
