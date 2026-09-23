from __future__ import annotations

from dataclasses import replace
from typing import Iterable

from .project_knowledge import Evidence, PathRecord


class PathEvaluator:
    """Derive path state from explicit evidence only."""

    def evaluate(self, path: PathRecord, evidence: Iterable[Evidence]) -> PathRecord:
        relevant = {
            item.id: item
            for item in evidence
            if item.id in set(path.evidence)
        }
        if not relevant:
            return replace(path, state="observed", last_validated=None)

        statuses = {item.status for item in relevant.values()}
        if "unavailable" in statuses:
            state = "unavailable"
        elif "degraded" in statuses or "failure" in statuses:
            state = "degraded"
        elif "operational" in statuses:
            state = "operational"
        elif "tested" in statuses:
            state = "tested"
        else:
            state = "observed"

        return replace(
            path,
            state=state,
            last_validated=max(x.observed_at for x in relevant.values()),
        )
