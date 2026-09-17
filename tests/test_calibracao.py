from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cerebro.ingestao import extrair  # noqa: E402


FONTES_CALIBRACAO = [
    "Projeto_Absoluto_MEMORIA_IA_V10_ATUALIZADO.docx",
    "Projeto_Absoluto_EBOOK_HUMANO_V10_ATUALIZADO.docx",
    "Pesquisa_Representacao_Armazenamento_Informacao_IA_Projeto_Absoluto_v1.docx",
]


def test_calibracao_acervo_real_preserva_origem_e_integridade():
    raiz = Path(__file__).resolve().parents[1]

    for nome in FONTES_CALIBRACAO:
        path = raiz / nome
        assert path.exists(), f"Fonte de calibração ausente: {nome}"
        original = path.read_bytes()

        documento = extrair(path)

        assert documento.erros == [], f"Falha na ingestão de {nome}: {documento.erros}"
        assert documento.formato == "docx"
        assert documento.nome == nome
        assert documento.tamanho == len(original)
        assert len(documento.sha256) == 64
        assert documento.origem == str(path)
        assert documento.texto.strip()
        assert documento.estrutura
        assert path.read_bytes() == original


def test_calibracao_torna_explicito_o_limite_semantico_da_base_atual():
    """A extração estrutural não deve fingir que já fez análise semântica."""
    raiz = Path(__file__).resolve().parents[1]
    documento = extrair(raiz / FONTES_CALIBRACAO[0])

    assert documento.metadados["parser"] == "stdlib-docx-xml"
    assert all(item["tipo"] in {"paragrafo", "tabela"} for item in documento.estrutura)
    # Relações semânticas e distinção entre fato, hipótese, interpretação e decisão
    # ainda são capacidades de camadas posteriores; não são inferidas pelo extrator.
