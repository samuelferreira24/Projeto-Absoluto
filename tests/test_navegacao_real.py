from __future__ import annotations

from tools.navegacao.validate_real import validate


def test_real_validation_harness(tmp_path):
    first = tmp_path / "first"; second = tmp_path / "second"
    first.mkdir(); second.mkdir()
    (first / "navigator.py").write_text(
        "class Navigator: pass\n# provenance verification\n", encoding="utf-8")
    (second / "Sistema.md").write_text(
        "# Sistema\nKnowledge source for navigation.\n", encoding="utf-8")
    result = validate(tmp_path / "nav.sqlite", {"projeto-absoluto": first, "sistema": second})
    assert result["status"] == "PASS"
    assert result["provenance"]["invalid"] == 0
    assert sum(item["evidence"] for item in result["query_matrix"]) >= 2
