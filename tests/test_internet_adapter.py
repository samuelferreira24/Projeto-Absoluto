from types import SimpleNamespace

import pytest

from abs_core.internet_adapter import InternetHTTPCapability


def test_internet_http_requires_absolute_url():
    with pytest.raises(ValueError):
        InternetHTTPCapability().execute("fetch", {"url": "localhost"})


def test_internet_http_retrieves_bounded_response(monkeypatch):
    class FakeResponse:
        status = 200
        headers = {"Content-Type": "text/plain"}
        def read(self, size):
            assert size == 1001
            return b"hello"
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False

    monkeypatch.setattr("abs_core.internet_adapter.urlopen", lambda *args, **kwargs: FakeResponse())
    result = InternetHTTPCapability(max_bytes=1000).execute(
        "read", {"url": "https://example.com"}
    )
    assert result["status"] == 200
    assert result["body"] == "hello"
    assert result["truncated"] is False
