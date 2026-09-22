from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .tool_knowledge import ToolKnowledgeRegistry


class ToolLearningEngine:
    """Turns execution evidence into explicit tool knowledge.

    It never treats an unverified result as success. Callers provide the
    observed outcome and evidence.
    """

    def __init__(self, knowledge: ToolKnowledgeRegistry) -> None:
        self.knowledge = knowledge

    def record(
        self,
        tool_id: str,
        *,
        success: bool,
        evidence: dict[str, Any],
        lesson: str | None = None,
        usage_pattern: str | None = None,
    ):
        enriched = dict(evidence)
        enriched.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
        enriched["success"] = success
        return self.knowledge.learn(
            tool_id,
            evidence=enriched,
            lesson=lesson,
            usage_pattern=usage_pattern,
            status="validated" if success else "degraded",
        )
