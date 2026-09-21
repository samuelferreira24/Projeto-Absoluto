from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .connections import ConnectionRecord, ConnectionRegistry


@dataclass(frozen=True)
class ResourceRouteRequest:
    """Declarative request for choosing a resource connection.

    Selection is planning only. It does not authenticate, execute, or imply
    that the selected connection is operationally reachable.
    """

    objective: str
    required_capabilities: tuple[str, ...] = ()
    preferred_categories: tuple[str, ...] = ()
    preferred_transports: tuple[str, ...] = ()
    allowed_connections: tuple[str, ...] = ()
    excluded_connections: tuple[str, ...] = ()
    require_configured: bool = False
    context: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ResourceRoute:
    connection_id: str
    score: float
    reasons: tuple[str, ...]
    connection: dict[str, Any]


class ResourceRouter:
    """Selects among replaceable resource/connection paths.

    The router intentionally sits above individual adapters. A logical
    resource can therefore have API, CLI, connector, browser or local paths.
    """

    _STATUS_SCORE = {
        "configured": 30.0,
        "available": 20.0,
        "degraded": 5.0,
        "planned": -50.0,
        "extensible": -40.0,
        "offline": -100.0,
    }

    def __init__(self, connections: ConnectionRegistry) -> None:
        self.connections = connections

    def rank(self, request: ResourceRouteRequest) -> list[ResourceRoute]:
        required = set(request.required_capabilities)
        allowed = set(request.allowed_connections)
        excluded = set(request.excluded_connections)

        routes: list[ResourceRoute] = []
        for item in self.connections.list():
            if allowed and item.id not in allowed:
                continue
            if item.id in excluded:
                continue
            if request.require_configured and not item.configured:
                continue

            capabilities = set(item.capabilities)
            missing = sorted(required - capabilities)
            if missing:
                continue

            if item.status in {"planned", "extensible", "offline"}:
                continue

            score = self._STATUS_SCORE.get(item.status, 0.0)
            reasons: list[str] = [f"status:{item.status}"]

            if required:
                score += 20.0 * len(required & capabilities)
                reasons.append("capability-match")

            if item.category in request.preferred_categories:
                score += 10.0
                reasons.append("preferred-category")

            if item.transport in request.preferred_transports:
                score += 8.0
                reasons.append("preferred-transport")

            if item.configured:
                score += 5.0
                reasons.append("configured")

            if item.status in {"planned", "extensible", "offline"}:
                reasons.append("not-ready")

            routes.append(
                ResourceRoute(
                    connection_id=item.id,
                    score=score,
                    reasons=tuple(reasons),
                    connection=item.public(),
                )
            )

        return sorted(routes, key=lambda route: (-route.score, route.connection_id))

    def select(self, request: ResourceRouteRequest) -> ResourceRoute:
        routes = self.rank(request)
        if not routes:
            raise LookupError("no_resource_route_available")
        return routes[0]

    def alternatives(self, request: ResourceRouteRequest) -> list[ResourceRoute]:
        return self.rank(request)[1:]
