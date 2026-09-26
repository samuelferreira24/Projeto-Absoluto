from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse

from .resource_dispatcher import ResourceDispatcher
from .resource_router import ResourceRouteRequest
from .tool_planner import ToolPlanner


class ConversationalToolRuntime:
    """Automatically routes supported conversational tool requests through ABS."""

    _GITHUB_MARKERS = (
        "github",
        "github.com",
        "repositório do projeto",
        "repositorio do projeto",
    )

    _URL_RE = re.compile(r"https?://[^\s<>'\"]+")

    def __init__(self, planner: ToolPlanner, dispatcher: ResourceDispatcher) -> None:
        self.planner = planner
        self.dispatcher = dispatcher

    def detect(self, message: str) -> dict[str, Any] | None:
        text = str(message or "").strip()
        lowered = text.lower()
        if not text:
            return None

        url_match = self._URL_RE.search(text)
        if url_match and not any(marker in lowered for marker in self._GITHUB_MARKERS):
            url = url_match.group(0).rstrip(".,;:)]}")
            parsed = urlparse(url)
            if parsed.scheme in {"http", "https"} and parsed.netloc:
                return {
                    "tool_id": "internet-http",
                    "action": "get",
                    "url": url,
                }

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
            match = re.search(
                r"(?:arquivo|ficheiro|file)\s+(?:chamado\s+|de\s+)?['\"]?([^'\"\n,;]+)",
                text,
                re.IGNORECASE,
            )
            if match:
                context["path"] = match.group(1).strip()
        elif action == "directory":
            match = re.search(
                r"(?:pasta|diret[oó]rio|directory)\s+(?:chamada\s+|de\s+)?['\"]?([^'\"\n,;]+)",
                text,
                re.IGNORECASE,
            )
            if match:
                context["path"] = match.group(1).strip()
        elif action == "search":
            match = re.search(
                r"(?:buscar|procure|procurar|pesquise|pesquisar|search)\s+(.+?)(?:\s+no\s+github|\s+no\s+reposit[oó]rio.*)?$",
                text,
                re.IGNORECASE,
            )
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

        tool_id = str(intent["tool_id"])
        if tool_id == "github":
            required = ("repository",)
            category = "source-control"
        elif tool_id == "internet-http":
            required = ("http",)
            category = "network"
        else:
            raise LookupError(f"unsupported_conversational_tool:{tool_id}")

        objective = str(message)
        request = ResourceRouteRequest(
            objective=objective,
            required_capabilities=required,
            preferred_categories=(category,),
            context={"tool_id": tool_id},
        )
        plans = self.planner.plan(
            objective,
            required,
            preferred_categories=(category,),
            tool_id=tool_id if tool_id == "github" else None,
        )
        if not plans:
            raise LookupError(f"{tool_id}_tool_route_not_available")

        context = dict(intent)
        context["tool_id"] = tool_id
        context["source"] = "conversational"
        result = self.dispatcher.dispatch(
            objective,
            request,
            context=context,
            approved=True,
        )
        return {
            "type": "tool_result",
            "tool": tool_id,
            "action": intent["action"],
            "route": result.selected_connection,
            "plan": {
                "tool_id": plans[0].tool_id,
                "routes": list(plans[0].routes),
            },
            "result": result.work.result,
            "work_id": result.work.id,
        }
