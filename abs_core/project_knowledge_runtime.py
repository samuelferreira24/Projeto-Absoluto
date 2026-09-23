from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any

from .project_knowledge import Evidence, ProjectKnowledge, utc_now, digest


class RuntimeKnowledgeCollector:
    """Translate live ABS runtime registries into observable project knowledge."""

    def collect(self, runtime: Any, knowledge: ProjectKnowledge | None = None) -> ProjectKnowledge:
        k = knowledge or ProjectKnowledge()
        now = utc_now()

        if hasattr(runtime, "registry") and hasattr(runtime.registry, "list"):
            k.capabilities.extend(
                {"id": f"runtime:capability:{item.id}", "name": item.name,
                 "state": "observed", "source": "abs_runtime",
                 "kind": getattr(item, "kind", "unknown")}
                for item in runtime.registry.list()
            )

        if hasattr(runtime, "connections") and hasattr(runtime.connections, "list"):
            for item in runtime.connections.list():
                data = item.public() if hasattr(item, "public") else asdict(item)
                k.resources.append({
                    "id": f"runtime:connection:{data['id']}",
                    "name": data.get("name", data["id"]),
                    "type": "connection",
                    "state": data.get("status", "unknown"),
                    "capabilities": data.get("capabilities", []),
                })

        if hasattr(runtime, "resources") and hasattr(runtime.resources, "list"):
            for item in runtime.resources.list():
                data = item.public() if hasattr(item, "public") else asdict(item)
                k.nodes.append({
                    "id": f"runtime:device:{data['id']}",
                    "name": data.get("name", data["id"]),
                    "state": data.get("status", "unknown"),
                    "capabilities": data.get("capabilities", []),
                })

        if hasattr(runtime, "tool_knowledge") and hasattr(runtime.tool_knowledge, "list"):
            for item in runtime.tool_knowledge.list():
                data = item.public() if hasattr(item, "public") else asdict(item)
                k.tools.append({
                    "id": f"runtime:tool:{data['id']}",
                    "name": data.get("name", data["id"]),
                    "state": data.get("status", "unknown"),
                    "capabilities": data.get("capabilities", []),
                    "reliability": item.reliability() if hasattr(item, "reliability") else None,
                })

        evidence_id = "evidence:runtime:" + digest(now)[:12]
        k.evidence.append(Evidence(
            evidence_id, "runtime_snapshot", "ABS runtime", now, "observed",
            "Live runtime registries were inspected; inspection is not execution proof.",
        ))
        k.events.append({
            "id": "event:runtime-snapshot:" + digest(now)[:12],
            "type": "runtime_snapshot",
            "at": now,
            "evidence_id": evidence_id,
        })
        return k
