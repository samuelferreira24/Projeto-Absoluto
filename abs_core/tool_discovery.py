from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlparse


@dataclass(frozen=True)
class ToolDiscoveryCandidate:
    name: str
    category: str
    source: str
    description: str = ""
    capabilities: tuple[str, ...] = ()
    connection_hints: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


class ToolDiscovery:
    """Normalizes new-tool candidates before they become system knowledge.

    Discovery never means trust or installation. Candidates must be researched,
    validated and authorized before becoming usable resources.
    """

    def from_candidate(self, candidate: ToolDiscoveryCandidate) -> dict[str, Any]:
        return {
            "name": candidate.name,
            "category": candidate.category,
            "source": candidate.source,
            "description": candidate.description,
            "capabilities": list(candidate.capabilities),
            "connection_hints": list(candidate.connection_hints),
            "metadata": dict(candidate.metadata),
            "state": "discovered",
        }

    def from_url(self, url: str, *, category: str = "unknown") -> ToolDiscoveryCandidate:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("invalid_tool_source_url")
        return ToolDiscoveryCandidate(
            name=parsed.netloc,
            category=category,
            source=url,
            connection_hints=("https",),
        )

    def validate_candidate(
        self,
        candidate: ToolDiscoveryCandidate,
        *,
        required_fields: tuple[str, ...] = ("name", "source"),
    ) -> list[str]:
        payload = self.from_candidate(candidate)
        return [field for field in required_fields if not payload.get(field)]
