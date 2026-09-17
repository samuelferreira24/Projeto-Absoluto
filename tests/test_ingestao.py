import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cerebro.ingestao import extrair, registrar_fonte  # noqa: E402
from cerebro.nucleo import RepositorioJSONL  # noqa: E402


def _criar_docx_minimo(path: Path) -> None:
    document_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
      <w:body>
        <w:p><w:r><w:t>Documento de teste do Cérebro.</w:t></w:r></w:p>
        <w:p><w:r><w:t>Segunda linha.</w:t></w:r></w:p>
      </w:body>
    </w:document>'''
    with ZipFile(path, "w", ZIP_DEFLATED) as archive:
        archive.writestr("word/document.xml", document_xml)


def test_ingestao_docx_preserva_identidade_e_extrai_texto():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "fonte.docx"
        _criar_docx_minimo(path)
        original = path.read_bytes()

        documento = extrair(path)

        assert documento.formato == "docx"
        assert documento.nome == "fonte.docx"
        assert documento.tamanho == len(original)
        assert len(documento.sha256) == 64
        assert "Documento de teste do Cérebro." in documento.texto
        assert len(documento.estrutura) == 2
        assert documento.erros == []
        assert path.read_bytes() == original


def test_ingestao_txt_e_registro_com_proveniencia():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "fonte.txt"
        path.write_text("Fonte original", encoding="utf-8")
        documento = extrair(path)
        repo = RepositorioJSONL(Path(tmp) / "cerebro")

        registro = registrar_fonte(repo, documento)

        assert registro.kind == "DOCUMENTO"
        assert registro.source == str(path)
        assert registro.provenance["tipo"] == "ingestao"
        assert registro.provenance["sha256"] == documento.sha256
        assert repo.buscar("Fonte original")[0].id == registro.id
