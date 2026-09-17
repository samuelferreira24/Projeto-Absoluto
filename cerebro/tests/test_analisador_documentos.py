from pathlib import Path

from cerebro.analisador_documentos import analisar_diretorio, analisar_arquivo


def test_analisar_texto(tmp_path: Path):
    arquivo = tmp_path / "base.md"
    arquivo.write_text("# Sistema\n\nO sistema deve ter capacidade de automação e memória.\n", encoding="utf-8")
    resultado = analisar_arquivo(arquivo, tmp_path)
    assert resultado.palavras > 0
    assert resultado.sinais["capacidade"] >= 1
    assert resultado.sinais["automacao"] >= 1
    assert resultado.sinais["memoria"] >= 1
    assert len(resultado.sha256) == 64


def test_analisar_diretorio_gera_inventario(tmp_path: Path):
    (tmp_path / "a.txt").write_text("requisito e planejamento", encoding="utf-8")
    (tmp_path / "b.md").write_text("arquitetura e aprendizado", encoding="utf-8")
    resultado = analisar_diretorio(tmp_path)
    assert resultado["quantidade_documentos"] == 2
    assert resultado["formatos"] == {".md": 1, ".txt": 1}
    assert resultado["sinais_globais"]["requisito"] >= 1
