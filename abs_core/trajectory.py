from __future__ import annotations

"""Bidirectional, repository-native trajectory/provenance traversal.

The graph is a derived navigation layer over durable project sources.
It never promotes an inferred relationship into project authority.
"""

from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

STRICT_ORDER_RELATIONS = frozenset({
    "precedes", "derived_from", "originated_from", "supersedes", "led_to",
})

@dataclass(frozen=True)
class TrajectoryIssue:
    kind: str
    detail: str

class TrajectoryGraph:
    def __init__(self, nodes: Iterable[Mapping[str, object]], relations: Iterable[Mapping[str, object]]) -> None:
        self.nodes = {str(node["id"]): dict(node) for node in nodes if node.get("id")}
        self.relations = [dict(relation) for relation in relations if relation.get("source") and relation.get("target")]

    def validate(self) -> list[TrajectoryIssue]:
        issues: list[TrajectoryIssue] = []
        seen: set[str] = set()
        for relation in self.relations:
            relation_id = str(relation.get("id", ""))
            if relation_id in seen:
                issues.append(TrajectoryIssue("duplicate_relation", relation_id))
            seen.add(relation_id)
            source = str(relation["source"])
            target = str(relation["target"])
            if source not in self.nodes:
                issues.append(TrajectoryIssue("missing_source", f"{relation_id}: {source}"))
            if target not in self.nodes:
                issues.append(TrajectoryIssue("missing_target", f"{relation_id}: {target}"))
            valid_from = relation.get("valid_from")
            valid_until = relation.get("valid_until")
            if valid_from and valid_until and str(valid_from) > str(valid_until):
                issues.append(TrajectoryIssue("invalid_interval", relation_id))

        adjacency: dict[str, list[str]] = defaultdict(list)
        for relation in self.relations:
            if relation.get("relation") in STRICT_ORDER_RELATIONS:
                adjacency[str(relation["source"])].append(str(relation["target"]))

        visiting: set[str] = set()
        visited: set[str] = set()
        def visit(node: str) -> None:
            if node in visiting:
                issues.append(TrajectoryIssue("strict_cycle", node))
                return
            if node in visited:
                return
            visiting.add(node)
            for target in adjacency.get(node, []):
                visit(target)
            visiting.remove(node)
            visited.add(node)
        for node in adjacency:
            visit(node)
        return issues

    def trace(self, start: str, *, direction: str = "forward", max_depth: int = 8,
              relation_types: Sequence[str] | None = None) -> list[list[str]]:
        if start not in self.nodes:
            return []
        if direction not in {"forward", "backward"}:
            raise ValueError("direction must be 'forward' or 'backward'")
        allowed = set(relation_types) if relation_types else None
        outgoing: dict[str, list[str]] = defaultdict(list)
        incoming: dict[str, list[str]] = defaultdict(list)
        for relation in self.relations:
            if allowed is not None and relation.get("relation") not in allowed:
                continue
            source, target = str(relation["source"]), str(relation["target"])
            outgoing[source].append(target)
            incoming[target].append(source)
        adjacency = outgoing if direction == "forward" else incoming
        paths: list[list[str]] = []
        queue = deque([(start, [start])])
        while queue:
            node, path = queue.popleft()
            if len(path) - 1 >= max_depth:
                paths.append(path)
                continue
            next_nodes = adjacency.get(node, [])
            if not next_nodes:
                paths.append(path)
                continue
            for target in next_nodes:
                if target in path:
                    paths.append(path + [target])
                else:
                    queue.append((target, path + [target]))
        return paths

    def ancestors(self, start: str, *, max_depth: int = 8) -> list[list[str]]:
        return self.trace(start, direction="backward", max_depth=max_depth)

    def descendants(self, start: str, *, max_depth: int = 8) -> list[list[str]]:
        return self.trace(start, direction="forward", max_depth=max_depth)
