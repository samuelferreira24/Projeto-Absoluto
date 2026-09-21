from __future__ import annotations

import os
from typing import Any

from .api import serve
from .cli import build
from .resources import ResourceManager
from .interface_runtime import InterfaceRuntime

HOST = os.getenv("ABS_HOST", "127.0.0.1")
PORT = int(os.getenv("ABS_PORT", "8787"))


class LocalABS:
    """Compatibility facade for the local runtime.

    The HTTP surface is now served by ABS API so the interface, capabilities
    and device resources use the same control plane.
    """

    def __init__(self) -> None:
        self.orchestrator = build()
        self.resources = ResourceManager()
        self.interface_runtime = InterfaceRuntime()

    def task(self, payload: dict[str, Any]) -> dict[str, Any]:
        objective = str(payload["objective"])
        context = payload.get("context") or {}
        capability_id = payload.get("capability_id")
        approved = bool(payload.get("approved", False))
        work = self.orchestrator.create(objective, context=context)
        result = self.orchestrator.run(
            work.id,
            capability_id=capability_id,
            approved=approved,
        )
        return {
            "id": result.id,
            "state": result.state.value,
            "objective": result.objective,
            "capability_id": result.capability_id,
            "result": result.result,
            "provenance": result.provenance,
        }


def main() -> None:
    local = LocalABS()
    print(f"ABS V1 running at http://{HOST}:{PORT}")
    print("Interface, capabilities and device resources are served by the unified ABS API.")
    serve(
        local.orchestrator,
        local.orchestrator.registry,
        host=HOST,
        port=PORT,
        resources=local.resources,
        interface_runtime=local.interface_runtime,
    )


if __name__ == "__main__":
    main()
