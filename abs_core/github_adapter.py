from __future__ import annotations

import base64
import json
import os
import urllib.parse
import urllib.request
from typing import Any


class GitHubCapability:
    """Read-only GitHub capability for ABS.

    It uses the GitHub REST API directly. Public repositories work without a
    token; ABS_GITHUB_TOKEN can be supplied later for authenticated access and
    higher rate limits. Write operations are intentionally outside this first
    capability.
    """

    id = "github"
    name = "GitHub"
    kind = "external_service"

    def __init__(
        self,
        *,
        api_url: str | None = None,
        token: str | None = None,
        default_repo: str | None = None,
    ) -> None:
        self.api_url = (api_url or os.getenv("ABS_GITHUB_API_URL") or "https://api.github.com").rstrip("/")
        self.token = token if token is not None else os.getenv("ABS_GITHUB_TOKEN")
        self.default_repo = default_repo or os.getenv(
            "ABS_GITHUB_REPO", "samuelferreira24/Projeto-Absoluto"
        )

    def _request(self, path: str, *, query: dict[str, str] | None = None) -> Any:
        url = f"{self.api_url}/{path.lstrip('/')}"
        if query:
            url = f"{url}?{urllib.parse.urlencode(query)}"
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "Projeto-Absoluto-ABS",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))

    def execute(self, objective: str, context: dict[str, Any]) -> dict[str, Any]:
        action = str(context.get("action") or "repository").strip().lower()
        repo = str(context.get("repo") or self.default_repo).strip()

        if action == "repository":
            data = self._request(f"repos/{repo}")
            return {
                "type": "github.repository",
                "repository": data,
                "objective": objective,
            }

        if action == "file":
            path = str(context.get("path") or "").strip().lstrip("/")
            if not path:
                raise ValueError("github_file_path_required")
            ref = str(context.get("ref") or "").strip()
            endpoint = f"repos/{repo}/contents/{urllib.parse.quote(path, safe='/')}"
            data = self._request(endpoint, query={"ref": ref} if ref else None)
            if isinstance(data, list):
                raise ValueError("github_path_is_directory")
            content = data.get("content")
            if data.get("encoding") == "base64" and content:
                content = base64.b64decode(content).decode("utf-8")
            return {
                "type": "github.file",
                "repository": repo,
                "path": path,
                "ref": ref or None,
                "sha": data.get("sha"),
                "content": content,
                "html_url": data.get("html_url"),
                "objective": objective,
            }

        if action == "directory":
            path = str(context.get("path") or "").strip().lstrip("/")
            endpoint = f"repos/{repo}/contents/{urllib.parse.quote(path, safe='/')}" if path else f"repos/{repo}/contents"
            data = self._request(endpoint)
            if not isinstance(data, list):
                raise ValueError("github_path_is_file")
            return {
                "type": "github.directory",
                "repository": repo,
                "path": path,
                "items": [
                    {
                        "name": item.get("name"),
                        "path": item.get("path"),
                        "type": item.get("type"),
                        "sha": item.get("sha"),
                        "html_url": item.get("html_url"),
                    }
                    for item in data
                ],
                "objective": objective,
            }

        if action == "search":
            query = str(context.get("query") or "").strip()
            if not query:
                raise ValueError("github_search_query_required")
            scoped = f"{query} repo:{repo}" if " repo:" not in query else query
            data = self._request(
                "search/code",
                query={"q": scoped, "per_page": str(min(int(context.get("limit", 20)), 100))},
            )
            return {
                "type": "github.search",
                "repository": repo,
                "query": query,
                "total_count": data.get("total_count", 0),
                "items": [
                    {
                        "name": item.get("name"),
                        "path": item.get("path"),
                        "sha": item.get("sha"),
                        "html_url": item.get("html_url"),
                    }
                    for item in data.get("items", [])
                ],
                "objective": objective,
            }

        raise ValueError(f"unsupported_github_action:{action}")
