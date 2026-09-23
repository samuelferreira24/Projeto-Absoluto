from __future__ import annotations
"""Observable Project Knowledge for Projeto Absoluto."""
import hashlib, json, os, subprocess
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0"
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
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve()
    def _git(self, *args: str) -> str | None:
        try:
            return subprocess.check_output(["git", *args], cwd=self.root, text=True, stderr=subprocess.DEVNULL).strip() or None
        except (OSError, subprocess.CalledProcessError):
            return None
    def revision(self) -> str | None:
        return self._git("rev-parse", "HEAD")
    def scan_files(self) -> list[dict[str, Any]]:
        out = []
        for path in sorted(self.root.rglob("*")):
            if not path.is_file() or any(part in EXCLUDED for part in path.parts):
                continue
            rel = path.relative_to(self.root).as_posix()
            out.append({"id": "file:" + rel, "path": rel, "kind": self._kind(rel), "size": path.stat().st_size})
        return out
    @staticmethod
    def _kind(rel: str) -> str:
        for prefix, kind in (("abs_core/","abs_core"),("cerebro/","cerebro"),("continuidade/","continuity"),("mini-cerebro/","historical_mini_cerebro"),("tests/","tests"),("docs/","docs")):
            if rel.startswith(prefix):
                return kind
        return "project"
    def scan(self) -> ProjectKnowledge:
        now = utc_now()
        files = self.scan_files()
        revision = self.revision()
        k = ProjectKnowledge(generated_at=now, source_revision=revision)
        kinds = sorted({f["kind"] for f in files})
        k.components = [{"id":"component:"+x,"kind":x,"file_count":sum(f["kind"]==x for f in files)} for x in kinds]
        evidence_id = "evidence:repository:" + digest((revision or "") + now)[:12]
        k.evidence.append(Evidence(evidence_id,"repository_scan",str(self.root),now,"observed",f"{len(files)} files indexed at revision {revision or 'unknown'}"))
        k.events.append({"id":"event:repository-scan:"+digest(now+(revision or ""))[:12],"type":"repository_scanned","at":now,"revision":revision,"file_count":len(files)})
        k.resources = [{"id":"resource:repository","name":self.root.name,"type":"repository","state":"observed"}]
        k.tools = [{"id":"tool:file:"+f["path"],"name":f["path"],"state":"present","source":"repository"} for f in files if f["kind"]=="abs_core" and any(x in f["path"] for x in ("tool_","codex","bridge","github"))]
        k.capabilities = [{"id":"capability:module:"+f["path"],"name":f["path"],"state":"implemented","source":"repository"} for f in files if f["kind"]=="abs_core" and f["path"].endswith(".py") and Path(f["path"]).stem!="__init__"]
        names = {x["name"] for x in k.capabilities}
        if "abs_core/orchestrator.py" in names:
            k.paths.append(PathRecord("PATH-ABS-ORCHESTRATOR","route an ABS work request through the operational core","Imperador/ABS input","ABS Work result","observed",tools=["abs_core/orchestrator.py"],evidence=[evidence_id],approval="required",last_validated=now))
        if "abs_core/codex_adapter.py" in names:
            k.paths.append(PathRecord("PATH-ABS-CODEX","execute code-engineering work through Codex adapter","ABS Orchestrator","Projeto Absoluto codebase","observed",tools=["abs_core/codex_adapter.py"],fallback=["another compatible execution resource"],evidence=[evidence_id],approval="required",last_validated=now))
        return k

class KnowledgeStore:
    def __init__(self, output_dir: str | Path = DEFAULT_OUTPUT) -> None:
        self.output_dir = Path(output_dir)
    def write(self, k: ProjectKnowledge) -> dict[str,str]:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        state = self.output_dir / "project_knowledge.json"
        projection = self.output_dir / "MAPA_AUTO_ESTADO_PROJETO.md"
        self._atomic(state, json.dumps(k.to_dict(), ensure_ascii=False, indent=2) + "\n")
        self._atomic(projection, self._render_map(k))
        return {"state":str(state),"map":str(projection)}
    @staticmethod
    def _atomic(path: Path, content: str) -> None:
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(content, encoding="utf-8")
        tmp.replace(path)
    @staticmethod
    def _render_map(k: ProjectKnowledge) -> str:
        lines = ["# MAPA AUTOMÁTICO — ESTADO OBSERVÁVEL DO PROJETO","","Gerado automaticamente; não substitui autoridade humana.","",f"Gerado em: {k.generated_at}",f"Revisão observada: {k.source_revision or 'desconhecida'}","","## Componentes"]
        lines += [f"- {x['id']} — {x['kind']} ({x['file_count']} arquivos)" for x in k.components]
        lines += ["","## Caminhos"]
        lines += [f"- {p.id} — {p.objective} — estado: {p.state}" for p in k.paths]
        lines += ["","## Evidências"]
        lines += [f"- {e.id} — {e.kind} — {e.status} — {e.detail}" for e in k.evidence]
        lines += ["","## Regra","Mudanças observáveis devem ser descobertas pelo sincronizador. Conteúdo autoritativo humano não é sobrescrito.",""]
        return "\n".join(lines)

def synchronize(root: str | Path, output_dir: str | Path = DEFAULT_OUTPUT) -> dict[str,str]:
    return KnowledgeStore(output_dir).write(RepositoryScanner(root).scan())

def main() -> int:
    root = Path(os.getenv("PA_ROOT",".")).resolve()
    print(json.dumps(synchronize(root), ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
