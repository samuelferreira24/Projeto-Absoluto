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
