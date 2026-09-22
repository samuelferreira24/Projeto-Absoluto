from __future__ import annotations

from dataclasses import asdict, dataclass, field
from threading import RLock
from typing import Any


@dataclass
class ToolKnowledge:
    """Operational knowledge about how ABS can use a resource.

    This is not model training. It is persistent system knowledge: capabilities,
    connection paths, input/output contracts, constraints, evidence and lessons.
    """

    id: str
    name: str
    category: str
    capabilities: list[str] = field(default_factory=list)
    connection_ids: list[str] = field(default_factory=list)
    input_contract: dict[str, Any] = field(default_factory=dict)
    output_contract: dict[str, Any] = field(default_factory=dict)
    constraints: list[str] = field(default_factory=list)
    usage_patterns: list[str] = field(default_factory=list)
    status: str = "discovered"
    evidence: list[dict[str, Any]] = field(default_factory=list)
    lessons: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def public(self) -> dict[str, Any]:
        return asdict(self)

    def reliability(self) -> float:
        """Return the observed success ratio from recorded evidence."""
        outcomes = [
            item.get("success")
            for item in self.evidence
            if isinstance(item, dict) and isinstance(item.get("success"), bool)
        ]
        if not outcomes:
            return 0.5
        return sum(outcomes) / len(outcomes)


class ToolKnowledgeRegistry:
    """Extensible memory of tool usage knowledge and evidence."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._items: dict[str, ToolKnowledge] = {}

    def register(self, tool: ToolKnowledge) -> ToolKnowledge:
        with self._lock:
            if tool.id in self._items:
                raise ValueError(f"Tool knowledge already registered: {tool.id}")
            self._items[tool.id] = tool
            return ToolKnowledge(**asdict(tool))

    def upsert(self, tool: ToolKnowledge) -> ToolKnowledge:
        with self._lock:
            self._items[tool.id] = tool
            return ToolKnowledge(**asdict(tool))

    def get(self, tool_id: str) -> ToolKnowledge:
        with self._lock:
            return ToolKnowledge(**asdict(self._items[tool_id]))

    def list(self) -> list[ToolKnowledge]:
        with self._lock:
            return [ToolKnowledge(**asdict(item)) for item in self._items.values()]

    def learn(
        self,
        tool_id: str,
        *,
        capabilities: list[str] | None = None,
        connection_ids: list[str] | None = None,
        usage_pattern: str | None = None,
        lesson: str | None = None,
        evidence: dict[str, Any] | None = None,
        status: str | None = None,
    ) -> ToolKnowledge:
        with self._lock:
            item = self._items[tool_id]
            if capabilities:
                item.capabilities = sorted(set(item.capabilities + capabilities))
            if connection_ids:
                item.connection_ids = sorted(set(item.connection_ids + connection_ids))
            if usage_pattern and usage_pattern not in item.usage_patterns:
                item.usage_patterns.append(usage_pattern)
            if lesson and lesson not in item.lessons:
                item.lessons.append(lesson)
            if evidence:
                item.evidence.append(dict(evidence))
            if status:
                item.status = status
            return ToolKnowledge(**asdict(item))

    def find_by_capability(self, capability: str) -> list[ToolKnowledge]:
        return [item for item in self.list() if capability in item.capabilities]

    def find_by_capabilities(self, capabilities: list[str] | tuple[str, ...]) -> list[ToolKnowledge]:
        required = set(capabilities)
        return [item for item in self.list() if required.issubset(item.capabilities)]
