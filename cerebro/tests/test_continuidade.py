from pathlib import Path

import pytest

from cerebro.continuidade import ErroContinuidade, validar_manifesto, validar_ou_erro


def manifesto_valido() -> dict:
    return {
        "schema_version": "0.1",
        "project": {"id": "PROJETO-ABSOLUTO", "name": "Projeto Absoluto"},
        "construction": {"current_branch": "base-cerebro-v0.1", "current_stage": "fundacao"},
        "continuity": {"required_file": "docs/continuidade.md"},
        "required_validation": ["tests"],
        "rules": ["preservar histórico"],
        "integration_boundary": {"strategy": "adaptadores por contrato"},
    }


def escrever_manifesto(tmp_path: Path, data: dict) -> Path:
    import json
    root = tmp_path / "repo"
    (root / "docs").mkdir(parents=True)
    (root / "docs" / "continuidade.md").write_text("ok", encoding="utf-8")
    path = root / "manifest.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_manifesto_valido(tmp_path: Path):
    path = escrever_manifesto(tmp_path, manifesto_valido())
    assert validar_manifesto(path, path.parent) == []
    validar_ou_erro(path, path.parent)


def test_detecta_referencia_ausente(tmp_path: Path):
    data = manifesto_valido()
    data["continuity"]["required_file"] = "docs/inexistente.md"
    path = escrever_manifesto(tmp_path, data)
    erros = validar_manifesto(path, path.parent)
    assert any("inexistente" in erro for erro in erros)


def test_detecta_campo_essencial_ausente(tmp_path: Path):
    data = manifesto_valido()
    del data["integration_boundary"]
    path = escrever_manifesto(tmp_path, data)
    with pytest.raises(ErroContinuidade):
        validar_ou_erro(path, path.parent)
