import json
import threading
import urllib.request
from http.server import ThreadingHTTPServer

from abs_core.api import ABSHandler
from abs_core.interface_runtime import InterfaceRuntime
from abs_core.resources import ResourceManager
from abs_core.server import build_registry
from abs_core.orchestrator import Orchestrator
from abs_core.store import WorkStore


def test_interface_runtime_http_contract(tmp_path) -> None:
    registry = build_registry()
    orchestrator = Orchestrator(registry, WorkStore(str(tmp_path / "abs.db")))
    ABSHandler.orchestrator = orchestrator
    ABSHandler.registry = registry
    ABSHandler.resources = ResourceManager()
    ABSHandler.interface_runtime = InterfaceRuntime()

    server = ThreadingHTTPServer(("127.0.0.1", 0), ABSHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"

    def request(path, method="GET", payload=None):
        body = None
        headers = {}
        if payload is not None:
            body = json.dumps(payload).encode()
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(base + path, data=body, method=method, headers=headers)
        with urllib.request.urlopen(req, timeout=3) as response:
            return response.status, json.loads(response.read())

    try:
        status, state = request("/interface/state")
        assert status == 200
        assert state["mode"]["id"] == "control"

        status, modes = request("/interface/modes")
        assert status == 200
        assert any(mode["id"] == "browser" for mode in modes["modes"])

        status, state = request("/interface/mode", "POST", {"mode_id": "browser"})
        assert status == 200
        assert state["mode"]["id"] == "browser"

        status, state = request("/interface/input", "POST", {"channel": "voice"})
        assert status == 200
        assert state["input_channel"] == "voice"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
