from abs_core.connections import ConnectionRegistry
from abs_core.resource_router import ResourceRouteRequest, ResourceRouter


def test_router_prefers_configured_matching_connection() -> None:
    registry = ConnectionRegistry.defaults()
    registry.update_status("claude-api", "configured", configured=True)

    router = ResourceRouter(registry)
    request = ResourceRouteRequest(
        objective="analisar texto",
        required_capabilities=("reasoning",),
        preferred_categories=("ai",),
        preferred_transports=("https",),
        require_configured=True,
    )

    selected = router.select(request)

    assert selected.connection_id == "claude-api"
    assert "capability-match" in selected.reasons
    assert selected.connection["configured"] is True


def test_router_keeps_alternate_paths() -> None:
    registry = ConnectionRegistry.defaults()
    registry.update_status("github-api", "configured", configured=True)
    registry.update_status("github-termux", "configured", configured=True)

    router = ResourceRouter(registry)
    request = ResourceRouteRequest(
        objective="operar repositório",
        required_capabilities=("repository",),
        require_configured=True,
    )

    routes = router.rank(request)
    ids = {route.connection_id for route in routes}

    assert {"github-api", "github-termux"} <= ids
    assert router.select(request).connection_id in ids


def test_router_does_not_select_planned_browser_when_not_ready() -> None:
    router = ResourceRouter(ConnectionRegistry.defaults())
    request = ResourceRouteRequest(
        objective="pesquisar na web",
        required_capabilities=("browse",),
    )

    try:
        router.select(request)
    except LookupError:
        return

    assert False, "planned browser runtime must not be treated as operational"
