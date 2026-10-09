import pytest
import socket

from abs_core.browser_adapter import BrowserCapability


def test_cdp_endpoint_must_be_loopback():
    with pytest.raises(ValueError, match="loopback"):
        BrowserCapability("http://0.0.0.0:9222")


def test_status_does_not_expose_websocket_endpoint(monkeypatch):
    adapter = BrowserCapability("http://127.0.0.1:9222")
    monkeypatch.setattr(adapter, "_request", lambda path, method="GET": {"Browser": "Chromium", "webSocketDebuggerUrl": "ws://secret"})
    result = adapter.execute("status", {"action": "status"})
    assert result["available"] is True
    assert result["browser"] == "Chromium"
    assert result["webSocketDebuggerUrl"] is None


def test_navigation_requires_explicit_approval(monkeypatch):
    adapter = BrowserCapability("http://127.0.0.1:9222")
    monkeypatch.setattr(adapter, "_request", lambda *args, **kwargs: pytest.fail("must not call CDP"))
    with pytest.raises(PermissionError, match="approval"):
        adapter.execute("open", {"action": "open_url", "url": "https://example.com", "approved": False})


@pytest.mark.parametrize("url", [
    "file:///etc/passwd",
    "javascript:alert(1)",
    "http://127.0.0.1/",
    "http://10.0.0.2/",
    "http://169.254.169.254/latest/meta-data/",
    "http://user:pass@example.com/",
    "http://localhost/",
])
def test_unsafe_urls_rejected(url):
    adapter = BrowserCapability("http://127.0.0.1:9222")
    with pytest.raises(ValueError):
        adapter._validate_url(url)


def test_allowlisted_public_host_navigation(monkeypatch):
    adapter = BrowserCapability("http://127.0.0.1:9222")
    adapter.allowed_hosts = {"example.com"}
    monkeypatch.setattr(
        "abs_core.browser_adapter.socket.getaddrinfo",
        lambda *args, **kwargs: [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))],
    )
    calls = []
    monkeypatch.setattr(adapter, "_request", lambda path, method="GET": calls.append((path, method)) or {"id": "tab1", "url": "https://example.com/"})
    result = adapter.execute("open", {"action": "open_url", "url": "https://example.com/", "approved": True})
    assert result["opened"] is True
    assert result["target_id"] == "tab1"
    assert calls and calls[0][1] == "PUT"


def test_allowlisted_host_resolving_private_ip_is_rejected(monkeypatch):
    adapter = BrowserCapability("http://127.0.0.1:9222")
    adapter.allowed_hosts = {"example.com"}
    monkeypatch.setattr(
        "abs_core.browser_adapter.socket.getaddrinfo",
        lambda *args, **kwargs: [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("10.0.0.8", 443))],
    )
    with pytest.raises(ValueError, match="private_destination"):
        adapter._validate_url("https://example.com/")


def test_navigation_rejects_non_allowlisted_host():
    adapter = BrowserCapability("http://127.0.0.1:9222")
    adapter.allowed_hosts = {"example.com"}
    with pytest.raises(ValueError, match="allowlisted"):
        adapter._validate_url("https://evil.example/")
