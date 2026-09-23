from __future__ import annotations

import json
import os
import shutil
import subprocess
from typing import Any


class CodexCapability:
    """ABS capability adapter for the locally authenticated Codex CLI.

    The ABS approval gate remains authoritative. Once a Work is approved,
    Codex receives workspace-write by default so it can actually modify the
    project while remaining sandboxed to its workspace.
    """

    id = "codex"
    name = "OpenAI Codex CLI"

    def __init__(self, command=None, sandbox=None, approval=None, timeout=None, bypass_sandbox=None):
        self.command = command or os.getenv("ABS_CODEX_COMMAND", "codex")
        self.sandbox = sandbox or os.getenv("ABS_CODEX_SANDBOX", "workspace-write")
        self.approval = approval or os.getenv("ABS_CODEX_APPROVAL", "never")
        self.timeout = timeout or int(os.getenv("ABS_CODEX_TIMEOUT", "900"))
        if bypass_sandbox is None:
            bypass_sandbox = os.getenv("ABS_CODEX_DANGEROUSLY_BYPASS", "").lower() in {"1", "true", "yes", "on"}
        self.bypass_sandbox = bypass_sandbox

    def execute(self, objective: str, context: dict[str, Any]) -> dict[str, Any]:
        executable = shutil.which(self.command) if os.path.basename(self.command) == self.command else self.command
        if not executable:
            raise RuntimeError(f"Codex CLI not found: {self.command}")

        thread_id = context.get("_codex_thread_id")
        clean_context = {k: v for k, v in context.items() if k not in {"_codex_thread_id", "_codex_cwd"}}
        prompt = objective
        if clean_context:
            prompt += "\n\nABS CONTEXT (JSON):\n" + json.dumps(clean_context, ensure_ascii=False, sort_keys=True)

        args = [executable, "exec"]
        if thread_id:
            args += ["resume", str(thread_id)]
        args += ["--json", "--sandbox", self.sandbox, "--ask-for-approval", self.approval]

        if self.bypass_sandbox:
            args = [executable, "exec"] + ([ "resume", str(thread_id)] if thread_id else []) + [
                "--json", "--dangerously-bypass-approvals-and-sandbox"
            ]

        cwd = context.get("_codex_cwd") or os.getenv("ABS_CODEX_CWD") or os.getcwd()
        completed = subprocess.run(args + [prompt], cwd=cwd, text=True, capture_output=True, timeout=self.timeout, check=False)

        if completed.returncode != 0:
            detail = completed.stderr.strip() or completed.stdout.strip()
            raise RuntimeError(f"Codex CLI exited with code {completed.returncode}: {detail}")

        thread_id = None
        final_response = None
        events = []
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
                thread_id = event.get("thread_id")
            item = event.get("item") or {}
            if event.get("type") == "item.completed" and item.get("type") == "agent_message":
                final_response = item.get("text")

        if final_response is None:
            raise RuntimeError("Codex CLI completed without a final agent message.")

        return {"type": "codex_cli", "thread_id": thread_id, "final_response": final_response, "event_count": len(events)}
