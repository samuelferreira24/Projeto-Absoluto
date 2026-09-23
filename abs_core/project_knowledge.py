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

SCHEMA_VERSION = "1.1"
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

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["paths"] = [asdict(x) for x in self.paths]
        data["evidence"] = [asdict(x) for x in self.evidence]
        return data


class RepositoryScanner:
    """Discover repository facts without treating every Python module as a capability."""

    CAPABILITY_FILES = {
        "abs_core/orchestrator.py": ("orchestrator", "ABS orchestration"),
        "abs_core/codex_adapter.py": ("codex", "Codex code engineering"),
        "abs_core/internet_adapter.py": ("internet-http", "Internet HTTP"),
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
                line.split("\\t", 1)[-1]
                for line in changes.splitlines()
                if line.strip()
            ]
            k.events.append(
                {
                    "id": "event:commit-observed:" + revision[:12],
                    "type": "commit_observed",
                    "at": observed_at,
                    "revision": revision,
                    "changed_files": changed,
                }
            )
        k.resources = [
            {
                "id": "resource:repository",
                "name": self.root.name,
                "type": "repository",
                "state": "observed",
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

        paths = {f["path"] for f in files}
        if "abs_core/orchestrator.py" in paths:
            k.paths.append(
                PathRecord(
                    "PATH-ABS-ORCHESTRATOR",
                    "route an ABS work request through the operational core",
                    "Imperador/ABS input",
                    "ABS Work result",
                    "observed",
                    tools=["abs_core/orchestrator.py"],
                    evidence=[evidence_id],
                    approval="required",
                )
            )
        if "abs_core/codex_adapter.py" in paths:
            k.paths.append(
                PathRecord(
                    "PATH-ABS-CODEX",
                    "execute code-engineering work through Codex adapter",
                    "ABS Orchestrator",
                    "Projeto Absoluto codebase",
                    "observed",
                    tools=["abs_core/codex_adapter.py"],
                    evidence=[evidence_id],
                    fallback=["another compatible execution resource"],
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
            "## Componentes",
        ]
        lines += [
            f"- {x['id']} — {x['kind']} ({x['file_count']} arquivos)"
            for x in k.components
        ]
        lines += ["", "## Capacidades"]
        lines += [
            f"- {x['id']} — {x['name']} — estado: {x['state']}"
            for x in k.capabilities
        ]
        lines += ["", "## Caminhos"]
        lines += [
            f"- {p.id} — {p.objective} — estado: {p.state}"
            for p in k.paths
        ]
        lines += ["", "## Eventos"]
        lines += [
            f"- {e['id']} — {e['type']} — revisão: {e.get('revision', 'n/a')}"
            for e in k.events
        ]
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
