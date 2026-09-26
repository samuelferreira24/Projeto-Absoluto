from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .capabilities import CapabilityRegistry
from .models import Work
from .orchestrator import Orchestrator
from .resource_router import ResourceRouteRequest, ResourceRouter
from .tool_knowledge import ToolKnowledgeRegistry
from .tool_planner import ToolPlanner
from .tool_learning import ToolLearningEngine


_CONNECTION_TO_CAPABILITY = {
    "codex-termux": "codex",
    "claude-api": "claude",
    "gemini-api": "gemini",
    "openai-api": "openai-api",
    "internet-http": "internet-http",
    "github-api": "github",
    "github-termux": "github",
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
        learning: ToolLearningEngine | None = None,
    ) -> None:
        self.router = router
        self.planner = planner
        self.capabilities = capabilities
        self.knowledge = knowledge
        self.learning = learning or ToolLearningEngine(knowledge)
        self.orchestrator = None

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

    def _learn(self, capability_id: str, connection_id: str, work: Work, success: bool, detail: str | None = None) -> None:
        try:
            self.learning.record(
                capability_id,
                success=success,
                evidence={
                    "work_id": work.id,
                    "connection_id": connection_id,
                    "state": work.state.value,
                    "detail": detail,
                },
                usage_pattern="resource-dispatch",
                lesson="dispatch succeeded" if success else "dispatch failed",
            )
        except KeyError:
            pass

    def dispatch(
        self,
        objective: str,
        request: ResourceRouteRequest,
        *,
        context: dict[str, Any] | None = None,
        approved: bool = False,
        orchestrator: Orchestrator | None = None,
    ) -> DispatchResult:
        orch = orchestrator or self.orchestrator
        if orch is None:
            raise RuntimeError("orchestrator_required")
        work = orch.create(objective, context or {})
        attempts: list[DispatchAttempt] = []
        for route in self.router.rank(request):
            capability = self.executable_capability_for(route.connection_id)
            if capability is None:
                attempts.append(DispatchAttempt(
                    route.connection_id, None, "unavailable", "no_registered_capability"
                ))
                continue
            try:
                work = orch.run(work.id, capability.id, approved=approved)
            except PermissionError as exc:
                attempts.append(DispatchAttempt(
                    route.connection_id, capability.id, "denied", str(exc)
                ))
                raise
            if work.state.value == "completed":
                self._learn(capability.id, route.connection_id, work, True)
                attempts.append(DispatchAttempt(route.connection_id, capability.id, "completed"))
                return DispatchResult(work, route.connection_id, tuple(attempts))
            detail = (work.result or {}).get("error") if isinstance(work.result, dict) else None
            self._learn(capability.id, route.connection_id, work, False, detail)
            attempts.append(DispatchAttempt(
                route.connection_id, capability.id, "failed", detail,
            ))
        return DispatchResult(work, None, tuple(attempts))
