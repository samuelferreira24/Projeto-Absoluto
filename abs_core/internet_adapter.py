from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlparse
from urllib.request import Request, urlopen


class InternetHTTPCapability:
    """Minimal external HTTP retrieval capability.

    It is deliberately a building block, not a browser. Rich navigation and
    JavaScript execution remain a separate browser-runtime capability.
    """

    id = "internet-http"
    name = "Internet HTTP"

    def __init__(self, timeout: int = 30, max_bytes: int = 1_000_000) -> None:
        self.timeout = timeout
        self.max_bytes = max_bytes

    def execute(self, objective: str, context: dict[str, Any]) -> dict[str, Any]:
        url = str(context.get("url") or "").strip()
        if not url:
            raise ValueError("context.url is required for Internet HTTP")
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("only absolute http/https URLs are supported")

        request = Request(
            url,
            headers={"User-Agent": "ABS/1.0 (InternetHTTPCapability)"},
            method="GET",
        )
        with urlopen(request, timeout=self.timeout) as response:
            raw = response.read(self.max_bytes + 1)
            truncated = len(raw) > self.max_bytes
            raw = raw[:self.max_bytes]
            content_type = response.headers.get("Content-Type", "")
            try:
                body: Any = raw.decode("utf-8", errors="replace")
            except Exception:
                body = raw.hex()

        return {
            "type": "internet_http",
            "url": url,
            "status": getattr(response, "status", None),
            "content_type": content_type,
            "truncated": truncated,
            "body": body,
            "objective": objective,
        }
