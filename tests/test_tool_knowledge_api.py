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


def test_tool_knowledge_api_exposes_catalog() -> None:
    orch = build()
    ABSHandler.orchestrator = orch
    ABSHandler.registry = orch.registry
    ABSHandler.resources = ResourceManager()
    ABSHandler.interface_runtime = InterfaceRuntime()
    ABSHandler.connections = ConnectionRegistry.defaults()
    ABSHandler.tool_knowledge = default_tool_knowledge()
    ABSHandler.tool_discovery = ToolDiscovery()

    server = ThreadingHTTPServer(("127.0.0.1", 0), ABSHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"

    try:
        with urllib.request.urlopen(base + "/tools/knowledge", timeout=3) as response:
            payload = json.loads(response.read())
        ids = {item["id"] for item in payload["tools"]}
        assert {"chatgpt", "codex", "claude", "gemini"} <= ids
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)


def test_tool_discovery_api_returns_untrusted_candidate_state() -> None:
    orch = build()
    ABSHandler.orchestrator = orch
    ABSHandler.registry = orch.registry
    ABSHandler.resources = ResourceManager()
    ABSHandler.interface_runtime = InterfaceRuntime()
    ABSHandler.connections = ConnectionRegistry.defaults()
    ABSHandler.tool_knowledge = default_tool_knowledge()
    ABSHandler.tool_discovery = ToolDiscovery()

    server = ThreadingHTTPServer(("127.0.0.1", 0), ABSHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"

    try:
        body = json.dumps({
            "name": "Future Tool",
            "source": "https://example.com",
            "category": "research",
            "capabilities": ["research"],
        }).encode()
        request = urllib.request.Request(
            base + "/tools/discover",
            data=body,
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=3) as response:
            payload = json.loads(response.read())
        assert response.status == 201
        assert payload["candidate"]["state"] == "discovered"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
