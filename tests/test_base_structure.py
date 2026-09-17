import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CEREBRO = ROOT / "cerebro"


def test_required_paths():
    required = [
        CEREBRO / "README.md",
        CEREBRO / "especificacao" / "BASE_V0_1.md",
        CEREBRO / "especificacao" / "SCHEMA_REGISTRO_V0_1.json",
        CEREBRO / "especificacao" / "ARQUITETURA_INGESTAO_V0_1.md",
        CEREBRO / "especificacao" / "ROADMAP_V0_1.md",
        CEREBRO / "ESTRUTURA_ATUAL_V0_1.md",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.is_file()]
    assert not missing, f"Arquivos fundamentais ausentes: {missing}"


def test_schema_is_valid_json():
    schema_path = CEREBRO / "especificacao" / "SCHEMA_REGISTRO_V0_1.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    assert schema.get("$schema")
    assert schema.get("type") == "object"
    required = set(schema.get("required", []))
    expected = {"id", "kind", "title", "created_at", "content", "state", "version"}
    assert expected.issubset(required)
    assert schema.get("additionalProperties") is True


def test_current_snapshot_mentions_calibration_material():
    snapshot = (CEREBRO / "ESTRUTURA_ATUAL_V0_1.md").read_text(encoding="utf-8")
    names = [
        "Projeto_Absoluto_MEMORIA_IA_V10_ATUALIZADO.docx",
        "Projeto_Absoluto_EBOOK_HUMANO_V10_ATUALIZADO.docx",
        "Pesquisa_Representacao_Armazenamento_Informacao_IA_Projeto_Absoluto_v1.docx",
    ]
    for name in names:
        assert name in snapshot


if __name__ == "__main__":
    tests = [
        test_required_paths,
        test_schema_is_valid_json,
        test_current_snapshot_mentions_calibration_material,
    ]
    for test in tests:
        test()
        print(f"PASS: {test.__name__}")
    print("BASE V0.1: validação estrutural concluída")
