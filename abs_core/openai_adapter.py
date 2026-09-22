from __future__ import annotations

import json
import os
from typing import Any

from .ai_adapters import _post_json


class OpenAICapability:
    """OpenAI Responses API capability for ABS."""

    id = "openai-api"
    name = "OpenAI API"

    def __init__(self, api_key: str | None = None, model: str | None = None, timeout: int = 120) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = model or os.getenv("ABS_OPENAI_MODEL", "gpt-5.6")
        self.timeout = timeout

    def execute(self, objective: str, context: dict[str, Any]) -> dict[str, Any]:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is required for OpenAI API.")
        prompt = objective
        if context:
            prompt += "\n\nABS CONTEXT (JSON):\n" + json.dumps(
                context, ensure_ascii=False, sort_keys=True
            )
        data = _post_json(
            "https://api.openai.com/v1/responses",
            {"Authorization": f"Bearer {self.api_key}"},
            {"model": self.model, "input": prompt},
            self.timeout,
        )
        text = data.get("output_text")
        if not text:
            chunks = []
            for item in data.get("output", []):
                for content in item.get("content", []):
                    if content.get("type") in {"output_text", "text"}:
                        chunks.append(content.get("text", ""))
            text = "".join(chunks)
        if not text:
            raise RuntimeError("OpenAI returned no text output.")
        return {
            "type": "openai_api",
            "model": data.get("model", self.model),
            "response_id": data.get("id"),
            "final_response": text,
        }
