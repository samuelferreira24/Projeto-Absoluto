from __future__ import annotations

"""Observable Project Knowledge for Projeto Absoluto.

Structured knowledge is the source; JSON/Markdown are generated projections.
Automatic observation may update factual state/evidence, never human authority.
"""

import hashlib
import json
import os
import subprocess
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.4"
DEFAULT_OUTPUT = Path(os.getenv("PA_KNOWLEDGE_DIR", "continuidade/07_conhecimento"))
EXCLUDED = {".git", ".venv", "__pycache__", ".pytest_cache", "node_modules"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@dataclass
class Evidence:
    id: str
    kind: str
    source: str
    observed_at: str
    status: str
    detail: str = ""


@dataclass
class PathRecord:
    id: str
    objective: str
    origin: str
    destination: str
    state: str
    preconditions: list[str] = field(default_factory=list)
    resources: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    fallback: list[str] = field(default_factory=list)
    approval: str = "required"
    last_validated: str | None = None



@dataclass
class KnowledgeSource:
    id: str
    path: str
    layer: str
    authority: str
    temporal: str
    status: str
    sha256: str | None = None


@dataclass
class Relation:
    id: str
    source: str
    relation: str
    target: str
    status: str = "asserted"
    at: str | None = None
    source_ref: str | None = None
    note: str = ""
    authority: str = "derived_observation"
    temporal: str = "current"
    valid_from: str | None = None
    valid_until: str | None = None


@dataclass
class ProjectKnowledge:
    schema_version: str = SCHEMA_VERSION
    project: str = "Projeto Absoluto"
    generated_at: str = field(default_factory=utc_now)
    source_revision: str | None = None
    components: list[dict[str, Any]] = field(default_factory=list)
    capabilities: list[dict[str, Any]] = field(default_factory=list)
    resources: list[dict[str, Any]] = field(default_factory=list)
    tools: list[dict[str, Any]] = field(default_factory=list)
    nodes: list[dict[str, Any]] = field(default_factory=list)
    paths: list[PathRecord] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)
    decisions: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)
    knowledge_sources: list[KnowledgeSource] = field(default_factory=list)
    relations: list[Relation] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["paths"] = [asdict(x) for x in self.paths]
        data["evidence"] = [asdict(x) for x in self.evidence]
        return data



def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


