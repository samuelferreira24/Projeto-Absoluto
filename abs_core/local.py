from __future__ import annotations

import json
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .cli import build

HOST = os.getenv("ABS_HOST", "127.0.0.1")
PORT = int(os.getenv("ABS_PORT", "8787"))

class LocalABS:
    def __init__(self) -> None:
        self.orchestrator = build()
        self.started_at = time.time()

    def task(self, payload: dict[str, Any]) -> dict[str, Any]:
        objective = str(payload["objective"])
        context = payload.get("context") or {}
        capability_id = payload.get("capability_id")
        approved = bool(payload.get("approved", False))
        work = self.orchestrator.create(objective, context=context)
        result = self.orchestrator.run(work.id, capability_id=capability_id, approved=approved)
        return {
            "id": result.id,
            "state": result.state.value,
            "objective": result.objective,
            "capability_id": result.capability_id,
            "result": result.result,
            "provenance": result.provenance,
        }

ABS = LocalABS()

class Handler(BaseHTTPRequestHandler):
    def _json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/health":
            self._json(200, {
                "name": "ABS",
                "status": "alive",
                "version": "v1",
                "uptime_seconds": round(time.time() - ABS.started_at, 3),
                "update_manager": "external",
            })
            return
        if self.path == "/capabilities":
            self._json(200, {
                "capabilities": [
                    {"id": c.id, "name": c.name, "kind": c.kind}
                    for c in ABS.orchestrator.registry.list()
                ]
            })
            return
        if self.path.startswith("/works/"):
            work_id = self.path.split("/", 2)[2]
            try:
                work = ABS.orchestrator.store.load(work_id)
            except KeyError:
                self._json(404, {"error": "work_not_found"})
                return
            self._json(200, {
                "id": work.id,
                "objective": work.objective,
                "state": work.state.value,
                "capability_id": work.capability_id,
                "result": work.result,
                "provenance": work.provenance,
                "events": [e.__dict__ for e in work.events],
            })
            return
        self._json(404, {"error": "not_found"})

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            self._json(400, {"error": "invalid_json"})
            return
        if self.path == "/task":
            if not payload.get("objective"):
                self._json(400, {"error": "objective_required"})
                return
            try:
                self._json(200, ABS.task(payload))
            except PermissionError as exc:
                self._json(403, {"error": "approval_required", "detail": str(exc)})
            except Exception as exc:
                self._json(500, {"error": type(exc).__name__, "detail": str(exc)})
            return
        self._json(404, {"error": "not_found"})

def main() -> None:
    if AUTO_UPDATE:
        threading.Thread(target=_auto_update_loop, daemon=True).start()
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"ABS local V1 running at http://{HOST}:{PORT}")
    print("Update manager: external")
    server.serve_forever()

if __name__ == "__main__":
    main()
