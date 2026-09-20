import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
from .orchestrator import Orchestrator

class ABSHandler(BaseHTTPRequestHandler):
    orchestrator: Orchestrator | None = None
    registry = None

    def _send(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            from pathlib import Path
            html = (Path(__file__).resolve().parent.parent / "web" / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html)))
            self.end_headers()
            self.wfile.write(html)
            return
        if self.path == "/capabilities":
            self._send(200, {"capabilities": [{"id": c.id, "name": c.name, "kind": c.kind} for c in self.registry.list()]})
            return
        if self.path.startswith("/works/"):
            work_id = self.path.split("/", 2)[2]
            try:
                w = self.orchestrator.store.load(work_id)
            except KeyError:
                self._send(404, {"error": "work_not_found"}); return
            self._send(200, {"id": w.id, "objective": w.objective, "state": w.state.value, "capability_id": w.capability_id, "result": w.result, "provenance": w.provenance, "events": [e.__dict__ for e in w.events]})
            return
        self._send(404, {"error": "not_found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        try: data = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError: self._send(400, {"error": "invalid_json"}); return
        if self.path == "/works":
            w = self.orchestrator.create(data["objective"], data.get("context"))
            self._send(201, {"id": w.id, "state": w.state.value}); return
        if self.path.startswith("/works/") and self.path.endswith("/run"):
            work_id = self.path.split("/")[2]
            try:
                w = self.orchestrator.run(work_id, data.get("capability_id"), bool(data.get("approved", False)))
            except PermissionError as exc:
                self._send(403, {"error": "approval_required", "detail": str(exc)}); return
            self._send(200, {"id": w.id, "state": w.state.value, "result": w.result, "provenance": w.provenance}); return
        if self.path.startswith("/works/") and self.path.endswith("/pause"):
            work_id = self.path.split("/")[2]
            w = self.orchestrator.pause(work_id)
            self._send(200, {"id": w.id, "state": w.state.value}); return
        self._send(404, {"error": "not_found"})

def serve(orchestrator: Orchestrator, registry, host="127.0.0.1", port=8787):
    ABSHandler.orchestrator = orchestrator
    ABSHandler.registry = registry
    server = ThreadingHTTPServer((host, port), ABSHandler)
    server.serve_forever()
