from abs_core.runtime import build_runtime


def test_local_composition_registers_codex_and_dispatcher(tmp_path):
    runtime = build_runtime(str(tmp_path / "abs.db"))

    assert runtime.registry.get("codex").id == "codex"
    assert runtime.resource_dispatcher.orchestrator is runtime.orchestrator
    route, capability = runtime.resource_dispatcher.choose_executable_route(
        __import__("abs_core.resource_router", fromlist=["ResourceRouteRequest"]).ResourceRouteRequest(
            objective="modify and test the ABS repository",
            required_capabilities=("code", "execution"),
            preferred_categories=("ai",),
        )
    )
    assert route.connection_id == "codex-termux"
    assert capability.id == "codex"
