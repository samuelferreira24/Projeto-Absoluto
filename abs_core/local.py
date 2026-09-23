from __future__ import annotations

import os
import subprocess
from pathlib import Path

from .api import serve
from .runtime import build_runtime

HOST = os.getenv("ABS_HOST", "127.0.0.1")
PORT = int(os.getenv("ABS_PORT", "8787"))


def _ensure_updater_service() -> None:
    if os.getenv("ABS_DISABLE_AUTO_UPDATER", "0").lower() in {"1", "true", "yes"}:
        return
    if os.getenv("PREFIX", "").strip() == "":
        return
    installer = Path(__file__).resolve().parent.parent / "scripts" / "termux" / "install_abs_updater_service.sh"
    if installer.exists():
        try:
            subprocess.run(["bash", str(installer)], cwd=installer.parent.parent.parent, check=False, timeout=30)
        except Exception:
            pass


def main() -> None:
    _ensure_updater_service()
    runtime = build_runtime()
    print(f"ABS V1 running at http://{HOST}:{PORT}")
    serve(
        runtime.orchestrator,
        runtime.registry,
        host=HOST,
        port=PORT,
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
