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

        base_endpoint = self.endpoint.rstrip("/")

        try:
            max_tokens = int(context.get("max_tokens", os.getenv("ABS_LOCAL_AI_MAX_TOKENS", "96")))
        except (TypeError, ValueError):
            max_tokens = 96
        max_tokens = max(1, min(max_tokens, 1024))

        # Keep the runtime context explicit: model defaults can allocate a KV cache
        # far larger than the VPS can sustain. Ollama expects num_ctx in options.
        try:
            num_ctx = int(context.get("num_ctx", os.getenv("ABS_LOCAL_AI_NUM_CTX", "2048")))
        except (TypeError, ValueError):
            num_ctx = 2048
        num_ctx = max(512, min(num_ctx, 8192))

        try:
            temperature = float(context.get("temperature", os.getenv("ABS_LOCAL_AI_TEMPERATURE", "0.2")))
        except (TypeError, ValueError):
            temperature = 0.2
        temperature = max(0.0, min(temperature, 2.0))

        think = context.get("think")
        if think is None:
            think = os.getenv("ABS_LOCAL_AI_THINK", "false").strip().lower() in {"1", "true", "yes", "on"}

        try:
            timeout = int(context.get("timeout", self.timeout))
        except (TypeError, ValueError):
            timeout = self.timeout
        timeout = max(1, min(timeout, 300))

        native_ollama = base_endpoint.startswith(("http://127.0.0.1:11434", "http://localhost:11434"))
        if native_ollama:
            native_endpoint = base_endpoint
            if native_endpoint.endswith("/v1"):
                native_endpoint = native_endpoint[:-3]
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "think": bool(think),
                "options": {"num_predict": max_tokens, "temperature": temperature, "num_ctx": num_ctx},
            }
            if "keep_alive" in context:
                payload["keep_alive"] = context["keep_alive"]
            data = _post_json(f"{native_endpoint}/api/chat", {}, payload, timeout)
            message = data.get("message") or {}
            text = message.get("content")
            if not text and message.get("thinking"):
                text = message.get("thinking")
        else:
            endpoint = base_endpoint
            if not endpoint.endswith("/chat/completions"):
                endpoint += "/v1/chat/completions"
            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": False,
            }
            data = _post_json(endpoint, {}, payload, timeout)
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
