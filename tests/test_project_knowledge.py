from pathlib import Path
from abs_core.project_knowledge import KnowledgeStore, RepositoryScanner, synchronize

def test_scan_produces_evidence_and_paths(tmp_path: Path):
    (tmp_path / "abs_core").mkdir()
    (tmp_path / "abs_core" / "orchestrator.py").write_text("x", encoding="utf-8")
    (tmp_path / "abs_core" / "codex_adapter.py").write_text("x", encoding="utf-8")
    k = RepositoryScanner(tmp_path).scan()
    assert k.project == "Projeto Absoluto"
    assert k.evidence
    assert {p.id for p in k.paths} == {"PATH-ABS-ORCHESTRATOR", "PATH-ABS-CODEX"}

def test_projection_is_atomic(tmp_path: Path):
    (tmp_path / "abs_core").mkdir()
    (tmp_path / "abs_core" / "orchestrator.py").write_text("x", encoding="utf-8")
    result = synchronize(tmp_path, tmp_path / "knowledge")
    assert Path(result["state"]).exists()
    assert Path(result["map"]).exists()
    assert not list((tmp_path / "knowledge").glob("*.tmp"))

def test_authoritative_files_are_preserved(tmp_path: Path):
    out = tmp_path / "knowledge"
    out.mkdir()
    decision = out / "DECISAO_IMPERADOR.md"
    decision.write_text("# Decisão humana\n", encoding="utf-8")
    KnowledgeStore(out).write(RepositoryScanner(tmp_path).scan())
    assert decision.read_text(encoding="utf-8") == "# Decisão humana\n"


def test_sync_is_deterministic_for_same_revision(tmp_path: Path):
    (tmp_path / "abs_core").mkdir()
    (tmp_path / "abs_core" / "orchestrator.py").write_text("x", encoding="utf-8")
    first = RepositoryScanner(tmp_path).scan().to_dict()
    second = RepositoryScanner(tmp_path).scan().to_dict()
    assert first == second



def test_scanner_does_not_promote_every_module_to_capability(tmp_path: Path):
    (tmp_path / "abs_core").mkdir()
    (tmp_path / "abs_core" / "random_module.py").write_text("x", encoding="utf-8")
    k = RepositoryScanner(tmp_path).scan()
    assert not any(
        x["id"] == "capability:module:abs_core/random_module.py"
        for x in k.capabilities
    )


def test_path_evaluator_is_used_by_sync(tmp_path: Path):
    (tmp_path / "abs_core").mkdir()
    (tmp_path / "abs_core" / "codex_adapter.py").write_text("x", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_codex_cli_adapter.py").write_text("x", encoding="utf-8")
    result = synchronize(
        tmp_path, tmp_path / "knowledge", test_status="tested", test_detail="1 passed"
    )
    data = __import__("json").loads(
        Path(result["state"]).read_text(encoding="utf-8")
    )
    path = next(x for x in data["paths"] if x["id"] == "PATH-ABS-CODEX")
    assert path["state"] == "tested"


def test_git_commit_event_is_discovered_when_revision_exists(tmp_path: Path):
    import subprocess

    (tmp_path / "abs_core").mkdir()
    (tmp_path / "abs_core" / "orchestrator.py").write_text("x", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "initial"], cwd=tmp_path, check=True)
    k = RepositoryScanner(tmp_path).scan()
    assert any(e["type"] == "commit_observed" for e in k.events)


def test_commit_event_contains_branch_and_subject(tmp_path: Path):
    import subprocess

    (tmp_path / "abs_core").mkdir()
    (tmp_path / "abs_core" / "orchestrator.py").write_text("x", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "construction event"], cwd=tmp_path, check=True)
    k = RepositoryScanner(tmp_path).scan()
    event = next(e for e in k.events if e["type"] == "commit_observed")
    assert event["subject"] == "construction event"
    assert event["branch"] in {"master", "main"}


def test_repository_resource_contains_provenance(tmp_path: Path):
    import subprocess

    (tmp_path / "abs_core").mkdir()
    (tmp_path / "abs_core" / "orchestrator.py").write_text("x", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "provenance"], cwd=tmp_path, check=True)
    resource = RepositoryScanner(tmp_path).scan().resources[0]
    assert resource["revision"]
    assert resource["commit_subject"] == "provenance"
    assert resource["branch"] in {"master", "main"}


def test_projection_includes_runtime_categories_and_path_evidence(tmp_path: Path):
    (tmp_path / "abs_core").mkdir()
    (tmp_path / "abs_core" / "codex_adapter.py").write_text("x", encoding="utf-8")
    result = synchronize(
        tmp_path, tmp_path / "knowledge", test_status="tested", test_detail="1 passed"
    )
    projection = Path(result["map"]).read_text(encoding="utf-8")
    assert "## Recursos" in projection
    assert "## Ferramentas" in projection
    assert "## Nós" in projection
    assert "## Caminhos" in projection
    assert "evidências:" in projection


