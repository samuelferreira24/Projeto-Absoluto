import json
import threading
import urllib.request
from http.server import ThreadingHTTPServer

from abs_core.api import ABSHandler
from abs_core.cli import build
from abs_core.connections import ConnectionRegistry
from abs_core.interface_runtime import InterfaceRuntime
from abs_core.resources import ResourceManager
from abs_core.tool_catalog import default_tool_knowledge
from abs_core.tool_discovery import ToolDiscovery
from abs_core.tool_learning import ToolLearningEngine
from abs_core.tool_planner import ToolPlanner
from abs_core.resource_router import ResourceRouter


def _server():
    orch = build()
    ABSHandler.orchestrator = orch
    ABSHandler.registry = orch.registry
    ABSHandler.resources = ResourceManager()
    ABSHandler.interface_runtime = InterfaceRuntime()
    ABSHandler.connections = ConnectionRegistry.defaults()
    ABSHandler.connections.update_status("claude-api", "configured", configured=True)
    ABSHandler.tool_knowledge = default_tool_knowledge()
    ABSHandler.tool_discovery = ToolDiscovery()
    ABSHandler.tool_planner = ToolPlanner(
        ABSHandler.tool_knowledge, ResourceRouter(ABSHandler.connections)
    )
    ABSHandler.tool_learning = ToolLearningEngine(ABSHandler.tool_knowledge)
    server = ThreadingHTTPServer(("127.0.0.1", 0), ABSHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def test_tool_plan_api() -> None:
    server, thread = _server()
    try:
        body = json.dumps({
            "objective": "analisar texto",
            "required_capabilities": ["reasoning"],
            "preferred_categories": ["ai"],
            "require_configured": True,
        }).encode()
        request = urllib.request.Request(
            f"http://127.0.0.1:{server.server_port}/tools/plan",
            data=body,
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=3) as response:
            payload = json.loads(response.read())
        assert response.status == 200
        assert any(plan["tool_id"] == "claude" for plan in payload["plans"])
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
