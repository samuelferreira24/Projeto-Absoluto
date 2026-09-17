from cerebro.ingestao import extrair, registrar_fonte
from cerebro.nucleo import RepositorioJSONL


def test_ingestao_preserva_fonte_original_por_hash(tmp_path):
    fonte = tmp_path / "original.md"
    fonte.write_text("# Fonte\nConteúdo original.", encoding="utf-8")
    repo = RepositorioJSONL(tmp_path / "data")

    registro = registrar_fonte(repo, extrair(fonte))

    copia = tmp_path / "data" / "fontes" / f"{registro.provenance['sha256']}.md"
    assert copia.exists()
    assert copia.read_bytes() == fonte.read_bytes()
    assert registro.provenance["fonte_original_preservada"] is True
