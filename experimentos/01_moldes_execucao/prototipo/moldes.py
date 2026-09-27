from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

MOLDS = ("DIRECT", "WORKFLOW", "AGENT", "MULTIAGENT", "RESEARCH", "RECOVERY")

WEIGHTS = {"DIRECT": 1, "WORKFLOW": 2, "RESEARCH": 2, "RECOVERY": 2, "AGENT": 3, "MULTIAGENT": 4}

@dataclass
class Mission:
    objective: str
    context: dict[str, Any] = field(default_factory=dict)
    explicit_molds: list[str] | None = None

@dataclass
class MoldPlan:
    molds: list[str]
    complexity: int
    reason: str
    automatic: bool
    candidates: list[str] = field(default_factory=list)

class MoldRegistry:
    def __init__(self) -> None:
        self._molds: dict[str, Callable[..., Any]] = {}

    def register(self, name: str, executor: Callable[..., Any] | None = None) -> None:
        if name not in MOLDS:
            raise ValueError(f"unknown_mold:{name}")
        self._molds[name] = executor or (lambda objective, context: {"status": "simulated", "mold": name})

    def available(self) -> list[str]:
        return sorted(self._molds)

    def has(self, name: str) -> bool:
        return name in self._molds

    def execute(self, name: str, objective: str, context: dict[str, Any]) -> Any:
        return self._molds[name](objective, context)

class MoldSelector:
    """Prototype selector: criteria create candidates; AV-like constraints filter them."""
    def __init__(self, registry: MoldRegistry) -> None:
        self.registry = registry

    def choose(self, mission: Mission) -> MoldPlan:
        if mission.explicit_molds:
            self._validate(mission.explicit_molds)
            return MoldPlan(list(mission.explicit_molds), max(WEIGHTS[m] for m in mission.explicit_molds),
                            "imperador_override", False, list(mission.explicit_molds))

        ctx = mission.context
        if ctx.get("recovery_required"):
            return MoldPlan(["RECOVERY"], 2, "state_requires_recovery", True, ["RECOVERY"])

        candidates = []
        if ctx.get("research_required") or ctx.get("high_uncertainty"):
            candidates.append("RESEARCH")
        if ctx.get("defined_steps"):
            candidates.append("WORKFLOW")
        if ctx.get("open_ended"):
            candidates.append("AGENT")
        if ctx.get("parallelizable") and ctx.get("independent_parts", 1) > 1:
            candidates.append("MULTIAGENT")

        if not candidates:
            candidates = ["DIRECT"]

        candidates = self._apply_constraints(candidates, ctx)
        if not candidates:
            return MoldPlan(["DIRECT"], 1, "constraints_left_no_specialized_mold", True, [])

        return MoldPlan(candidates, max(WEIGHTS[m] for m in candidates),
                        "criteria_composition" if len(candidates) > 1 else f"criteria:{candidates[0]}",
                        True, list(candidates))

    def _apply_constraints(self, candidates, context):
        forbidden = set(context.get("forbid_molds", []))
        filtered = [m for m in candidates if m not in forbidden]
        max_complexity = context.get("max_complexity")
        if max_complexity is not None:
            filtered = [m for m in filtered if WEIGHTS[m] <= max_complexity]
        return filtered

    def _validate(self, molds):
        unknown = [m for m in molds if not self.registry.has(m)]
        if unknown:
            raise ValueError(f"unknown_mold:{','.join(unknown)}")

class MoldRuntime:
    def __init__(self, registry: MoldRegistry) -> None:
        self.registry = registry

    def run(self, plan: MoldPlan, mission: Mission):
        return [self.registry.execute(m, mission.objective, mission.context) for m in plan.molds]

def default_registry() -> MoldRegistry:
    registry = MoldRegistry()
    for mold in MOLDS:
        registry.register(mold)
    return registry
