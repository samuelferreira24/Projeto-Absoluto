import json
from typing import Any

class CodexCapability:
    """Codex adapter with persisted thread continuity."""

    id = "codex"
    name = "OpenAI Codex"

    def __init__(self, model: str | None = None, sandbox: str = "workspace_write") -> None:
        self.model = model
        self.sandbox = sandbox

    def execute(self, objective: str, context: dict[str, Any]) -> dict[str, Any]:
        try:
            from openai_codex import Codex, Sandbox
        except ImportError as exc:
            raise RuntimeError("Codex adapter requires: pip install -e '.[codex]'") from exc

        sandbox_value = getattr(Sandbox, self.sandbox)
        thread_id = context.get("_codex_thread_id")
        with Codex() as codex:
            if thread_id:
                thread = codex.thread_resume(thread_id)
            else:
                kwargs = {"sandbox": sandbox_value}
                if self.model:
                    kwargs["model"] = self.model
                thread = codex.thread_start(**kwargs)

            prompt = objective
            clean_context = {k: v for k, v in context.items() if k != "_codex_thread_id"}
            if clean_context:
                prompt += "\n\nABS CONTEXT (JSON):\n" + json.dumps(clean_context, ensure_ascii=False)

            result = thread.run(prompt)
            return {
                "type": "codex",
                "thread_id": getattr(thread, "id", thread_id),
                "final_response": result.final_response,
            }
