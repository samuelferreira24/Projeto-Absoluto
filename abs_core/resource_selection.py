from .connections import ConnectionRegistry
from .resource_router import ResourceRouteRequest, ResourceRouter


def select_resource_route(
    connections: ConnectionRegistry,
    objective: str,
    required_capabilities: list[str] | None = None,
    preferred_categories: list[str] | None = None,
    preferred_transports: list[str] | None = None,
    require_configured: bool = False,
):
    request = ResourceRouteRequest(
        objective=objective,
        required_capabilities=tuple(required_capabilities or []),
        preferred_categories=tuple(preferred_categories or []),
        preferred_transports=tuple(preferred_transports or []),
        require_configured=require_configured,
    )
    return ResourceRouter(connections).rank(request)
