from abs_core.runtime import build_runtime


def test_shared_runtime_contains_cognitive_and_resource_layers(tmp_path) -> None:
    runtime = build_runtime(str(tmp_path / "abs.db"))
    assert runtime.orchestrator.registry is runtime.registry
    assert runtime.cognitive_runtime.orchestrator is runtime.orchestrator
    assert runtime.resource_dispatcher.orchestrator is runtime.orchestrator
    assert runtime.resource_dispatcher.router is runtime.resource_router
    assert runtime.tool_planner.router is runtime.resource_router
    assert runtime.accounts is not None
    assert runtime.intelligence.list()


def test_shared_runtime_can_discover_core_capabilities(tmp_path) -> None:
    runtime = build_runtime(str(tmp_path / "abs.db"))
    ids = {item.id for item in runtime.registry.list()}
    assert "echo" in ids
    assert "internet-http" in ids
