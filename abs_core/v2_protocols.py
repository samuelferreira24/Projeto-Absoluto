from __future__ import annotations

"""Protocol adapters for ABS V2.

MCP is treated as a tool/resource boundary and A2A as an agent/task boundary.
Neither protocol receives ABS authority implicitly.
"""

import json
import os
import ssl
import urllib.request
import urllib.error
import uuid
from dataclasses import dataclass
from typing import Any


class ProtocolError(RuntimeError):
    pass


@dataclass(frozen=True)
class ProtocolTarget:
    id: str
    endpoint: str
    auth_env: str | None = None
    timeout: int = 30

    def headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.auth_env:
            token = os.getenv(self.auth_env, "")
            if token:
                headers["Authorization"] = f"Bearer {token}"
        return headers


class JsonRpcClient:
    def __init__(self, target: ProtocolTarget):
        self.target = target

    def call(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        request_id = str(uuid.uuid4())
        body = json.dumps({
            "jsonrpc": "2.0", "id": request_id, "method": method, "params": params or {}
        }).encode()
        request = urllib.request.Request(
            self.target.endpoint, data=body, headers=self.target.headers(), method="POST"
        )
        try:
            with urllib.request.urlopen(request, timeout=self.target.timeout,
                                        context=ssl.create_default_context()) as response:
                payload = json.loads(response.read().decode())
        except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
            raise ProtocolError(f"jsonrpc_transport_error:{exc}") from exc
        if payload.get("error"):
            raise ProtocolError(f"jsonrpc_error:{payload['error']}")
        return payload.get("result") or {}


class MCPClient:
    """Minimal MCP JSON-RPC client.

    The client deliberately exposes only protocol operations. ABS policy and
    verification remain outside this class.
    """

    def __init__(self, target: ProtocolTarget):
        self.target = target
        self.rpc = JsonRpcClient(target)

    def initialize(self, client_name: str = "ABS", version: str = "2.0") -> dict[str, Any]:
        return self.rpc.call("initialize", {
            "protocolVersion": version,
            "capabilities": {},
            "clientInfo": {"name": client_name, "version": version},
        })

    def list_tools(self) -> dict[str, Any]:
        return self.rpc.call("tools/list")

    def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.rpc.call("tools/call", {"name": name, "arguments": arguments or {}})


class A2AClient:
    """A2A task boundary represented as an HTTP JSON request.

    Servers can expose a task endpoint; the ABS Work remains authoritative.
    """

    def __init__(self, target: ProtocolTarget):
        self.target = target

    def send_task(self, message: str, *, work_id: str | None = None,
                  metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        body = json.dumps({
            "task": {
                "id": work_id or str(uuid.uuid4()),
                "message": {"role": "user", "parts": [{"kind": "text", "text": message}]},
                "metadata": metadata or {},
            }
        }).encode()
        request = urllib.request.Request(
            self.target.endpoint, data=body, headers=self.target.headers(), method="POST"
        )
        try:
            with urllib.request.urlopen(request, timeout=self.target.timeout,
                                        context=ssl.create_default_context()) as response:
                return json.loads(response.read().decode())
        except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
            raise ProtocolError(f"a2a_transport_error:{exc}") from exc


class ProtocolRegistry:
    def __init__(self):
        self.mcp: dict[str, MCPClient] = {}
        self.a2a: dict[str, A2AClient] = {}

    def register_mcp(self, target: ProtocolTarget) -> MCPClient:
        client = MCPClient(target)
        self.mcp[target.id] = client
        return client

    def register_a2a(self, target: ProtocolTarget) -> A2AClient:
        client = A2AClient(target)
        self.a2a[target.id] = client
        return client

    def discover_from_env(self) -> None:
        mcp = os.getenv("ABS_MCP_ENDPOINT", "").strip()
        if mcp:
            self.register_mcp(ProtocolTarget(
                "mcp:default", mcp, os.getenv("ABS_MCP_AUTH_ENV") or None
            ))
        a2a = os.getenv("ABS_A2A_ENDPOINT", "").strip()
        if a2a:
            self.register_a2a(ProtocolTarget(
                "a2a:default", a2a, os.getenv("ABS_A2A_AUTH_ENV") or None
            ))

    def public(self) -> dict[str, Any]:
        return {
            "mcp": [{"id": k, "endpoint": v.target.endpoint} for k, v in self.mcp.items()],
            "a2a": [{"id": k, "endpoint": v.target.endpoint} for k, v in self.a2a.items()],
        }
