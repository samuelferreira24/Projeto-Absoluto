import json
import threading
import urllib.request
from http.server import ThreadingHTTPServer

from abs_core.api import ABSHandler
from abs_core.cli import build
from abs_core.connections import ConnectionRegistry
from abs_core.interface_runtime import InterfaceRuntime
from abs_core.resources import ResourceManager


def test_resource_selection_api_returns_ranked_routes() -> None:
    orch = build()
    ABSHandler.orchestrator = orch
    ABSHandler.registry = orch.registry
    ABSHandler.resources = ResourceManager()
    ABSHandler.interface_runtime = InterfaceRuntime()
    ABSHandler.connections = ConnectionRegistry.defaults()

    ABSHandler.connections.update_status("claude-api", "configured", configured=True)

    server = ThreadingHTTPServer(("127.0.0.1", 0), ABSHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"

    try:
        body = json.dumps({
            "objective": "analisar um texto",
            "required_capabilities": ["reasoning"],
            "preferred_categories": ["ai"],
            "require_configured": True,
        }).encode()
        request = urllib.request.Request(
            base + "/resources/select",
            data=body,
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=3) as response:
            assert response.status == 200
            payload = json.loads(response.read())

        assert payload["routes"]
        assert payload["routes"][0]["connection_id"] == "claude-api"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
