import pytest

from cerebro.tabuleiro import Caminho, Relacao, Tabuleiro


def caminho(id_: str, nome: str, **kwargs) -> Caminho:
    return Caminho(id=id_, nome=nome, **kwargs)


def test_tabuleiro_permite_varios_caminhos_sem_ordem_fixa():
    a = caminho("A", "Cérebro", valor_multiplicador=0.9)
    b = caminho("B", "Continuidade", reversibilidade=0.9)
    c = caminho("C", "Pesquisa", incerteza=0.8)
    tab = Tabuleiro([a, b, c])

    assert {x.id for x in tab.candidatos()} == {"A", "B", "C"}
    assert len(tab.relacoes) == 0


def test_relacoes_representam_impulso_e_convergencia():
    tab = Tabuleiro([
        caminho("A", "Pesquisa"),
        caminho("B", "Cérebro"),
        caminho("C", "Construção"),
    ])
    tab.adicionar_relacao(Relacao("A", "IMPULSIONA", "B"))
    tab.adicionar_relacao(Relacao("B", "MULTIPLICA_VALOR", "C"))
    tab.adicionar_relacao(Relacao("A", "CONVERGE_COM", "C"))

    assert tab.habilitados_por("A") == ("B",)
    assert set(tab.relacionados("B")) == {"A", "C"}


def test_relacao_exige_caminhos_existentes():
    tab = Tabuleiro([caminho("A", "A")])
    with pytest.raises(ValueError):
        tab.adicionar_relacao(Relacao("A", "HABILITA", "B"))


def test_candidato_contextual_nao_e_regra_de_execucao():
    tab = Tabuleiro([
        caminho("A", "Base", valor_multiplicador=0.2, risco=0.1),
        caminho("B", "Pesquisa", valor_multiplicador=0.5, risco=0.1),
    ])
    primeiro = tab.candidatos({"A": 1.0})[0]
    assert primeiro.id == "A"
    assert {c.id for c in tab.candidatos({"B": 1.0})} == {"A", "B"}


def test_nao_permite_estado_desconhecido():
    with pytest.raises(ValueError):
        caminho("A", "A", estado="ORDEM_FIXA")
