from cerebro.composicao import (
    Capacidade,
    Combinacao,
    EstadoCombinacao,
    Tarefa,
    determinar_topologia,
    registrar_resultado,
    recursos_em_conflito,
)


def test_tarefas_independentes_podem_ser_paralelas():
    tarefas = (
        Tarefa(id="a", objetivo="pesquisar", capacidades=("pesquisa",)),
        Tarefa(id="b", objetivo="analisar", capacidades=("analise",)),
    )
    assert determinar_topologia(tarefas) == "PARALELO"


def test_dependencia_impede_classificacao_paralela():
    tarefas = (
        Tarefa(id="a", objetivo="pesquisar"),
        Tarefa(id="b", objetivo="sintetizar", depende_de=("a",)),
    )
    assert determinar_topologia(tarefas) == "DEPENDENTE"


def test_recursos_compartilhados_sao_detectados():
    tarefas = (
        Tarefa(id="a", objetivo="x", recursos=("gpu-1",)),
        Tarefa(id="b", objetivo="y", recursos=("gpu-1", "api")),
    )
    assert recursos_em_conflito(tarefas) == {"gpu-1"}


def test_resultado_preserva_registro_anterior_e_adiciona_evidencia():
    combinacao = Combinacao(
        id="c1",
        objetivo="testar sinergia",
        capacidades=("pesquisa", "memoria"),
    )
    resultado = registrar_resultado(
        combinacao,
        estado=EstadoCombinacao.PROMISSORA,
        resultado="ganho observado",
        qualidade=0.8,
        evidencia="teste-001",
        aprendizado="A combinação parece útil neste contexto.",
    )
    assert combinacao.estado == EstadoCombinacao.NAO_TESTADA
    assert resultado.estado == EstadoCombinacao.PROMISSORA
    assert "teste-001" in resultado.evidencias
    assert resultado.qualidade == 0.8
