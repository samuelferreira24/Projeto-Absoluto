from __future__ import annotations

from .api import serve
from .runtime import build_runtime


def main() -> None:
    runtime = build_runtime()
    serve(
        runtime.orchestrator,
        runtime.registry,
        resources=runtime.resources,
        interface_runtime=runtime.interface_runtime,
        connections=runtime.connections,
        accounts=runtime.accounts,
        tool_knowledge=runtime.tool_knowledge,
        tool_discovery=runtime.tool_discovery,
        tool_planner=runtime.tool_planner,
        tool_learning=runtime.tool_learning,
        resource_dispatcher=runtime.resource_dispatcher,
        cognitive_runtime=runtime.cognitive_runtime,
    )


if __name__ == "__main__":
    main()
