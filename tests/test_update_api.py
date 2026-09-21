import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

from abs_core.api import ABSHandler
from abs_core.cli import build
from abs_core.connections import ConnectionRegistry
from abs_core.interface_runtime import InterfaceRuntime
from abs_core.resources import ResourceManager


def test_update_api_requires_explicit_approval(monkeypatch) -> None:
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
        with urllib.request.urlopen(base + "/update/status", timeout=3) as response:
            assert response.status == 200
            payload = json.loads(response.read())
        assert "current_commit" in payload

        request = urllib.request.Request(
            base + "/update/apply",
            data=b'{"approved": false}',
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        try:
            urllib.request.urlopen(request, timeout=3)
            assert False
        except urllib.error.HTTPError as exc:
            assert exc.code == 403
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
