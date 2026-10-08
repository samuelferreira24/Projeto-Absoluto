from __future__ import annotations

import json
import os
import shutil
import subprocess
from typing import Any


class OpenClawIntelligenceCapability:
    """Use the already-installed OpenClaw runtime as an ABS reasoning resource."""

    id = "openclaw-intelligence"
    name = "OpenClaw Operational Intelligence"

    def __init__(self, command: str | None = None, timeout: int = 300):
        self.command = command or os.getenv("ABS_OPENCLAW_COMMAND", "/usr/bin/openclaw")
        self.timeout = timeout

    def execute(self, objective: str, context: dict[str, Any]) -> dict[str, Any]:
        executable = self.command
        if os.path.basename(executable) == executable:
            executable = shutil.which(executable) or ""
        if not executable:
            raise RuntimeError("OpenClaw intelligence executable not found")
        clean = {k: v for k, v in context.items() if not str(k).startswith("_")}
        prompt = objective
        if clean:
            prompt += "\n\nABS CONTEXT (JSON):\n" + json.dumps(clean, ensure_ascii=False, default=str)
        proc = subprocess.run(
            [executable, "agent", "--message", prompt, "--json"],
            text=True, capture_output=True, timeout=self.timeout, check=False,
            env={**os.environ, "HOME": os.getenv("HOME", "/home/absadmin")},
        )
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.strip() or f"openclaw_exit_{proc.returncode}")
        final = None
        events = []
        for line in proc.stdout.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            events.append(event)
            item = event.get("item") or {}
            if event.get("type") == "item.completed" and item.get("type") == "agent_message":
                final = item.get("text")
            if event.get("type") == "agent_message":
                final = event.get("text") or final
        if final is None:
            # Some OpenClaw versions return a JSON object containing the text
            # directly rather than item.completed events.
            try:
                parsed = json.loads(proc.stdout)
                final = parsed.get("text") or parsed.get("final_response")
            except Exception:
                final = proc.stdout.strip()
        if not final:
            raise RuntimeError("OpenClaw intelligence returned no final response")
        return {
            "type": "openclaw_intelligence",
            "final_response": final,
            "event_count": len(events),
        }
