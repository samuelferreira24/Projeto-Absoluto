from __future__ import annotations

import json
import os
import shutil
import subprocess
from typing import Any


class CodexCapability:
    """ABS capability adapter for the locally authenticated Codex CLI."""

    id = "codex"
    name = "OpenAI Codex CLI"

    def __init__(
        self,
        command: str | None = None,
        sandbox: str | None = None,
        approval: str | None = None,
        timeout: int | None = None,
        bypass_sandbox: bool | None = None,
    ) -> None:
        self.command = command or os.getenv("ABS_CODEX_COMMAND", "codex")
        self.sandbox = sandbox or os.getenv("ABS_CODEX_SANDBOX", "read-only")
        self.approval = approval or os.getenv("ABS_CODEX_APPROVAL", "never")
        self.timeout = timeout or int(os.getenv("ABS_CODEX_TIMEOUT", "900"))
        if bypass_sandbox is None:
            bypass_sandbox = os.getenv("ABS_CODEX_DANGEROUSLY_BYPASS", "").lower() in {
                "1", "true", "yes", "on"
            }
        self.bypass_sandbox = bypass_sandbox

    def execute(self, objective: str, context: dict[str, Any]) -> dict[str, Any]:
        executable = shutil.which(self.command) if os.path.basename(self.command) == self.command else self.command
        if not executable:
            raise RuntimeError(
                f"Codex CLI not found: {self.command}. "
                "Install/authenticate Codex CLI or set ABS_CODEX_COMMAND."
            )

        thread_id = context.get("_codex_thread_id")
        clean_context = {
            k: v for k, v in context.items()
            if k not in {"_codex_thread_id", "_codex_cwd"}
        }

        prompt = objective
        if clean_context:
            prompt += "\n\nABS CONTEXT (JSON):\n" + json.dumps(
                clean_context, ensure_ascii=False, sort_keys=True
            )

        if thread_id:
            args = [executable, "exec", "resume", str(thread_id), "--json"]
        else:
            args = [executable, "exec", "--json"]

        if self.bypass_sandbox:
            args.append("--dangerously-bypass-approvals-and-sandbox")
        else:
            args.extend(["-s", self.sandbox, "--ask-for-approval", self.approval])

        cwd = context.get("_codex_cwd") or os.getcwd()
        completed = subprocess.run(
            args + [prompt],
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=self.timeout,
            check=False,
        )

        if completed.returncode != 0:
            detail = completed.stderr.strip() or completed.stdout.strip()
            raise RuntimeError(
                f"Codex CLI exited with code {completed.returncode}: {detail}"
            )

        new_thread_id: str | None = None
        final_response: str | None = None
        events: list[dict[str, Any]] = []

        for line in completed.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            events.append(event)

            if event.get("type") == "thread.started":
                new_thread_id = event.get("thread_id")

            item = event.get("item") or {}
            if event.get("type") == "item.completed" and item.get("type") == "agent_message":
                final_response = item.get("text")

        if final_response is None:
            raise RuntimeError("Codex CLI completed without a final agent message.")

        return {
            "type": "codex_cli",
            "thread_id": new_thread_id or thread_id,
            "final_response": final_response,
            "event_count": len(events),
        }
