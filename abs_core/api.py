import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from .orchestrator import Orchestrator
from .resources import ResourceManager
from .interface_runtime import InterfaceRuntime
from .connections import ConnectionRegistry
from .resource_router import ResourceRouteRequest, ResourceRouter
from . import update_manager

WEB_INDEX = Path(__file__).resolve().parent.parent / "20_interface" / "web" / "index.html"
WEB_MANIFEST = WEB_INDEX.parent / "manifest.webmanifest"
WEB_SW = WEB_INDEX.parent / "sw.js"


class ABSHandler(BaseHTTPRequestHandler):
    orchestrator: Orchestrator | None = None
    registry = None
    resources: ResourceManager | None = None
    interface_runtime: InterfaceRuntime | None = None
    connections: ConnectionRegistry | None = None
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
        if self.path == "/interface/state":
            self._send(200, self.interface_runtime.public_state())
            return
        if self.path == "/interface/modes":
            self._send(200, {"modes": self.interface_runtime.public_modes()})
            return
        if self.path == "/interface/inputs":
            self._send(200, {"inputs": self.interface_runtime.list_inputs()})
            return
        if self.path == "/update/status":
            try:
                self._send(200, update_manager.status())
            except Exception as exc:
                self._send(503, {"error": "update_status_failed", "detail": str(exc)})
            return
        if self.path == "/connections":
            self._send(200, {"connections": self.connections.public()})
            return
        if self.path == "/health":
            self._send(200, {
                "name": "ABS",
                "status": "alive",
                "version": "v1",
                "uptime_seconds": round(time.time() - self.started_at, 3),
                "connection_count": len(self.connections.list()),
                "auto_update": True,
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

        if self.path in {"/update/apply", "/update/rollback"}:
            if data.get("approved") is not True:
                self._send(403, {"error": "approval_required", "detail": "Explicit update authorization required."})
                return
            try:
                result = update_manager.apply() if self.path == "/update/apply" else update_manager.rollback()
            except Exception as exc:
                self._send(500, {"error": "update_failed", "detail": str(exc)})
                return
            self._send(200, result)
            return

        if self.path == "/resources/select":
            objective = str(data.get("objective") or "").strip()
            if not objective:
                self._send(400, {"error": "objective_required"})
                return
            request = ResourceRouteRequest(
                objective=objective,
                required_capabilities=tuple(data.get("required_capabilities") or []),
                preferred_categories=tuple(data.get("preferred_categories") or []),
                preferred_transports=tuple(data.get("preferred_transports") or []),
                allowed_connections=tuple(data.get("allowed_connections") or []),
                excluded_connections=tuple(data.get("excluded_connections") or []),
                require_configured=bool(data.get("require_configured", False)),
                context=data.get("context") if isinstance(data.get("context"), dict) else {},
            )
            routes = ResourceRouter(self.connections).rank(request)
            self._send(200, {"objective": objective, "routes": [
                {"connection_id": route.connection_id, "score": route.score,
                 "reasons": list(route.reasons), "connection": route.connection}
                for route in routes
            ]})
            return

        if self.path == "/interface/mode":
            mode_id = data.get("mode_id")
            if not mode_id:
                self._send(400, {"error": "mode_id_required"})
                return
            try:
                self.interface_runtime.set_mode(str(mode_id))
            except KeyError:
                self._send(404, {"error": "interface_mode_not_found"})
                return
            self._send(200, self.interface_runtime.public_state())
            return

        if self.path == "/interface/input":
            channel = data.get("channel")
            if not channel:
                self._send(400, {"error": "input_channel_required"})
                return
            try:
                self.interface_runtime.set_input(str(channel))
            except KeyError:
                self._send(404, {"error": "interface_input_not_found"})
                return
            self._send(200, self.interface_runtime.public_state())
            return

        if self.path == "/interface/context":
            values = data.get("context")
            if not isinstance(values, dict):
                self._send(400, {"error": "context_object_required"})
                return
            self.interface_runtime.update_context(**values)
            self._send(200, self.interface_runtime.public_state())
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


def serve(orchestrator: Orchestrator, registry, host="127.0.0.1", port=8787,
          resources=None, interface_runtime=None, connections=None):
    ABSHandler.orchestrator = orchestrator
    ABSHandler.registry = registry
    ABSHandler.resources = resources or ResourceManager()
    ABSHandler.interface_runtime = interface_runtime or InterfaceRuntime()
    ABSHandler.connections = connections or ConnectionRegistry.defaults()
    ABSHandler.started_at = time.time()
    server = ThreadingHTTPServer((host, port), ABSHandler)
    server.serve_forever()
