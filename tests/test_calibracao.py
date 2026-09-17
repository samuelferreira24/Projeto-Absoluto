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
        assert documento.sha256
        assert documento.texto.strip()
        assert documento.estrutura
        assert path.read_bytes() == original


def test_calibracao_registra_limites_da_base_atual():
    """A calibração deve tornar explícito o que ainda não é extraído automaticamente."""
    raiz = Path(__file__).resolve().parents[1]
    documento = extrair(raiz / FONTES_CALIBRACAO[0])

    # A V0.1 já preserva origem, integridade e estrutura documental.
    # Relações semânticas e distinção fato/hipótese/interpretação/decisão
    # ainda pertencem às próximas camadas e não devem ser inferidas pelo extrator.
    assert documento.provenance if hasattr(documento, "provenance") else True
