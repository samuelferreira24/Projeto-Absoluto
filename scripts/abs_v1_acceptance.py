from __future__ import annotations

"""V1 acceptance preflight.

This does not pretend that external services are available. It checks the ABS
composition, local data/verification layers, and reports configured AI routes.
Run with: python -m scripts.abs_v1_acceptance
"""

import json

from abs_core.runtime import build_runtime
from abs_core.verification import ResultVerifier


def main() -> int:
    runtime = build_runtime(":memory:")
    capabilities = runtime.registry.list()
    intelligences = runtime.intelligence.list()

    echo = runtime.orchestrator.create("V1 preflight echo")
    result = runtime.orchestrator.run(echo.id, "echo", approved=True)
    verification = result.result.get("verification") if isinstance(result.result, dict) else None
    memory = runtime.data_layer.search(kind="work_result", query=echo.id, limit=1)
    report = {
        "status": "PASS" if result.state.value == "completed" and memory else "FAIL",
        "capabilities": [{"id": x.id, "kind": x.kind, "name": x.name} for x in capabilities],
        "intelligences": [x.public() for x in intelligences],
        "echo_work": {"id": echo.id, "state": result.state.value, "verification": verification},
        "data_layer": {"work_result_recorded": bool(memory)},
        "manual_next": [
            "configure/install local models",
            "configure at least one external provider if desired",
            "run online/offline/model-switch/recovery acceptance tests",
            "connect an auxiliary OpenAI-compatible UI if desired",
        ],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
