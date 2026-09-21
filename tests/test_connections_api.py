import json
import threading
import urllib.request
from http.server import ThreadingHTTPServer

from abs_core.api import ABSHandler
from abs_core.cli import build
from abs_core.connections import ConnectionRegistry
from abs_core.interface_runtime import InterfaceRuntime
from abs_core.resources import ResourceManager


def test_connections_http_contract(tmp_path) -> None:
    orch = build()
    ABSHandler.orchestrator = orch
    ABSHandler.registry = orch.registry
    ABSHandler.resources = ResourceManager()
    ABSHandler.interface_runtime = InterfaceRuntime()
    ABSHandler.connections = ConnectionRegistry.defaults()

    server = ThreadingHTTPServer(("127.0.0.1", 0), ABSHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"

    try:
        with urllib.request.urlopen(base + "/connections", timeout=3) as response:
            assert response.status == 200
            data = json.loads(response.read())
        ids = {item["id"] for item in data["connections"]}
        assert "codex-termux" in ids
        assert "claude-api" in ids
        assert "gemini-api" in ids

        with urllib.request.urlopen(base + "/health", timeout=3) as response:
            health = json.loads(response.read())
        assert health["status"] == "alive"
        assert health["auto_update"] is True
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
