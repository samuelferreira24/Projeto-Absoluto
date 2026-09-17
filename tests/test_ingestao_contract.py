import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cerebro.ingestao.contrato import (  # noqa: E402
    IntermediateDocument,
    SourceIdentity,
    fingerprint_source,
    identify_format,
)


def test_identify_supported_formats():
    assert identify_format("documento.docx") == "DOCX"
    assert identify_format("documento.pdf") == "PDF"
    assert identify_format("documento.mht") == "MHT"
    assert identify_format("documento.md") == "MARKDOWN"


def test_identify_unknown_format_fails_explicitly():
    try:
        identify_format("documento.xyz")
    except ValueError as exc:
        assert "Formato não suportado" in str(exc)
    else:
        raise AssertionError("Formato desconhecido deveria falhar explicitamente")


def test_source_fingerprint_is_stable_and_non_destructive():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "fonte.txt"
        path.write_text("conteúdo de teste", encoding="utf-8")
        before = path.read_bytes()

        identity = fingerprint_source(path)

        assert isinstance(identity, SourceIdentity)
        assert identity.name == "fonte.txt"
        assert identity.format == "TXT"
        assert identity.size_bytes == len(before)
        assert len(identity.sha256) == 64
        assert path.read_bytes() == before


def test_intermediate_document_holds_source_and_provenance():
    source = SourceIdentity("fonte.txt", "TXT", 10, "a" * 64)
    document = IntermediateDocument(
        source=source,
        text="texto",
        structure=[{"type": "paragraph", "text": "texto"}],
        provenance=[{"source": source.name}],
    )

    assert document.source is source
    assert document.text == "texto"
    assert document.structure[0]["type"] == "paragraph"
    assert document.provenance[0]["source"] == "fonte.txt"
