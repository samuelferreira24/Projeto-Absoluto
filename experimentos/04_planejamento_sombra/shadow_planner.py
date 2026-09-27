from dataclasses import dataclass, field
from typing import Any

from abs_core.capabilities import CapabilityRegistry
from abs_core.resource_router import ResourceRouteRequest, ResourceRouter


@dataclass
class ShadowMission:
    objective: str
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class ShadowPlan:
    mode: str
    required_capabilities: tuple[str, ...]
    resource_request: ResourceRouteRequest


MODE_TO_REQUIREMENT = {
    "DIRECT": ("execute",),
    "WORKFLOW": ("workflow",),
    "RESEARCH": ("research",),
    "AGENT": ("reasoning",),
    "MULTIAGENT": ("parallel",),
    "RECOVERY": ("recovery",),
}


def select_mode(mission: ShadowMission) -> str:
    c = mission.context
    if c.get("recovery_required"):
        return "RECOVERY"
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


def build_shadow_plan(mission: ShadowMission, capabilities: CapabilityRegistry, resources: ResourceRouter) -> ShadowPlan:
    mode = select_mode(mission)
    if mode == "OBSERVE":
        required = ("observe",)
    else:
        required = MODE_TO_REQUIREMENT[mode]

    request = ResourceRouteRequest(
        objective=mission.objective,
        required_capabilities=required,
        context=mission.context,
    )
    return ShadowPlan(mode, required, request)


def evaluate_plan(plan: ShadowPlan, capabilities: CapabilityRegistry, resources: ResourceRouter) -> dict[str, Any]:
    available_caps = {
        item.id: item for item in capabilities.list()
        if set(plan.required_capabilities).issubset(set(item.metadata.get("capabilities", ())))
    }
    routes = resources.rank(plan.resource_request)
    return {
        "mode": plan.mode,
        "required_capabilities": plan.required_capabilities,
        "capabilities_found": sorted(available_caps),
        "routes_found": [r.connection_id for r in routes],
        "executable": bool(available_caps and routes),
    }
