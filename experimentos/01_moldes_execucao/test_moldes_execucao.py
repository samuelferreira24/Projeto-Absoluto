from dataclasses import dataclass, field
from typing import Any


MOLDS = (
    "DIRECT",
    "WORKFLOW",
    "AGENT",
    "MULTIAGENT",
    "RESEARCH",
    "RECOVERY",
)


@dataclass
class Mission:
    objective: str
    context: dict[str, Any] = field(default_factory=dict)
    explicit_mold: str | None = None


@dataclass
class Decision:
    molds: list[str]
    complexity: int
    reason: str
    switched: bool = False


class MoldSelector:
    """Experimental selector. It is deliberately small and inspectable."""

    def choose(self, mission: Mission) -> Decision:
        if mission.explicit_mold:
            if mission.explicit_mold not in MOLDS:
                raise ValueError(f"unknown_mold:{mission.explicit_mold}")
            return Decision(
                molds=[mission.explicit_mold],
                complexity=self._complexity(mission.explicit_mold),
                reason="imperador_override",
            )

        ctx = mission.context

        if ctx.get("recovery_required"):
            return Decision(["RECOVERY"], 2, "state_requires_recovery")

        if ctx.get("research_required") or ctx.get("high_uncertainty"):
            return Decision(["RESEARCH"], 2, "uncertainty_or_research_requirement")

        if ctx.get("parallelizable") and ctx.get("independent_parts", 1) > 1:
            return Decision(["MULTIAGENT"], 4, "independent_parallel_parts")

        if ctx.get("defined_steps"):
            return Decision(["WORKFLOW"], 2, "defined_sequence")

        if ctx.get("open_ended"):
            return Decision(["AGENT"], 3, "open_ended_reasoning")

        return Decision(["DIRECT"], 1, "minimum_sufficient_execution")

    @staticmethod
    def _complexity(mold: str) -> int:
        return {
            "DIRECT": 1,
            "WORKFLOW": 2,
            "AGENT": 3,
            "MULTIAGENT": 4,
            "RESEARCH": 2,
            "RECOVERY": 2,
        }[mold]


def compose(*molds: str) -> Decision:
    for mold in molds:
        if mold not in MOLDS:
            raise ValueError(f"unknown_mold:{mold}")
    return Decision(list(molds), max(MoldSelector._complexity(m) for m in molds), "explicit_composition")


def switch_after_failure(previous: Decision, context: dict[str, Any]) -> Decision:
    next_mission = Mission("continue mission", context=context)
    decision = MoldSelector().choose(next_mission)
    decision.switched = decision.molds != previous.molds
    return decision


def assert_case(name: str, actual: Any, expected: Any) -> None:
    if actual != expected:
        raise AssertionError(f"{name}: expected {expected!r}, got {actual!r}")


def run():
    selector = MoldSelector()

    # 1. Simple objective: do not activate unnecessary machinery.
    d = selector.choose(Mission("return a known value"))
    assert_case("simple/direct", d.molds, ["DIRECT"])
    assert_case("simple/minimum complexity", d.complexity, 1)

    # 2. Structured objective: workflow.
    d = selector.choose(Mission("perform migration", {"defined_steps": True}))
    assert_case("structured/workflow", d.molds, ["WORKFLOW"])

    # 3. Open-ended objective: agent.
    d = selector.choose(Mission("solve an unfamiliar problem", {"open_ended": True}))
    assert_case("open/agent", d.molds, ["AGENT"])

    # 4. Independent parallel work: multiagent.
    d = selector.choose(Mission(
        "analyze independent domains",
        {"parallelizable": True, "independent_parts": 3},
    ))
    assert_case("parallel/multiagent", d.molds, ["MULTIAGENT"])

    # 5. High uncertainty: research.
    d = selector.choose(Mission(
        "discover possible approaches",
        {"research_required": True, "high_uncertainty": True},
    ))
    assert_case("uncertainty/research", d.molds, ["RESEARCH"])

    # 6. Failure/context change: recovery can replace the previous mold.
    previous = selector.choose(Mission("execute a known operation"))
    d = switch_after_failure(previous, {"recovery_required": True})
    assert_case("failure/recovery", d.molds, ["RECOVERY"])
    assert_case("failure/switch", d.switched, True)

    # 7. Imperator can explicitly select a mold.
    d = selector.choose(Mission(
        "simple task",
        explicit_mold="AGENT",
    ))
    assert_case("imperator/override", d.molds, ["AGENT"])
    assert_case("imperator/override_reason", d.reason, "imperador_override")

    # 8. A mission may compose molds instead of choosing exactly one.
    d = compose("RESEARCH", "WORKFLOW", "AGENT")
    assert_case("composition/order", d.molds, ["RESEARCH", "WORKFLOW", "AGENT"])

    # 9. Resource availability must not determine the mold.
    # The same strategy remains DIRECT even when the preferred resource changes.
    d1 = selector.choose(Mission("known operation", {"resource": "phone"}))
    d2 = selector.choose(Mission("known operation", {"resource": "vps"}))
    assert_case("resource/strategy independence", d1.molds, d2.molds)

    # 10. Context can change the mold without changing the objective.
    base = selector.choose(Mission("collect a known datum"))
    changed = selector.choose(Mission(
        "collect a known datum",
        {"high_uncertainty": True, "research_required": True},
    ))
    assert_case("same objective/context change", base.molds, ["DIRECT"])
    assert_case("same objective/new context", changed.molds, ["RESEARCH"])

    print("EXPERIMENTO_01: PASS")
    print("Casos validados: 10")
    print("Moldes exercitados:", ", ".join(MOLDS))
    print("Hipótese testada: família de moldes + seleção + override + composição + troca")


if __name__ == "__main__":
    run()