class RepositoryScanner:
    """Discover repository facts without treating every Python module as a capability."""


    KNOWLEDGE_SOURCES = {
        "source:vision": ("continuidade/01_contexto/01_MODELO_ABS_E_PRINCIPIOS.md", "vision_principles", "human_authority", "current"),
        "source:decisions": ("continuidade/03_decisoes/01_DECISOES_CORRECOES_E_REGRAS.md", "decisions", "human_authority", "current"),
        "source:research": ("docs/00_governanca/PESQUISA_PRESERVACAO_CONTEXTO_CONTINUIDADE_V1.md", "research", "research_reference", "current"),
        "source:trajectory-research": ("docs/00_governanca/PESQUISA_TRAJETORIA_PROVENIENCIA_BIDIRECIONAL_V1.md", "trajectory_research", "research_reference", "current"),
        "source:evidence": ("continuidade/07_conhecimento/03_CONTRATO_DE_PROVA.md", "evidence_contract", "project_governance", "current"),
        "source:state": ("continuidade/07_conhecimento/project_knowledge.json", "derived_state", "derived_observation", "current"),
        "source:session": ("continuidade/07_conhecimento/SESSAO_ATUAL.md", "session_state", "continuity", "current"),
        "source:handoff": ("continuidade/05_handoffs/05_HANDOFF_ATUAL_COMPLETO_2026-10-03.md", "handoff", "continuity", "current"),
        "source:navigation": ("00_IA_NAVEGACAO.md", "navigation", "project_governance", "current"),
        "source:history": ("99_arquivo/README.md", "history_archive", "historical_archive", "historical"),
        "source:trajectory-registry": ("continuidade/07_conhecimento/trajectory_registry.json", "trajectory_registry", "project_governance", "current"),
        "source:capability-registry": ("continuidade/07_conhecimento/capability_registry.json", "capability_registry", "project_governance", "current"),
    }

    def _load_trajectory_registry(self) -> list[dict[str, Any]]:
        path = self.root / "continuidade/07_conhecimento/trajectory_registry.json"
        if not path.is_file():
            return []
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        relations = payload.get("relations", [])
        return [dict(item) for item in relations if isinstance(item, dict)]

    def _scan_knowledge_sources(self) -> list[KnowledgeSource]:
        records: list[KnowledgeSource] = []
        for source_id, (rel, layer, authority, temporal) in self.KNOWLEDGE_SOURCES.items():
            path = self.root / rel
            if not path.is_file():
                records.append(KnowledgeSource(source_id, rel, layer, authority, temporal, "missing"))
            else:
                records.append(KnowledgeSource(source_id, rel, layer, authority, temporal, "present", sha256_file(path)))
        return records

    CAPABILITY_FILES = {
        "abs_core/orchestrator.py": ("orchestrator", "ABS orchestration"),
        "abs_core/codex_adapter.py": ("codex", "Codex code engineering"),
        "abs_core/internet_adapter.py": ("internet-http", "Internet HTTP"),
    }

    CAPABILITY_PATHS = {
        "orchestrator": (
            "PATH-ABS-ORCHESTRATOR",
            "route an ABS work request through the operational core",
            "Imperador/ABS input",
            "ABS Work result",
        ),
        "codex": (
            "PATH-ABS-CODEX",
            "execute code-engineering work through Codex adapter",
            "ABS Orchestrator",
            "Projeto Absoluto codebase",
        ),
        "internet-http": (
            "PATH-ABS-INTERNET-HTTP",
            "execute an HTTP request through the Internet adapter",
            "ABS capability/resource",
            "HTTP response",
        ),
    }

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve()

    def _git(self, *args: str) -> str | None:
        try:
            return (
                subprocess.check_output(
                    ["git", *args], cwd=self.root, text=True, stderr=subprocess.DEVNULL
                ).strip()
                or None
            )
        except (OSError, subprocess.CalledProcessError):
            return None

    def revision(self) -> str | None:
        return self._git("rev-parse", "HEAD")

    def revision_timestamp(self) -> str:
        return self._git("show", "-s", "--format=%cI", "HEAD") or "unknown"

    def branch(self) -> str | None:
        return self._git("branch", "--show-current")

    def remote(self) -> str | None:
        return self._git("config", "--get", "remote.origin.url")

    def commit_subject(self) -> str | None:
        return self._git("show", "-s", "--format=%s", "HEAD")

    def git_history(self) -> list[dict[str, Any]]:
        raw = self._git(
            "log",
            "--reverse",
            "--format=@@@%x1f%H%x1f%P%x1f%cI%x1f%s",
            "--name-only",
        ) or ""
        commits: list[dict[str, Any]] = []
        current: dict[str, Any] | None = None
        for line in raw.splitlines():
            if line.startswith("@@@\x1f"):
                _, sha, parents, at, subject = line.split("\x1f", 4)
                current = {
                    "id": "commit:" + sha,
                    "sha": sha,
                    "parents": parents.split() if parents else [],
                    "at": at,
                    "subject": subject,
                    "changed_files": [],
                }
                commits.append(current)
            elif line.strip() and current is not None:
                current["changed_files"].append(line.strip())
        return commits

    def scan_files(self) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for path in sorted(self.root.rglob("*")):
            if not path.is_file() or any(part in EXCLUDED for part in path.parts):
                continue
            rel = path.relative_to(self.root).as_posix()
            out.append(
                {
                    "id": "file:" + rel,
                    "path": rel,
                    "kind": self._kind(rel),
                    "size": path.stat().st_size,
                }
            )
        return out

    @staticmethod
    def _kind(rel: str) -> str:
        for prefix, kind in (
            ("abs_core/", "abs_core"),
            ("cerebro/", "cerebro"),
            ("continuidade/", "continuity"),
            ("mini-cerebro/", "historical_mini_cerebro"),
            ("tests/", "tests"),
            ("docs/", "docs"),
        ):
            if rel.startswith(prefix):
                return kind
        return "project"

    def scan(self) -> ProjectKnowledge:
        files = self.scan_files()
        revision = self.revision()
        observed_at = self.revision_timestamp()
        manifest = json.dumps(files, sort_keys=True, separators=(",", ":"))
        state_id = digest((revision or "unversioned") + manifest)[:12]
        k = ProjectKnowledge(generated_at=observed_at, source_revision=revision)
        k.knowledge_sources = self._scan_knowledge_sources()
        for item in self._load_trajectory_registry():
            k.relations.append(Relation(
                id=str(item.get("id")),
                source=str(item.get("source")),
                relation=str(item.get("relation")),
                target=str(item.get("target")),
                status=str(item.get("status", "asserted")),
                source_ref=item.get("source_ref"),
                note=str(item.get("note", "")),
                authority=str(item.get("authority", "project_governance")),
                temporal=str(item.get("temporal", "current")),
                valid_from=item.get("valid_from"),
                valid_until=item.get("valid_until"),
            ))

        kinds = sorted({f["kind"] for f in files})
        k.components = [
            {
                "id": "component:" + kind,
                "kind": kind,
                "file_count": sum(f["kind"] == kind for f in files),
            }
            for kind in kinds
        ]

        evidence_id = "evidence:repository:" + state_id
        k.evidence.append(
            Evidence(
                evidence_id,
                "repository_scan",
                str(self.root),
                observed_at,
                "observed",
                f"{len(files)} files indexed at revision {revision or 'unknown'}",
            )
        )
        k.events.append(
            {
                "id": "event:repository-scan:" + state_id,
                "type": "repository_scanned",
                "at": observed_at,
                "revision": revision,
                "file_count": len(files),
                "evidence_id": evidence_id,
            }
        )
        if revision:
            changes = self._git(
                "diff-tree", "--no-commit-id", "--name-status", "-r", revision
            ) or ""
            changed = [
                line.split("\t", 1)[-1]
                for line in changes.splitlines()
                if line.strip()
            ]
            k.events.append(
                {
                    "id": "event:commit-observed:" + revision[:12],
                    "type": "commit_observed",
                    "at": observed_at,
                    "revision": revision,
                    "branch": self.branch(),
                    "subject": self.commit_subject(),
                    "changed_files": changed,
                }
            )

        history = self.git_history()
        changed_paths = {path for commit in history for path in commit["changed_files"]}
        for path in sorted(changed_paths):
            k.nodes.append({"id": "file:" + path, "kind": "file", "path": path})

        for commit in history:
            k.nodes.append({
                "id": commit["id"], "kind": "commit", "at": commit["at"],
                "subject": commit["subject"], "sha": commit["sha"],
            })
            for parent in commit["parents"]:
                k.relations.append(Relation(
                    id=f"rel:commit-precedes:{parent[:12]}:{commit['sha'][:12]}",
                    source="commit:" + parent, relation="precedes", target=commit["id"],
                    at=commit["at"], source_ref="git",
                ))
            for path in commit["changed_files"]:
                k.relations.append(Relation(
                    id=f"rel:commit-changed:{commit['sha'][:12]}:{digest(path)[:12]}",
                    source=commit["id"], relation="changed", target="file:" + path,
                    at=commit["at"], source_ref="git",
                ))

        for source in k.knowledge_sources:
            k.nodes.append({
                "id": source.id, "kind": "knowledge_source", "path": source.path,
                "authority": source.authority, "temporal": source.temporal,
                "status": source.status,
            })

        for relation in k.relations:
            for node_id in (relation.source, relation.target):
                if not any(node.get("id") == node_id for node in k.nodes):
                    k.nodes.append({"id": node_id, "kind": "trajectory_endpoint"})

        for evidence in k.evidence:
            k.nodes.append({
                "id": evidence.id, "kind": "evidence", "at": evidence.observed_at,
                "status": evidence.status, "source": evidence.source,
            })

        for event in k.events:
            k.nodes.append({
                "id": event["id"], "kind": "event", "type": event["type"],
                "at": event.get("at"),
            })
            evidence_id = event.get("evidence_id")
            if evidence_id:
                k.relations.append(Relation(
                    id=f"rel:event-evidence:{event['id']}",
                    source=event["id"], relation="generated", target=evidence_id,
                    at=event.get("at"), source_ref="repository-observation",
                ))

        if revision:
            scan_event = next(
                (e for e in k.events if e["id"].startswith("event:repository-scan:")),
                None,
            )
            if scan_event:
                k.relations.append(Relation(
                    id=f"rel:scan-commit:{revision[:12]}",
                    source="commit:" + revision, relation="observed_by",
                    target=scan_event["id"], at=observed_at, source_ref="git",
                ))
        k.resources = [
            {
                "id": "resource:repository",
                "name": self.root.name,
                "type": "repository",
                "state": "observed",
                "branch": self.branch(),
                "remote": self.remote(),
                "revision": revision,
                "commit_subject": self.commit_subject(),
            }
        ]

        k.tools = [
            {
                "id": "tool:file:" + f["path"],
                "name": f["path"],
                "state": "present",
                "source": "repository",
            }
            for f in files
            if f["kind"] == "abs_core"
            and any(token in f["path"] for token in ("tool_", "codex", "bridge", "github"))
        ]

        for f in files:
            capability = self.CAPABILITY_FILES.get(f["path"])
            if f["kind"] == "abs_core" and capability:
                capability_id, name = capability
                k.capabilities.append(
                    {
                        "id": f"capability:{capability_id}",
                        "name": name,
                        "state": "observed",
                        "source": "repository",
                        "module": f["path"],
                    }
                )

        capability_registry_path = self.root / "continuidade/07_conhecimento/capability_registry.json"
        if capability_registry_path.is_file():
            try:
                capability_registry = json.loads(capability_registry_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                capability_registry = {}
            for item in capability_registry.get("capabilities", []):
                if not isinstance(item, dict) or not item.get("id"):
                    continue
                k.capabilities.append({
                    "id": item["id"],
                    "name": item.get("name", item["id"]),
                    "state": item.get("status", "planned"),
                    "source": "capability_registry",
                    "category": item.get("category"),
                    "evidence": item.get("evidence", []),
                })

        paths = {f["path"] for f in files}
        for capability_id, (path_id, objective, origin, destination) in self.CAPABILITY_PATHS.items():
            module = next(
                (
                    file["path"]
                    for file in files
                    if self.CAPABILITY_FILES.get(file["path"], (None,))[0] == capability_id
                ),
                None,
            )
            if module:
                k.paths.append(
                    PathRecord(
                        path_id,
                        objective,
                        origin,
                        destination,
                        "observed",
                        tools=[module],
                        evidence=[evidence_id],
                        approval="required",
                    )
                )
        return k


class KnowledgeStore:
    """Persist only the two generated projection files, atomically."""

    def __init__(self, output_dir: str | Path = DEFAULT_OUTPUT) -> None:
        self.output_dir = Path(output_dir)

    def write(self, k: ProjectKnowledge) -> dict[str, str]:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        state = self.output_dir / "project_knowledge.json"
        projection = self.output_dir / "MAPA_AUTO_ESTADO_PROJETO.md"
        self._atomic(state, json.dumps(k.to_dict(), ensure_ascii=False, indent=2) + "\n")
        self._atomic(projection, self._render_map(k))
        return {"state": str(state), "map": str(projection)}

    @staticmethod
    def _atomic(path: Path, content: str) -> None:
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(content, encoding="utf-8")
        tmp.replace(path)

    @staticmethod
    def _render_map(k: ProjectKnowledge) -> str:
        lines = [
            "# MAPA AUTOMÁTICO — ESTADO OBSERVÁVEL DO PROJETO",
            "",
            "Gerado automaticamente; não substitui autoridade humana.",
            "",
            f"Revisão observada: {k.source_revision or 'desconhecida'}",
            f"Momento da revisão: {k.generated_at}",
            "",
            "## Camadas de continuidade",
        ]
        lines += [
            f"- {x.id} — {x.layer} — {x.path} — {x.status} — autoridade: {x.authority} — temporalidade: {x.temporal}"
            for x in k.knowledge_sources
        ]
        lines += ["", "## Componentes"]
        lines += [
            f"- {x['id']} — {x['kind']} ({x['file_count']} arquivos)"
            for x in k.components
        ]
        lines += ["", "## Capacidades"]
        lines += [
            f"- {x['id']} — {x['name']} — estado: {x['state']}"
            for x in k.capabilities
        ]
        lines += ["", "## Recursos"]
        lines += [
            f"- {x.get('id')} — {x.get('name', x.get('type', 'recurso'))} — estado: {x.get('state', 'unknown')}"
            for x in k.resources
        ]
        lines += ["", "## Ferramentas"]
        lines += [
            f"- {x.get('id')} — {x.get('name')} — estado: {x.get('state', 'unknown')}"
            for x in k.tools
        ]
        lines += ["", "## Nós"]
        lines += [
            f"- {x.get('id')} — {x.get('name')} — estado: {x.get('state', 'unknown')}"
            for x in k.nodes
        ]
        lines += ["", "## Caminhos"]
        lines += [
            f"- {p.id} — {p.objective} — estado: {p.state} — evidências: {', '.join(str(x) for x in p.evidence if x) or 'nenhuma'}"
            for p in k.paths
        ]
        lines += ["", "## Eventos"]
        lines += [
            f"- {e['id']} — {e['type']} — revisão: {e.get('revision', 'n/a')}"
            for e in k.events
        ]
        lines += ["", "## Relações de trajetória"]
        lines += [
            f"- {r.source} — {r.relation} → {r.target} — {r.status}"
            for r in k.relations
        ]
        lines += ["", "## Trajetória"]
        lines += ["- validação: " + ("PASS" if not validate_trajectory(k) else "FAIL")]
        lines += ["", "## Evidências"]
        lines += [
            f"- {e.id} — {e.kind} — {e.status} — {e.detail}"
            for e in k.evidence
        ]
        lines += [
            "",
            "## Regra",
            "Mudança observável → evento → conhecimento estruturado → evidência → "
            "reavaliação de caminhos → projeções.",
            "",
            "Conteúdo autoritativo humano não é sobrescrito.",
            "",
        ]
        return "\n".join(lines)


def validate_trajectory(knowledge: ProjectKnowledge) -> list[dict[str, str]]:
    from .trajectory import TrajectoryGraph
    graph = TrajectoryGraph(knowledge.nodes, [asdict(r) for r in knowledge.relations])
    return [asdict(issue) for issue in graph.validate()]


def trace_trajectory(knowledge: ProjectKnowledge, start: str, *, direction: str = "backward", max_depth: int = 8, relation_types: list[str] | None = None) -> list[list[str]]:
    from .trajectory import TrajectoryGraph
    graph = TrajectoryGraph(knowledge.nodes, [asdict(r) for r in knowledge.relations])
    return graph.trace(start, direction=direction, max_depth=max_depth, relation_types=relation_types)


def evaluate_paths(knowledge: ProjectKnowledge) -> ProjectKnowledge:
    # Local import avoids a module cycle: PathEvaluator consumes these dataclasses.
    from .path_evaluator import PathEvaluator

    knowledge.paths = [
        PathEvaluator().evaluate(path, knowledge.evidence)
        for path in knowledge.paths
    ]
    return knowledge


def synchronize(
    root: str | Path,
    output_dir: str | Path = DEFAULT_OUTPUT,
    test_status: str | None = None,
    test_detail: str = "",
) -> dict[str, str]:
    root_path = Path(root).resolve()
    knowledge = RepositoryScanner(root_path).scan()

    if test_status:
        evidence_id = "evidence:test:" + digest(
            f"{knowledge.source_revision or 'unknown'}|pytest|{test_status}|{test_detail}"
        )[:12]
        knowledge.evidence.append(
            Evidence(
                evidence_id,
                "test",
                "pytest",
                knowledge.generated_at,
                test_status,
                test_detail,
            )
        )
        for path in knowledge.paths:
            if test_status == "tested":
                if (
                    path.id == "PATH-ABS-CODEX"
                    and (root_path / "tests/test_codex_cli_adapter.py").exists()
                ):
                    path.evidence.append(evidence_id)
                elif (
                    path.id == "PATH-ABS-ORCHESTRATOR"
                    and (root_path / "tests/test_orchestrator.py").exists()
                ):
                    path.evidence.append(evidence_id)
        knowledge.events.append(
            {
                "id": "event:test:" + evidence_id.split(":")[-1],
                "type": "tests_observed",
                "at": knowledge.generated_at,
                "status": test_status,
                "evidence_id": evidence_id,
            }
        )

    evaluate_paths(knowledge)
    return KnowledgeStore(output_dir).write(knowledge)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=os.getenv("PA_ROOT", "."))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--test-status", choices=["tested", "failure"])
    parser.add_argument("--test-detail", default="")
    args = parser.parse_args()
    print(
        json.dumps(
            synchronize(
                args.root,
                args.output,
                test_status=args.test_status,
                test_detail=args.test_detail,
            ),
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
