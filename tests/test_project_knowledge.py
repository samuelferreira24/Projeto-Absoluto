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
