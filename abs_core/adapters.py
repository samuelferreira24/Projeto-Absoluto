from typing import Any

class EchoCapability:
    id = "echo"
    name = "Echo test capability"
    def execute(self, objective: str, context: dict[str, Any]) -> dict[str, Any]:
        return {"type": "echo", "objective": objective, "context": context}

class CodexCapabilityPlaceholder:
    """Boundary for a real Codex adapter; deliberately does not fake remote execution."""
    id = "codex"
    name = "Codex"
    def execute(self, objective: str, context: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError("Connect this adapter to a verified Codex runtime before enabling execution.")
