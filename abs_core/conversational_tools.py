from __future__ import annotations

import re
from typing import Any

from .resource_dispatcher import ResourceDispatcher
from .resource_router import ResourceRouteRequest
from .tool_planner import ToolPlanner


class ConversationalToolRuntime:
    """Turns explicit conversational tool requests into normal ABS work."""

    _GITHUB_MARKERS = (
        "github",
        "github.com",
        "repositório do projeto",
        "repositorio do projeto",
    )

    def __init__(self, planner: ToolPlanner, dispatcher: ResourceDispatcher) -> None:
        self.planner = planner
        self.dispatcher = dispatcher

    def detect(self, message: str) -> dict[str, Any] | None:
        text = str(message or "").strip()
        lowered = text.lower()
        if not any(marker in lowered for marker in self._GITHUB_MARKERS):
            return None

        write_markers = (
            "crie", "criar", "edite", "editar", "altere", "alterar",
            "apague", "apagar", "commit", "push", "merge", "publique",
        )
        if any(marker in lowered for marker in write_markers):
            return {
                "tool_id": "github",
                "action": "unsupported_write",
                "reason": "github_write_requires_explicit_write_workflow",
            }

        action = "repository"
        if any(word in lowered for word in ("arquivo", "ficheiro", "file")):
            action = "file"
        elif any(word in lowered for word in ("pasta", "diretório", "diretorio", "directory")):
            action = "directory"
        elif any(word in lowered for word in ("buscar", "procure", "procurar", "pesquise", "pesquisar", "search")):
            action = "search"

        context: dict[str, Any] = {"action": action}
        if action == "file":
            match = re.search(r"(?:arquivo|ficheiro|file)\s+(?:chamado\s+|de\s+)?['\"]?([^'\"\n,;]+)", text, re.IGNORECASE)
            if match:
                context["path"] = match.group(1).strip()
        elif action == "directory":
            match = re.search(r"(?:pasta|diret[oó]rio|directory)\s+(?:chamada\s+|de\s+)?['\"]?([^'\"\n,;]+)", text, re.IGNORECASE)
            if match:
                context["path"] = match.group(1).strip()
        elif action == "search":
            match = re.search(r"(?:buscar|procure|procurar|pesquise|pesquisar|search)\s+(.+)$", text, re.IGNORECASE)
            if match:
                context["query"] = match.group(1).strip()

        return {"tool_id": "github", **context}

    def execute(self, message: str) -> dict[str, Any] | None:
        intent = self.detect(message)
        if intent is None:
            return None
        if intent.get("action") == "unsupported_write":
            return {
                "type": "tool_blocked",
                "tool": "github",
                "reason": intent["reason"],
            }

        required = ("repository",)
        objective = f"GitHub: {message}"
        request = ResourceRouteRequest(
            objective=objective,
            required_capabilities=required,
            preferred_categories=("source-control",),
            context={"tool_id": "github"},
        )
        plans = self.planner.plan(
            objective,
            required,
            preferred_categories=("source-control",),
            tool_id="github",
        )
        if not plans:
            raise LookupError("github_tool_route_not_available")

        context = dict(intent)
        context["tool_id"] = "github"
        context["source"] = "conversational"
        result = self.dispatcher.dispatch(
            objective,
            request,
            context=context,
            approved=True,
        )
        return {
            "type": "tool_result",
            "tool": "github",
            "action": intent["action"],
            "route": result.selected_connection,
            "plan": {
                "tool_id": plans[0].tool_id,
                "routes": list(plans[0].routes),
            },
            "result": result.work.result,
            "work_id": result.work.id,
        }
