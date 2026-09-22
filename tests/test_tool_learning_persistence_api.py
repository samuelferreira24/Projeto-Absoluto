import json
import threading
import urllib.request
from http.server import ThreadingHTTPServer

from abs_core.api import ABSHandler
from abs_core.cli import build
from abs_core.connections import ConnectionRegistry
from abs_core.interface_runtime import InterfaceRuntime
from abs_core.resource_router import ResourceRouter
from abs_core.resources import ResourceManager
from abs_core.tool_catalog import default_tool_knowledge
from abs_core.tool_discovery import ToolDiscovery
from abs_core.tool_learning import ToolLearningEngine
from abs_core.tool_knowledge_store import ToolKnowledgeStore
from abs_core.tool_planner import ToolPlanner


def test_tool_learning_api_changes_state_and_persists() -> None:
    orch = build()
    ABSHandler.orchestrator = orch
    ABSHandler.registry = orch.registry
    ABSHandler.resources = ResourceManager()
    ABSHandler.interface_runtime = InterfaceRuntime()
    ABSHandler.connections = ConnectionRegistry.defaults()
    ABSHandler.tool_knowledge = default_tool_knowledge()
    ABSHandler.tool_discovery = ToolDiscovery()
    ABSHandler.tool_planner = ToolPlanner(ABSHandler.tool_knowledge, ResourceRouter(ABSHandler.connections))
    ABSHandler.tool_learning = ToolLearningEngine(ABSHandler.tool_knowledge)

    server = ThreadingHTTPServer(("127.0.0.1", 0), ABSHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        body = json.dumps({
            "tool_id": "claude",
            "success": True,
            "evidence": {"type": "integration", "result": "ok"},
            "lesson": "validated structured prompt",
        }).encode()
        req = urllib.request.Request(
            f"http://127.0.0.1:{server.server_port}/tools/learn",
            data=body, method="POST",
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=3) as response:
            payload = json.loads(response.read())
        assert payload["tool"]["status"] == "validated"
        assert payload["tool"]["evidence"][-1]["success"] is True

        store = ToolKnowledgeStore(":memory:")
        assert store.save_registry(ABSHandler.tool_knowledge) > 0
        restored = default_tool_knowledge()
        assert store.load_into(restored) > 0
        assert restored.get("claude").status == "validated"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
