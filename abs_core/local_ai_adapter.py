from __future__ import annotations

import json
import os
from typing import Any
from .ai_adapters import _post_json


class LocalAICapability:
    """Local intelligence adapter.

    The endpoint is intentionally generic: any local runtime exposing an
    OpenAI-compatible /chat/completions endpoint can be used. This keeps the
    ABS independent from a particular local model runtime.
    """

    id = "local-ai"
    name = "IA local"

    def __init__(self, endpoint: str | None = None, model: str | None = None, timeout: int = 120) -> None:
        self.endpoint = endpoint or os.getenv("ABS_LOCAL_AI_URL", "")
        self.model = model or os.getenv("ABS_LOCAL_AI_MODEL", "local")
        self.timeout = timeout

    def execute(self, objective: str, context: dict[str, Any]) -> dict[str, Any]:
        if not self.endpoint:
            raise RuntimeError("ABS_LOCAL_AI_URL is required for local intelligence.")

        messages = list((context.get("conversation") or {}).get("messages") or [])
        if not messages:
            messages = [{"role": "user", "content": objective}]
        elif messages[-1].get("content") != objective:
            messages.append({"role": "user", "content": objective})

        endpoint = self.endpoint.rstrip("/")
        if not endpoint.endswith("/chat/completions"):
            endpoint += "/v1/chat/completions"

        data = _post_json(
            endpoint,
            {},
            {"model": self.model, "messages": messages},
            self.timeout,
        )
        choices = data.get("choices") or []
        if not choices:
            raise RuntimeError("Local AI returned no choices.")
        message = choices[0].get("message") or {}
        text = message.get("content")
        if isinstance(text, list):
            text = "".join(
                item.get("text", "") for item in text
                if isinstance(item, dict) and item.get("type") == "text"
            )
        if not text:
            raise RuntimeError("Local AI returned no text content.")
        return {
            "type": "local_ai",
            "model": data.get("model", self.model),
            "final_response": text,
        }
