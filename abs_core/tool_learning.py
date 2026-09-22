from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .tool_knowledge import ToolKnowledgeRegistry
from .tool_knowledge_store import ToolKnowledgeStore


class ToolLearningEngine:
    """Turns execution evidence into explicit tool knowledge.

    It never treats an unverified result as success. Callers provide the
    observed outcome and evidence.
    """

    def __init__(self, knowledge: ToolKnowledgeRegistry, store: ToolKnowledgeStore | None = None) -> None:
        self.knowledge = knowledge
        self.store = store

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
        result = self.knowledge.learn(
            tool_id,
            evidence=enriched,
            lesson=lesson,
            usage_pattern=usage_pattern,
            status="validated" if success else "degraded",
        )
        if self.store:
            self.store.save(result)
        return result
