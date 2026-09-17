import pytest

from cerebro.rede_evolutiva import ArestaRede, NoRede, RedeEvolutiva


def rede_basica() -> RedeEvolutiva:
    rede = RedeEvolutiva()
    rede.adicionar_no(NoRede("objetivo", "OBJETIVO", "Objetivo"))
    rede.adicionar_no(NoRede("pesquisa", "PESQUISA", "Pesquisa", potencial_multiplicador=2))
    rede.adicionar_no(NoRede("capacidade", "CAPACIDADE", "Capacidade", potencial_multiplicador=3))
    rede.adicionar_no(NoRede("experiencia", "EXPERIENCIA", "Experiência", potencial_multiplicador=1))
    return rede


def test_rede_permite_caminhos_paralelos_e_convergencia():
    rede = rede_basica()
    rede.conectar(ArestaRede("pesquisa", "INFORMA", "objetivo"))
    rede.conectar(ArestaRede("capacidade", "CONVERGE_COM", "objetivo"))
    rede.conectar(ArestaRede("experiencia", "CONVERGE_COM", "objetivo"))

    assert set(rede.caminhos_que_convergem("objetivo")) == {"capacidade", "experiencia"}
    assert rede.sucessores("pesquisa", "INFORMA") == ["objetivo"]


def test_valor_multiplicador_cria_ponto_de_alavancagem():
    rede = rede_basica()
    rede.conectar(ArestaRede("capacidade", "MULTIPLICA", "objetivo", peso=2))
    rede.conectar(ArestaRede("pesquisa", "HABILITA", "objetivo", peso=1))

    assert rede.impulso_total("objetivo") == 8
    assert rede.pontos_de_alavancagem(1)[0] == ("objetivo", 8)


def test_rede_rejeita_relacao_invalida():
    with pytest.raises(ValueError):
        ArestaRede("a", "INVALIDA", "b")


def test_rede_rejeita_conexao_para_no_inexistente():
    rede = rede_basica()
    with pytest.raises(KeyError):
        rede.conectar(ArestaRede("pesquisa", "HABILITA", "nao-existe"))


def test_validacao_detecta_integridade():
    rede = rede_basica()
    assert rede.validar() == []


def test_rede_expoe_relacionamentos_sem_impor_ordem():
    rede = rede_basica()
    rede.conectar(ArestaRede("pesquisa", "IMPULSIONA", "objetivo"))
    rede.conectar(ArestaRede("experiencia", "MULTIPLICA_VALOR", "objetivo"))

    assert set(rede.relacionados("objetivo")) == {"pesquisa", "experiencia"}
    assert set(rede.caminhos_que_impulsionam("objetivo")) == {"pesquisa"}


def test_candidatos_sao_sinais_contextuais_e_nao_fila_fixa():
    rede = rede_basica()
    candidatos = rede.candidatos_contextuais({"experiencia": 10.0})

    assert candidatos[0][0] == "experiencia"
    assert {item[0] for item in candidatos} == {"objetivo", "pesquisa", "capacidade", "experiencia"}


def test_adicionar_nos_em_lote():
    rede = RedeEvolutiva()
    rede.adicionar_nos([
        NoRede("a", "IDEIA", "A"),
        NoRede("b", "IDEIA", "B"),
    ])
    assert set(rede.nos) == {"a", "b"}
