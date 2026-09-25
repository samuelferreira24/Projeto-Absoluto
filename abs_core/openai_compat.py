from __future__ import annotations

"""Small OpenAI-compatible facade for external interfaces such as Open WebUI."""

import json
import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from .runtime import build_runtime


class OpenAICompatHandler(BaseHTTPRequestHandler):
    runtime = None

    def _send(self, status: int, payload: dict[str, Any]) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        if self.path == "/v1/models":
            models = []
            for item in self.runtime.intelligence.list():
                models.append({"id": item.id, "object": "model", "owned_by": "abs", "metadata": item.public()})
            self._send(200, {"object": "list", "data": models})
            return
        self._send(404, {"error": {"message": "not_found", "type": "invalid_request_error"}})

    def do_POST(self) -> None:
        if self.path != "/v1/chat/completions":
            self._send(404, {"error": {"message": "not_found", "type": "invalid_request_error"}})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(size).decode("utf-8"))
            messages = data.get("messages") or []
            if not messages:
                raise ValueError("messages_required")
            latest = messages[-1]
            content = latest.get("content", "") if isinstance(latest, dict) else str(latest)
            if isinstance(content, list):
                content = "".join(str(x.get("text", "")) for x in content if isinstance(x, dict))
            model = data.get("model")
            preferred = model if model in {x.id for x in self.runtime.intelligence.list()} else None
            context = {
                "conversation": {"messages": messages},
                "ai_model": data.get("model") if preferred else None,
            }
            result = self.runtime.cognitive_runtime.turn(str(content), preferred_resource=preferred, context=context, approved=False)
            now = int(time.time())
            self._send(200, {
                "id": f"abs-{result['work_id']}", "object": "chat.completion", "created": now,
                "model": result["resource"]["id"],
                "choices": [{"index": 0, "message": {"role": "assistant", "content": result["response"]}, "finish_reason": "stop"}],
                "usage": {},
                "abs": {"session_id": result["session_id"], "work_id": result["work_id"], "verification": result.get("verification")},
            })
        except PermissionError as exc:
            self._send(403, {"error": {"message": str(exc), "type": "approval_required"}})
        except (KeyError, ValueError, RuntimeError) as exc:
            self._send(400, {"error": {"message": str(exc), "type": "invalid_request_error"}})


def main() -> None:
    host = os.getenv("ABS_OPENAI_COMPAT_HOST", "127.0.0.1")
    port = int(os.getenv("ABS_OPENAI_COMPAT_PORT", "8788"))
    OpenAICompatHandler.runtime = build_runtime()
    print(f"ABS OpenAI-compatible gateway at http://{host}:{port}/v1")
    ThreadingHTTPServer((host, port), OpenAICompatHandler).serve_forever()


if __name__ == "__main__":
    main()
