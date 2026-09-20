from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

from .cli import build


class GitHubIssueBridge:
    """Poll GitHub Issues and execute approved ABS tasks locally."""

    def __init__(self, repo=None, token=None, interval=None, max_tasks=None):
        self.repo = repo or os.getenv("ABS_GITHUB_REPO", "")
        self.token = token or os.getenv("ABS_GITHUB_TOKEN", "")
        self.interval = interval or int(os.getenv("ABS_BRIDGE_INTERVAL", "15"))
        self.max_tasks = max_tasks or int(os.getenv("ABS_BRIDGE_MAX_TASKS", "1"))
        if not self.repo:
            raise RuntimeError("ABS_GITHUB_REPO is required (owner/repo).")
        if not self.token:
            raise RuntimeError("ABS_GITHUB_TOKEN is required.")
        self.base_url = f"https://api.github.com/repos/{self.repo}"
        self.orchestrator = build()

    def _request(self, method, path, body=None):
        data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
        req = urllib.request.Request(
            self.base_url + path,
            data=data,
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "Projeto-Absoluto-ABS-Bridge",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                raw = response.read()
                return json.loads(raw.decode("utf-8")) if raw else None
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"GitHub API {exc.code}: {detail}") from exc

    def _pending_issues(self):
        issues = self._request("GET", "/issues?state=open&per_page=20")
        return [
            issue for issue in issues
            if issue.get("pull_request") is None
            and str(issue.get("title", "")).startswith("[ABS]")
        ]

    @staticmethod
    def _task_from_issue(issue):
        body = issue.get("body") or ""
        marker = "ABS_TASK_JSON:"
        if marker not in body:
            raise ValueError("ABS issue does not contain ABS_TASK_JSON.")
        payload = body.split(marker, 1)[1].strip()
        task = json.loads(payload)
        if not isinstance(task, dict):
            raise ValueError("ABS task must be a JSON object.")
        if not task.get("id"):
            task["id"] = f"github-issue-{issue['number']}"
        return task

    def _comment(self, issue_number, body):
        self._request("POST", f"/issues/{issue_number}/comments", {"body": body})

    def _close(self, issue_number):
        self._request("PATCH", f"/issues/{issue_number}", {"state": "closed", "state_reason": "completed"})

    def run_once(self):
        processed = 0
        for issue in self._pending_issues():
            if processed >= self.max_tasks:
                break
            try:
                task = self._task_from_issue(issue)
                if task.get("status", "pending") != "pending":
                    continue
                task_id = str(task["id"])
                capability = task.get("capability", "codex")
                approved = bool(task.get("approved", False))
                context = task.get("context") or {}

                self._comment(
                    issue["number"],
                    "ABS-BRIDGE: running task " + task_id
                    + " (capability=" + capability
                    + ", approved=" + str(approved) + ").",
                )

                work = self.orchestrator.create(str(task["objective"]), context=context)
                result = self.orchestrator.run(work.id, capability_id=capability, approved=approved)

                payload = {
                    "task_id": task_id,
                    "work_id": work.id,
                    "state": result.state.value,
                    "result": result.result,
                    "completed_at": datetime.now(timezone.utc).isoformat(),
                }
                self._comment(
                    issue["number"],
                    "ABS-BRIDGE: completed.\n\n" + json.dumps(payload, ensure_ascii=False, indent=2),
                )
                self._close(issue["number"])
                processed += 1
            except Exception as exc:
                self._comment(
                    issue["number"],
                    "ABS-BRIDGE: failed.\n\n" + f"{type(exc).__name__}: {exc}",
                )
                self._close(issue["number"])
                processed += 1
        return processed

    def run_forever(self):
        while True:
            self.run_once()
            time.sleep(self.interval)


def main():
    GitHubIssueBridge().run_forever()


if __name__ == "__main__":
    main()
