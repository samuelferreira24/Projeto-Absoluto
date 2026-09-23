from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

from .project_knowledge import Evidence, ProjectKnowledge, digest


def _public(item: Any) -> dict[str, Any]:
    if hasattr(item, "public"):
        return item.public()
    try:
        return asdict(item)
    except TypeError:
        return {
            key: getattr(item, key)
            for key in ("id", "name", "status", "capabilities")
            if hasattr(item, key)
        }


def _merge_unique(items: list[dict[str, Any]], values: list[dict[str, Any]]) -> None:
    existing = {item.get("id") for item in items}
    for value in values:
        if value.get("id") not in existing:
            items.append(value)
            existing.add(value.get("id"))


class RuntimeKnowledgeCollector:
    """Translate runtime registries into deterministic observable knowledge."""

    def collect(
        self, runtime: Any, knowledge: ProjectKnowledge | None = None
    ) -> ProjectKnowledge:
        k = knowledge or ProjectKnowledge()

        capabilities = []
        if hasattr(runtime, "registry") and hasattr(runtime.registry, "list"):
            for item in runtime.registry.list():
                capabilities.append(
                    {
                        "id": f"runtime:capability:{item.id}",
                        "name": item.name,
                        "state": "observed",
                        "source": "abs_runtime",
                        "kind": getattr(item, "kind", "unknown"),
                    }
                )
        _merge_unique(k.capabilities, capabilities)

        resources = []
        if hasattr(runtime, "connections") and hasattr(runtime.connections, "list"):
            for item in runtime.connections.list():
                data = _public(item)
                resources.append(
                    {
                        "id": f"runtime:connection:{data['id']}",
                        "name": data.get("name", data["id"]),
                        "type": "connection",
                        "state": data.get("status", "unknown"),
                        "capabilities": data.get("capabilities", []),
                    }
                )
        _merge_unique(k.resources, resources)

        nodes = []
        if hasattr(runtime, "resources") and hasattr(runtime.resources, "list"):
            for item in runtime.resources.list():
                data = _public(item)
                nodes.append(
                    {
                        "id": f"runtime:device:{data['id']}",
                        "name": data.get("name", data["id"]),
                        "state": data.get("status", "unknown"),
                        "capabilities": data.get("capabilities", []),
                    }
                )
        _merge_unique(k.nodes, nodes)

        tools = []
        if hasattr(runtime, "tool_knowledge") and hasattr(runtime.tool_knowledge, "list"):
            for item in runtime.tool_knowledge.list():
                data = _public(item)
                tools.append(
                    {
                        "id": f"runtime:tool:{data['id']}",
                        "name": data.get("name", data["id"]),
                        "state": data.get("status", "unknown"),
                        "capabilities": data.get("capabilities", []),
                        "reliability": (
                            item.reliability() if hasattr(item, "reliability") else None
                        ),
                    }
                )
        _merge_unique(k.tools, tools)

        snapshot = json.dumps(
            {
                "capabilities": capabilities,
                "resources": resources,
                "nodes": nodes,
                "tools": tools,
            },
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        )
        snapshot_id = digest(snapshot)[:12]
        evidence_id = f"evidence:runtime:{snapshot_id}"
        if not any(item.id == evidence_id for item in k.evidence):
            k.evidence.append(
                Evidence(
                    evidence_id,
                    "runtime_snapshot",
                    "ABS runtime",
                    k.generated_at,
                    "observed",
                    "Live registries inspected; inspection is not execution proof.",
                )
            )
        event_id = f"event:runtime-snapshot:{snapshot_id}"
        if not any(item.get("id") == event_id for item in k.events):
            k.events.append(
                {
                    "id": event_id,
                    "type": "runtime_snapshot",
                    "at": k.generated_at,
                    "evidence_id": evidence_id,
                }
            )
        return k


    def record_execution(
        self,
        knowledge: ProjectKnowledge,
        *,
        path_id: str,
        operation: str,
        status: str,
        detail: str = "",
        source: str = "ABS runtime",
    ) -> ProjectKnowledge:
        """Record explicit runtime execution evidence for a path."""
        execution_key = digest(
            f"{knowledge.source_revision or 'unknown'}|{path_id}|{operation}|{status}|{detail}"
        )[:12]
        evidence_id = f"evidence:execution:{execution_key}"
        if not any(item.id == evidence_id for item in knowledge.evidence):
            knowledge.evidence.append(
                Evidence(
                    evidence_id,
                    "execution",
                    source,
                    knowledge.generated_at,
                    status,
                    detail,
                )
            )
        for path in knowledge.paths:
            if path.id == path_id and evidence_id not in path.evidence:
                path.evidence.append(evidence_id)
        event_id = f"event:execution:{execution_key}"
        if not any(item.get("id") == event_id for item in knowledge.events):
            knowledge.events.append(
                {
                    "id": event_id,
                    "type": "execution_observed",
                    "at": knowledge.generated_at,
                    "path_id": path_id,
                    "operation": operation,
                    "status": status,
                    "evidence_id": evidence_id,
                }
            )
        return knowledge
