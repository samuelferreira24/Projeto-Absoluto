from __future__ import annotations

import os

from .api import serve
from .cli import build
from .resources import ResourceManager

HOST = os.getenv("ABS_HOST", "127.0.0.1")
PORT = int(os.getenv("ABS_PORT", "8787"))


def main() -> None:
    orchestrator = build()
    resources = ResourceManager()
    print(f"ABS V1 running at http://{HOST}:{PORT}")
    print("Interface, capabilities and device resources are served by the unified ABS API.")
    serve(orchestrator, orchestrator.registry, host=HOST, port=PORT, resources=resources)


if __name__ == "__main__":
    main()
