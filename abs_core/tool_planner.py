from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .resource_router import ResourceRouteRequest, ResourceRouter
from .tool_knowledge import ToolKnowledge, ToolKnowledgeRegistry


@dataclass(frozen=True)
class ToolPlan:
    objective: str
    tool_id: str
    tool_name: str
    capabilities: tuple[str, ...]
    routes: tuple[dict[str, Any], ...]
    rationale: tuple[str, ...] = ()
    constraints: tuple[str, ...] = ()


class ToolPlanner:
    """Combines tool knowledge with connection routing.

    Planning remains separate from execution and authorization.
    """

    def __init__(self, knowledge: ToolKnowledgeRegistry, router: ResourceRouter) -> None:
        self.knowledge = knowledge
        self.router = router

    def plan(
        self,
        objective: str,
        required_capabilities: tuple[str, ...],
        *,
        preferred_categories: tuple[str, ...] = (),
        require_configured: bool = False,
        tool_id: str | None = None,
    ) -> list[ToolPlan]:
        candidates = (
            [self.knowledge.get(tool_id)]
            if tool_id
            else self.knowledge.find_by_capabilities(required_capabilities)
            if required_capabilities
            else self.knowledge.list()
        )

        plans: list[ToolPlan] = []
        for tool in candidates:
            if any(cap not in tool.capabilities for cap in required_capabilities):
                continue
            route_request = ResourceRouteRequest(
                objective=objective,
                required_capabilities=tuple(required_capabilities),
                preferred_categories=preferred_categories or (tool.category,),
                require_configured=require_configured,
            )
            routes = self.router.rank(route_request)
            if not routes:
                continue
            plans.append(ToolPlan(
                objective=objective,
                tool_id=tool.id,
                tool_name=tool.name,
                capabilities=tuple(tool.capabilities),
                routes=tuple(
                    {
                        "connection_id": route.connection_id,
                        "score": route.score,
                        "reasons": list(route.reasons),
                    }
                    for route in routes
                ),
                rationale=(
                    f"tool:{tool.id}",
                    f"status:{tool.status}",
                    f"route:{routes[0].connection_id}",
                ),
                constraints=tuple(tool.constraints),
            ))

        return plans
