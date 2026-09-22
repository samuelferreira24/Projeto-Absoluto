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
    ABSHandler.tool_planner = ToolPlanner(ABSHandler.tool_knowledge, ResourceRouter(ABSHandler.connections))
    ABSHandler.tool_learning = ToolLearningEngine(ABSHandler.tool_knowledge)
    server = ThreadingHTTPServer(("127.0.0.1", 0), ABSHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def test_discover_and_learn_are_distinct_endpoints():
    server, thread = _server()
    try:
        body = json.dumps({
            "name": "Future Tool",
            "source": "https://example.com",
            "category": "research",
            "capabilities": ["research"],
        }).encode()
        req = urllib.request.Request(
            f"http://127.0.0.1:{server.server_port}/tools/discover",
            data=body, method="POST",
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=3) as response:
            payload = json.loads(response.read())
        assert response.status == 201
        assert payload["candidate"]["state"] == "discovered"

        learn_body = json.dumps({
            "tool_id": "claude",
            "success": True,
            "evidence": {"type": "test", "result": "ok"},
            "lesson": "structured prompt works",
        }).encode()
        req = urllib.request.Request(
            f"http://127.0.0.1:{server.server_port}/tools/learn",
            data=learn_body, method="POST",
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=3) as response:
            payload = json.loads(response.read())
        assert response.status == 200
        assert payload["tool"]["status"] == "validated"
        assert payload["tool"]["evidence"][-1]["success"] is True
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)


def test_planner_requires_all_requested_capabilities():
    server, thread = _server()
    try:
        body = json.dumps({
            "objective": "complex work",
            "required_capabilities": ["reasoning", "code"],
            "require_configured": True,
        }).encode()
        req = urllib.request.Request(
            f"http://127.0.0.1:{server.server_port}/tools/plan",
            data=body, method="POST",
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=3) as response:
            payload = json.loads(response.read())
        assert response.status == 200
        assert all(
            set(plan["capabilities"]) >= {"reasoning", "code"}
            for plan in payload["plans"]
        )
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