def test_capability_discovery_expands_paths_without_manual_map_edit(tmp_path: Path):
    (tmp_path / "abs_core").mkdir()
    (tmp_path / "abs_core" / "internet_adapter.py").write_text("x", encoding="utf-8")
    k = RepositoryScanner(tmp_path).scan()
    path = next(p for p in k.paths if p.id == "PATH-ABS-INTERNET-HTTP")
    assert path.state == "observed"
    assert "abs_core/internet_adapter.py" in path.tools


def test_continuity_layers_are_observed_with_provenance(tmp_path: Path):
    (tmp_path / "abs_core").mkdir()
    (tmp_path / "abs_core" / "orchestrator.py").write_text("x", encoding="utf-8")
    (tmp_path / "continuidade/01_contexto").mkdir(parents=True)
    (tmp_path / "continuidade/03_decisoes").mkdir(parents=True)
    (tmp_path / "continuidade/07_conhecimento").mkdir(parents=True)
    (tmp_path / "continuidade/05_handoffs").mkdir(parents=True)
    (tmp_path / "docs/00_governanca").mkdir(parents=True)
    (tmp_path / "99_arquivo").mkdir()
    required = {
        "continuidade/01_contexto/01_MODELO_ABS_E_PRINCIPIOS.md",
        "continuidade/03_decisoes/01_DECISOES_CORRECOES_E_REGRAS.md",
        "docs/00_governanca/PESQUISA_PRESERVACAO_CONTEXTO_CONTINUIDADE_V1.md",
        "docs/00_governanca/PESQUISA_TRAJETORIA_PROVENIENCIA_BIDIRECIONAL_V1.md",
        "continuidade/07_conhecimento/03_CONTRATO_DE_PROVA.md",
        "continuidade/07_conhecimento/project_knowledge.json",
        "continuidade/07_conhecimento/SESSAO_ATUAL.md",
        "continuidade/05_handoffs/05_HANDOFF_ATUAL_COMPLETO_2026-10-03.md",
        "00_IA_NAVEGACAO.md",
        "99_arquivo/README.md",
    }
    for rel in required:
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rel, encoding="utf-8")
    knowledge = RepositoryScanner(tmp_path).scan()
    sources = {item.id: item for item in knowledge.knowledge_sources}
    assert len(sources) == 10
    assert all(item.status == "present" for item in sources.values())
    assert sources["source:decisions"].authority == "human_authority"
    assert sources["source:history"].temporal == "historical"
    assert sources["source:research"].layer == "research"
    assert sources["source:handoff"].layer == "handoff"
    assert all(item.sha256 for item in sources.values())


def test_projection_exposes_continuity_layers(tmp_path: Path):
    (tmp_path / "abs_core").mkdir()
    (tmp_path / "abs_core" / "orchestrator.py").write_text("x", encoding="utf-8")
    result = synchronize(tmp_path, tmp_path / "knowledge")
    projection = Path(result["map"]).read_text(encoding="utf-8")
    assert "## Camadas de continuidade" in projection
    assert "source:handoff" in projection
    assert "source:decisions" in projection


def test_trajectory_schema_exposes_relations_and_git_lineage(tmp_path: Path):
    import subprocess
    (tmp_path / "abs_core").mkdir()
    file_path = tmp_path / "abs_core" / "orchestrator.py"
    file_path.write_text("v1", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "origin"], cwd=tmp_path, check=True)
    file_path.write_text("v2", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "change"], cwd=tmp_path, check=True)

    knowledge = RepositoryScanner(tmp_path).scan()
    data = knowledge.to_dict()

    assert data["schema_version"] == "1.3"
    assert data["relations"]
    assert any(r["relation"] == "precedes" for r in data["relations"])
    assert any(
        r["relation"] == "changed" and r["target"] == "file:abs_core/orchestrator.py"
        for r in data["relations"]
    )


def test_trajectory_links_observation_to_evidence(tmp_path: Path):
    (tmp_path / "abs_core").mkdir()
    (tmp_path / "abs_core" / "orchestrator.py").write_text("x", encoding="utf-8")
    knowledge = RepositoryScanner(tmp_path).scan()

    event_ids = {e["id"] for e in knowledge.events if e.get("evidence_id")}
    linked = {
        r.source for r in knowledge.relations
        if r.relation == "generated"
    }

    assert event_ids
    assert event_ids <= linked


def test_trajectory_projection_is_present(tmp_path: Path):
    (tmp_path / "abs_core").mkdir()
    (tmp_path / "abs_core" / "orchestrator.py").write_text("x", encoding="utf-8")
    result = synchronize(tmp_path, tmp_path / "knowledge")
    projection = Path(result["map"]).read_text(encoding="utf-8")

    assert "## Relações de trajetória" in projection


def test_projection_tolerates_missing_path_evidence(tmp_path: Path):
    from abs_core.project_knowledge import PathRecord, ProjectKnowledge

    knowledge = ProjectKnowledge()
    knowledge.paths = [
        PathRecord("PATH-X", "test", "a", "b", "observed", evidence=[None, "evidence:test"])
    ]
    result = KnowledgeStore(tmp_path).write(knowledge)
    projection = Path(result["map"]).read_text(encoding="utf-8")
    assert "evidence:test" in projection
