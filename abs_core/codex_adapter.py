from typing import Any

class CodexCapability:
    """Real Codex capability adapter using the official Python Codex SDK.

    The dependency is optional; installing this project's 'codex' extra enables it.
    The ABS remains independent of Codex because this class is only an adapter.
    """
    id = "codex"
    name = "OpenAI Codex"

    def __init__(self, model: str | None = None, sandbox: str = "workspace_write") -> None:
        self.model = model
        self.sandbox = sandbox
        self._thread = None
        self.thread_id: str | None = None

    def execute(self, objective: str, context: dict[str, Any]) -> dict[str, Any]:
        try:
            from openai_codex import Codex, Sandbox
        except ImportError as exc:
            raise RuntimeError("Codex adapter requires: pip install -e '.[codex]'") from exc

        sandbox_value = getattr(Sandbox, self.sandbox)
        with Codex() as codex:
            if self._thread is None:
                kwargs = {"sandbox": sandbox_value}
                if self.model:
                    kwargs["model"] = self.model
                self._thread = codex.thread_start(**kwargs)
                self.thread_id = getattr(self._thread, "id", None)
            prompt = objective
            if context:
                prompt += "\\n\\nABS CONTEXT (JSON):\\n" + __import__("json").dumps(context, ensure_ascii=False)
            result = self._thread.run(prompt)
            return {
                "type": "codex",
                "thread_id": getattr(self._thread, "id", self.thread_id),
                "final_response": result.final_response,
            }
