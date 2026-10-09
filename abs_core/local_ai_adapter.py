from __future__ import annotations

import os
from typing import Any
from .ai_adapters import _post_json
from .cognitive_context import build_system_context


class LocalAICapability:
    """Local intelligence adapter."""

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
        external_results = context.get("external_results") or []
        system_context = build_system_context(
            context.get("_capabilities") or [],
            external_results,
        )

        # O contexto do ABS fica separado do histórico da conversa.
        messages.insert(0, {"role": "system", "content": system_context})

        if not messages:
            messages = [{"role": "user", "content": objective}]
        elif not (
            isinstance(messages[-1], dict)
            and messages[-1].get("role") == "user"
            and messages[-1].get("content") == objective
        ):
            messages.append({"role": "user", "content": objective})

        endpoint = self.endpoint.rstrip("/")
        if not endpoint.endswith("/chat/completions"):
            endpoint += "/v1/chat/completions"

        try:
            max_tokens = int(context.get("max_tokens", os.getenv("ABS_LOCAL_AI_MAX_TOKENS", "256")))
        except (TypeError, ValueError):
            max_tokens = 256
        max_tokens = max(1, min(max_tokens, 2048))

        try:
            temperature = float(context.get("temperature", os.getenv("ABS_LOCAL_AI_TEMPERATURE", "0.2")))
        except (TypeError, ValueError):
            temperature = 0.2
        temperature = max(0.0, min(temperature, 2.0))

        think = context.get("think")
        if think is None:
            think = os.getenv("ABS_LOCAL_AI_THINK", "false").strip().lower() in {"1", "true", "yes", "on"}

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False,
            "think": bool(think),
        }
        if "keep_alive" in context:
            payload["keep_alive"] = context["keep_alive"]

        data = _post_json(endpoint, {}, payload, self.timeout)
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
