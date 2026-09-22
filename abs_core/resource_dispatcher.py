from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .capabilities import CapabilityRegistry
from .models import Work
from .resource_router import ResourceRouteRequest, ResourceRouter
from .tool_knowledge import ToolKnowledgeRegistry
from .tool_planner import ToolPlanner


_CONNECTION_TO_CAPABILITY = {
    "codex-termux": "codex",
    "claude-api": "claude",
    "gemini-api": "gemini",
    "openai-api": "openai-api",
}


@dataclass(frozen=True)
class DispatchAttempt:
    connection_id: str
    capability_id: str | None
    status: str
    detail: str | None = None


@dataclass(frozen=True)
class DispatchResult:
    work: Work
    selected_connection: str | None
    attempts: tuple[DispatchAttempt, ...]


class ResourceDispatcher:
    """Converts a planned resource route into an executable capability.

    The dispatcher does not bypass Imperator authorization. It can select a
    fallback path, but execution remains subject to the normal orchestrator
    approval contract.
    """

    def __init__(
        self,
        router: ResourceRouter,
        planner: ToolPlanner,
        capabilities: CapabilityRegistry,
        knowledge: ToolKnowledgeRegistry,
    ) -> None:
        self.router = router
        self.planner = planner
        self.capabilities = capabilities
        self.knowledge = knowledge

    def executable_capability_for(self, connection_id: str):
        capability_id = _CONNECTION_TO_CAPABILITY.get(connection_id)
        if not capability_id:
            return None
        try:
            return self.capabilities.get(capability_id)
        except KeyError:
            return None

    def routes_for(self, request: ResourceRouteRequest):
        return self.router.rank(request)

    def candidate_capabilities(self, required: tuple[str, ...]):
        return [
            cap for cap in self.capabilities.list()
            if set(required).issubset(set(cap.metadata.get("capabilities", required)))
        ]

    def choose_executable_route(self, request: ResourceRouteRequest):
        for route in self.router.rank(request):
            capability = self.executable_capability_for(route.connection_id)
            if capability is not None:
                return route, capability
        raise LookupError("no_executable_resource_route_available")
