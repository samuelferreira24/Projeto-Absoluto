from __future__ import annotations

import json
import os
from typing import Any
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def _post_json(url: str, headers: dict[str, str], payload: dict[str, Any], timeout: int = 120) -> dict[str, Any]:
    request = Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json", **headers},
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"AI API HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"AI API connection failed: {exc.reason}") from exc


class ClaudeCapability:
    id = "claude"
    name = "Anthropic Claude API"

    def __init__(self, api_key: str | None = None, model: str | None = None, timeout: int = 120) -> None:
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY", "")
        self.model = model or os.getenv("ABS_CLAUDE_MODEL", "claude-sonnet-5")
        self.timeout = timeout

    def execute(self, objective: str, context: dict[str, Any]) -> dict[str, Any]:
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is required for Claude.")
        prompt = objective
        if context:
            prompt += "\n\nABS CONTEXT (JSON):\n" + json.dumps(context, ensure_ascii=False, sort_keys=True)
        payload = {
            "model": self.model,
            "max_tokens": int(os.getenv("ABS_CLAUDE_MAX_TOKENS", "2048")),
            "messages": [{"role": "user", "content": prompt}],
        }
        data = _post_json(
            "https://api.anthropic.com/v1/messages",
            {"x-api-key": self.api_key, "anthropic-version": "2023-06-01"},
            payload,
            self.timeout,
        )
        text = "".join(
            block.get("text", "") for block in data.get("content", [])
            if block.get("type") == "text"
        )
        if not text:
            raise RuntimeError("Claude returned no text content.")
        return {"type": "claude_api", "model": data.get("model", self.model),
                "message_id": data.get("id"), "final_response": text}


class GeminiCapability:
    id = "gemini"
    name = "Google Gemini API"

    def __init__(self, api_key: str | None = None, model: str | None = None, timeout: int = 120) -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.model = model or os.getenv("ABS_GEMINI_MODEL", "gemini-3.8-flash")
        self.timeout = timeout

    def execute(self, objective: str, context: dict[str, Any]) -> dict[str, Any]:
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is required for Gemini.")
        prompt = objective
        if context:
            prompt += "\n\nABS CONTEXT (JSON):\n" + json.dumps(context, ensure_ascii=False, sort_keys=True)
        payload = {"model": self.model, "input": prompt}
        data = _post_json(
            os.getenv("ABS_GEMINI_ENDPOINT", "https://generativelanguage.googleapis.com/v1/interactions"),
            {"x-goog-api-key": self.api_key},
            payload,
            self.timeout,
        )
        text = data.get("output_text")
        if not text:
            for step in data.get("steps", []):
                for block in step.get("content", []):
                    if block.get("type") == "text":
                        text = (text or "") + block.get("text", "")
        if not text:
            raise RuntimeError("Gemini returned no text output.")
        return {"type": "gemini_api", "model": data.get("model", self.model),
                "interaction_id": data.get("id"), "final_response": text}
