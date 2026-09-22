import json
import threading
from http.client import HTTPConnection

from abs_core.accounts import AccountRegistry
from abs_core.adapters import EchoCapability
from abs_core.api import ABSHandler
from abs_core.capabilities import CapabilityRecord, CapabilityRegistry
from abs_core.orchestrator import Orchestrator
from abs_core.store import WorkStore


def test_accounts_api_registers_multiple_accounts():
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("echo", "Echo", "test", EchoCapability()))
    store = WorkStore(":memory:")
    orchestrator = Orchestrator(registry, store)
    ABSHandler.orchestrator = orchestrator
    ABSHandler.registry = registry
    ABSHandler.accounts = AccountRegistry(":memory:")

    from http.server import ThreadingHTTPServer
    server = ThreadingHTTPServer(("127.0.0.1", 0), ABSHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        conn = HTTPConnection(*server.server_address)
        payloads = [
            {"id": "chatgpt-1", "provider": "chatgpt", "name": "Conta 1", "connection_id": "chatgpt-connector"},
            {"id": "chatgpt-2", "provider": "chatgpt", "name": "Conta 2", "connection_id": "chatgpt-connector"},
        ]
        for payload in payloads:
            conn.request("POST", "/accounts/register", body=json.dumps(payload), headers={"Content-Type": "application/json"})
            assert conn.getresponse().status == 201
        conn.request("GET", "/accounts")
        response = conn.getresponse()
        body = json.loads(response.read())
        assert response.status == 200
        assert {item["id"] for item in body["accounts"]} == {"chatgpt-1", "chatgpt-2"}
    finally:
        server.shutdown()
        server.server_close()
