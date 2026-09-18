from pathlib import Path
from zipfile import ZipFile

from cerebro.fontes_base import FONTES_BASE, auditar_fontes, ingerir_fontes_base
from cerebro.nucleo import RepositorioJSONL


def _docx(path: Path, texto: str) -> None:
    ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <w:document xmlns:w="{ns}"><w:body><w:p><w:r><w:t>{texto}</w:t></w:r></w:p></w:body></w:document>'''
    with ZipFile(path, "w") as z:
        z.writestr("[Content_Types].xml", '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>')
        z.writestr("word/document.xml", xml)


def test_as_tres_fontes_base_sao_identificadas(tmp_path):
    for i, fonte in enumerate(FONTES_BASE):
        _docx(tmp_path / fonte.arquivo, f"fonte {i}")

    auditoria = auditar_fontes(tmp_path)
    assert len(auditoria) == 3
    assert all(x["existe"] for x in auditoria)
    assert all(x["texto_extraido"] for x in auditoria)
    assert {x["fonte"]["funcao"] for x in auditoria} == {
        "VISAO_E_PROJETO",
        "MEMORIA_E_CEREBRO",
        "REPRESENTACAO_E_ARMAZENAMENTO",
    }


def test_ingestao_das_fontes_e_idempotente(tmp_path):
    for i, fonte in enumerate(FONTES_BASE):
        _docx(tmp_path / fonte.arquivo, f"fonte {i}")

    repo = RepositorioJSONL(tmp_path / "data")
    primeira = ingerir_fontes_base(repo, tmp_path)
    segunda = ingerir_fontes_base(repo, tmp_path)

    assert {x["status"] for x in primeira["resultados"]} == {"INGERIDA"}
    assert {x["status"] for x in segunda["resultados"]} == {"JA_INGESTA"}
    assert len([r for r in repo._iter_registros() if r.kind == "DOCUMENTO"]) == 3
