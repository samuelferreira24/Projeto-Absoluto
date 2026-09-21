from __future__ import annotations

import os
from dataclasses import asdict, dataclass, field
from threading import RLock
from typing import Any


@dataclass
class ConnectionRecord:
    id: str
    name: str
    category: str
    transport: str
    status: str = "available"
    configured: bool = False
    endpoint: str | None = None
    capabilities: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def public(self) -> dict[str, Any]:
        data = asdict(self)
        data["capabilities"] = sorted(set(self.capabilities))
        return data


class ConnectionRegistry:
    """Extensible registry for external tools, networks, APIs and interfaces.

    A connection is deliberately separate from a capability implementation.
    A service may be reachable through more than one transport.
    """

    def __init__(self) -> None:
        self._lock = RLock()
        self._items: dict[str, ConnectionRecord] = {}

    def register(self, record: ConnectionRecord) -> None:
        with self._lock:
            if record.id in self._items:
                raise ValueError(f"Connection already registered: {record.id}")
            self._items[record.id] = record

    def get(self, connection_id: str) -> ConnectionRecord:
        with self._lock:
            return self._items[connection_id]

    def list(self) -> list[ConnectionRecord]:
        with self._lock:
            return [ConnectionRecord(**asdict(item)) for item in self._items.values()]

    def public(self) -> list[dict[str, Any]]:
        return [item.public() for item in self.list()]

    def update_status(self, connection_id: str, status: str, configured: bool | None = None) -> ConnectionRecord:
        with self._lock:
            item = self._items[connection_id]
            item.status = status
            if configured is not None:
                item.configured = configured
            return ConnectionRecord(**asdict(item))

    @classmethod
    def defaults(cls) -> "ConnectionRegistry":
        registry = cls()

        def add(id: str, name: str, category: str, transport: str, *,
                env: str | None = None, endpoint: str | None = None,
                capabilities: list[str] | None = None, status: str = "available",
                metadata: dict[str, Any] | None = None) -> None:
            configured = bool(env and os.getenv(env))
            registry.register(ConnectionRecord(
                id=id,
                name=name,
                category=category,
                transport=transport,
                status=("configured" if configured else status),
                configured=configured,
                endpoint=endpoint,
                capabilities=capabilities or [],
                metadata={**(metadata or {}), **({"credential_env": env} if env else {})},
            ))

        add("codex-termux", "OpenAI Codex CLI", "ai", "cli-termux",
            capabilities=["code", "reasoning", "execution"], metadata={"adapter": "codex"})
        add("chatgpt-connector", "ChatGPT Connector", "ai", "connector",
            capabilities=["ai", "context", "tool-access"],
            metadata={"host_managed": True, "note": "Connector availability is managed by the host platform."})
        add("claude-api", "Anthropic Claude API", "ai", "https",
            env="ANTHROPIC_API_KEY", endpoint="https://api.anthropic.com/v1/messages",
            capabilities=["ai", "reasoning", "multimodal"], metadata={"adapter": "claude"})
        add("gemini-api", "Google Gemini API", "ai", "https",
            env="GEMINI_API_KEY", endpoint="https://generativelanguage.googleapis.com/v1/interactions",
            capabilities=["ai", "reasoning", "multimodal", "agents"], metadata={"adapter": "gemini"})
        add("local-ai", "IA local", "ai", "local-http",
            env="ABS_LOCAL_AI_URL", endpoint=os.getenv("ABS_LOCAL_AI_URL"),
            capabilities=["ai", "offline-capable"], metadata={"replaceable": True})
        add("internet-http", "Internet / HTTP", "network", "https",
            capabilities=["web", "http", "api"])
        add("browser-runtime", "Browser Runtime", "network", "browser",
            capabilities=["browse", "research", "web-execution"],
            status="planned", metadata={"runtime_required": True})
        add("api-http", "APIs externas", "service", "https",
            capabilities=["rest", "graphql", "websocket"])
        add("github-api", "GitHub API", "service", "https",
            env="ABS_GITHUB_TOKEN", endpoint="https://api.github.com",
            capabilities=["repository", "issues", "actions", "source-control"])
        add("github-termux", "GitHub via Termux", "service", "cli-termux",
            capabilities=["git", "repository", "source-control"])
        add("local-network", "Rede local", "network", "lan",
            capabilities=["devices", "services", "discovery"])
        add("remote-device", "Dispositivo remoto", "resource", "abs-agent",
            capabilities=["execution", "resources", "heartbeat"],
            status="planned", metadata={"requires_agent": True})
        add("future-network", "Nova tecnologia de rede", "network", "extensible",
            capabilities=["transport"], status="extensible")
        return registry
