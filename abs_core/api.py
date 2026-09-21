import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from .orchestrator import Orchestrator
from .resources import ResourceManager

WEB_INDEX = Path(__file__).resolve().parent.parent / "20_interface" / "web" / "index.html"
WEB_MANIFEST = WEB_INDEX.parent / "manifest.webmanifest"
WEB_SW = WEB_INDEX.parent / "sw.js"


class ABSHandler(BaseHTTPRequestHandler):
    orchestrator: Orchestrator | None = None
    registry = None
    resources: ResourceManager | None = None
    started_at = time.time()

    def _send(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path, content_type: str) -> None:
        if not path.exists():
            self._send(404, {"error": "asset_not_found"})
            return
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self._send_file(WEB_INDEX, "text/html; charset=utf-8")
            return
        if self.path == "/manifest.webmanifest":
            self._send_file(WEB_MANIFEST, "application/manifest+json")
            return
        if self.path == "/sw.js":
            self._send_file(WEB_SW, "application/javascript; charset=utf-8")
            return
        if self.path == "/health":
            self._send(200, {
                "name": "ABS",
                "status": "alive",
                "version": "v1",
                "uptime_seconds": round(time.time() - self.started_at, 3),
            })
            return
        if self.path == "/capabilities":
            self._send(200, {
                "capabilities": [
                    {"id": c.id, "name": c.name, "kind": c.kind}
                    for c in self.registry.list()
                ]
            })
            return
        if self.path == "/devices":
            self._send(200, {
                "devices": [d.public() for d in self.resources.list()],
                "summary": self.resources.summary(),
            })
            return
        if self.path.startswith("/works/"):
            work_id = self.path.split("/", 2)[2]
            try:
                w = self.orchestrator.store.load(work_id)
            except KeyError:
                self._send(404, {"error": "work_not_found"})
                return
            self._send(200, {
                "id": w.id, "objective": w.objective, "state": w.state.value,
                "capability_id": w.capability_id, "result": w.result,
                "provenance": w.provenance,
                "events": [e.__dict__ for e in w.events],
            })
            return
        self._send(404, {"error": "not_found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        try:
            data = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            self._send(400, {"error": "invalid_json"})
            return

        if self.path == "/works":
            if not data.get("objective"):
                self._send(400, {"error": "objective_required"})
                return
            w = self.orchestrator.create(data["objective"], data.get("context"))
            self._send(201, {"id": w.id, "state": w.state.value})
            return

        if self.path.startswith("/works/") and self.path.endswith("/run"):
            work_id = self.path.split("/")[2]
            try:
                w = self.orchestrator.run(
                    work_id,
                    data.get("capability_id"),
                    bool(data.get("approved", False)),
                )
            except PermissionError as exc:
                self._send(403, {"error": "approval_required", "detail": str(exc)})
                return
            except KeyError:
                self._send(404, {"error": "work_not_found"})
                return
            self._send(200, {
                "id": w.id, "state": w.state.value, "result": w.result,
                "provenance": w.provenance,
            })
            return

        if self.path == "/devices/register":
            if not data.get("name"):
                self._send(400, {"error": "device_name_required"})
                return
            device = self.resources.register(
                name=data["name"],
                kind=data.get("kind", "unknown"),
                endpoint=data.get("endpoint"),
                capabilities=data.get("capabilities"),
                metadata=data.get("metadata"),
                device_id=data.get("id"),
            )
            self._send(201, {"device": device.public()})
            return

        if self.path.startswith("/devices/") and self.path.endswith("/heartbeat"):
            device_id = self.path.split("/")[2]
            try:
                device = self.resources.heartbeat(device_id, data.get("status", "online"))
            except KeyError:
                self._send(404, {"error": "device_not_found"})
                return
            self._send(200, {"device": device.public()})
            return

        if self.path.startswith("/works/") and self.path.endswith("/pause"):
            work_id = self.path.split("/")[2]
            try:
                w = self.orchestrator.pause(work_id)
            except KeyError:
                self._send(404, {"error": "work_not_found"})
                return
            self._send(200, {"id": w.id, "state": w.state.value})
            return

        self._send(404, {"error": "not_found"})


def serve(orchestrator: Orchestrator, registry, host="127.0.0.1", port=8787, resources=None):
    ABSHandler.orchestrator = orchestrator
    ABSHandler.registry = registry
    ABSHandler.resources = resources or ResourceManager()
    ABSHandler.started_at = time.time()
    server = ThreadingHTTPServer((host, port), ABSHandler)
    server.serve_forever()
