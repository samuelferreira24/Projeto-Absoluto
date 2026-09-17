from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cerebro.ingestao import extrair  # noqa: E402


ACERVO_REPRESENTATIVO = [
    "Conversaweb.mht",
    "Transcricao_Conversa.txt",
    "Relatorio_Diagnostico_Completo_da_Conversa.docx",
]


def test_acervo_representativo_preserva_fonte_e_produz_conteudo():
    raiz = Path(__file__).resolve().parents[1]

    for nome in ACERVO_REPRESENTATIVO:
        path = raiz / nome
        assert path.exists(), f"Arquivo representativo ausente: {nome}"
        original = path.read_bytes()

        documento = extrair(path)

        assert documento.erros == [], f"Falha na ingestão de {nome}: {documento.erros}"
        assert documento.nome == nome
        assert documento.tamanho == len(original)
        assert len(documento.sha256) == 64
        assert documento.origem == str(path)
        assert documento.texto.strip(), f"Nenhum conteúdo extraído de {nome}"
        assert documento.estrutura, f"Nenhuma estrutura extraída de {nome}"
        assert documento.metadados.get("parser")
        assert path.read_bytes() == original


def test_acervo_representativo_mantem_formatos_distintos():
    raiz = Path(__file__).resolve().parents[1]
    documentos = [extrair(raiz / nome) for nome in ACERVO_REPRESENTATIVO]

    assert [d.formato for d in documentos] == ["mht", "txt", "docx"]
    assert len({d.metadados["parser"] for d in documentos}) == 3
