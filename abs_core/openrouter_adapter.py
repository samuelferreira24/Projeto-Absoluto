from __future__ import annotations

import json
import os
from typing import Any

from .ai_adapters import _post_json


class OpenRouterCapability:
    """OpenRouter adapter kept behind the ABS intelligence boundary."""

    id = "openrouter"
    name = "OpenRouter"

    def __init__(self, api_key: str | None = None, model: str | None = None, timeout: int = 120) -> None:
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY", "")
        self.model = model or os.getenv("ABS_OPENROUTER_MODEL", "openrouter/free")
        self.timeout = timeout

    def execute(self, objective: str, context: dict[str, Any]) -> dict[str, Any]:
        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY is required for OpenRouter.")
        messages = list((context.get("conversation") or {}).get("messages") or [])
        if not messages or messages[-1].get("content") != objective:
            messages.append({"role": "user", "content": objective})
        payload: dict[str, Any] = {
            "model": context.get("ai_model") or self.model,
            "messages": messages,
        }
        fallbacks = context.get("ai_fallback_models")
        if isinstance(fallbacks, list) and fallbacks:
            payload["models"] = [str(item) for item in fallbacks[:3]]
        data = _post_json(
            "https://openrouter.ai/api/v1/chat/completions",
            {
                "Authorization": f"Bearer {self.api_key}",
                "HTTP-Referer": os.getenv("OPENROUTER_HTTP_REFERER", ""),
                "X-Title": os.getenv("OPENROUTER_X_TITLE", "ABS"),
            },
            payload,
            self.timeout,
        )
        choices = data.get("choices") or []
        if not choices:
            raise RuntimeError("OpenRouter returned no choices.")
        message = choices[0].get("message") or {}
        text = message.get("content") or ""
        if not text:
            raise RuntimeError("OpenRouter returned no text content.")
        return {
            "type": "openrouter",
            "model": data.get("model", payload["model"]),
            "response_id": data.get("id"),
            "usage": data.get("usage"),
            "final_response": text,
        }
