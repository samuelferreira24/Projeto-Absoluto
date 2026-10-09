from __future__ import annotations

"""Safety-bounded Chromium DevTools adapter for ABS.

The CDP endpoint must be bound to loopback and must never be exposed publicly.
Navigation requires explicit approval and rejects local/private destinations.
"""

import ipaddress
import json
import os
import socket
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen


class BrowserCapability:
    id = "browser-control"
    name = "ABS Browser Control"

    def __init__(self, endpoint: str | None = None, timeout: float = 4.0) -> None:
        self.endpoint = (endpoint or os.getenv("ABS_BROWSER_CDP_URL", "http://127.0.0.1:9222")).rstrip("/")
        parsed = urlparse(self.endpoint)
        if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
            raise ValueError("browser_cdp_endpoint_must_be_loopback_http")
        self.timeout = timeout
        self.allowed_hosts = {
            h.strip().lower().rstrip(".")
            for h in os.getenv("ABS_BROWSER_ALLOWED_HOSTS", "").split(",")
            if h.strip()
        }

    def _request(self, path: str, method: str = "GET") -> Any:
        req = Request(self.endpoint + path, method=method, headers={"Accept": "application/json"})
        try:
            with urlopen(req, timeout=self.timeout) as response:
                raw = response.read(1024 * 1024)
                return json.loads(raw.decode("utf-8")) if raw else {}
        except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
            raise RuntimeError(f"browser_cdp_unavailable:{type(exc).__name__}") from None

    def _validate_url(self, raw_url: str) -> str:
        url = str(raw_url or "").strip()
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError("browser_url_must_be_http_or_https")
        if parsed.username or parsed.password:
            raise ValueError("browser_url_credentials_forbidden")
        host = parsed.hostname.lower().rstrip(".")
        if host in {"localhost", "metadata.google.internal"} or host.endswith((".localhost", ".local", ".internal")):
            raise ValueError("browser_local_destination_forbidden")
        try:
            ip = ipaddress.ip_address(host)
        except ValueError:
            ip = None
        if ip is not None and not ip.is_global:
            raise ValueError("browser_private_destination_forbidden")
        if self.allowed_hosts and host not in self.allowed_hosts and not any(host.endswith("." + h) for h in self.allowed_hosts):
            raise ValueError("browser_host_not_allowlisted")
        if ip is None:
            # Always resolve hostnames, including allowlisted ones, and reject any
            # non-global result to reduce DNS-based SSRF/rebinding risk.
            try:
                addresses = {
                    ipaddress.ip_address(item[4][0])
                    for item in socket.getaddrinfo(
                        host,
                        parsed.port or (443 if parsed.scheme == "https" else 80),
                        type=socket.SOCK_STREAM,
                    )
                }
            except OSError:
                raise ValueError("browser_host_resolution_failed") from None
            if not addresses or any(not address.is_global for address in addresses):
                raise ValueError("browser_private_destination_forbidden")
        return url

    def execute(self, objective: str, context: dict[str, Any]) -> dict[str, Any]:
        action = str(context.get("action", "status")).strip().lower()
        if action == "status":
            version = self._request("/json/version")
            return {"type": "browser_status", "available": True, "browser": version.get("Browser"), "webSocketDebuggerUrl": None}
        if action == "list_tabs":
            tabs = self._request("/json/list")
            return {
                "type": "browser_tabs",
                "tabs": [
                    {"id": t.get("id"), "title": t.get("title"), "url": t.get("url"), "type": t.get("type")}
                    for t in tabs if isinstance(t, dict) and t.get("type") == "page"
                ],
            }
        if action == "open_url":
            if context.get("approved") is not True:
                raise PermissionError("browser_navigation_requires_explicit_approval")
            url = self._validate_url(str(context.get("url") or ""))
            target = self._request("/json/new?" + quote(url, safe=":/?&=#%"), method="PUT")
            return {
                "type": "browser_navigation",
                "opened": True,
                "target_id": target.get("id"),
                "url": target.get("url", url),
                "title": target.get("title"),
            }
        raise ValueError("unsupported_browser_action")
