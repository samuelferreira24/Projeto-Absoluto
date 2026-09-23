from __future__ import annotations

"""Stable integration contract for ABS surfaces and nodes."""

from typing import Any

API_VERSION = "v1"
PROTOCOL_VERSION = "abs-integration-v1"


def integration_descriptor() -> dict[str, Any]:
    return {
        "name": "ABS",
        "protocol": PROTOCOL_VERSION,
        "api_version": API_VERSION,
        "role": "integration-boundary",
        "surfaces": ["web", "app", "server", "termux", "remote-node"],
        "principles": [
            "surfaces are replaceable",
            "runtime is not tied to one interface",
            "state belongs to ABS, not to a client",
            "clients integrate through versioned contracts",
        ],
        "transports": ["http", "json", "sse-ready"],
        "resources": ["/api/v1/intelligence", "/api/v1/capabilities", "/api/v1/connections"],
        "execution": ["/api/v1/chat", "/api/v1/works", "/api/v1/resources/dispatch"],
    }
