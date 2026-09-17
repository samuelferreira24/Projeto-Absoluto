from cerebro.grafo_tarefas import GrafoTarefas, NoTarefa
from cerebro.orquestracao_adaptativa import OrquestradorAdaptativo


def test_plano_respeita_dependencia_recurso_orcamento_e_tempo():
    g = GrafoTarefas()
    g.adicionar(NoTarefa("a", "A", recursos=("cpu",), valor_estimado=10, custo_estimado=2, tempo_estimado=2))
    g.adicionar(NoTarefa("b", "B", depende_de=("a",), recursos=("cpu",), valor_estimado=20, custo_estimado=2, tempo_estimado=2))
    g.adicionar(NoTarefa("c", "C", recursos=("gpu",), valor_estimado=5, custo_estimado=1, tempo_estimado=1))
    o = OrquestradorAdaptativo(g)
    assert [t.id for t in o.plano_adaptativo({"cpu", "gpu"}, orcamento=3, capacidade_de_tempo=3)] == ["a", "c"]


def test_replanejamento_libera_dependentes():
    g = GrafoTarefas()
    g.adicionar(NoTarefa("a", "A", valor_estimado=10))
    g.adicionar(NoTarefa("b", "B", depende_de=("a",), valor_estimado=20))
    o = OrquestradorAdaptativo(g)
    assert [t.id for t in o.plano_adaptativo()] == ["a"]
    proximo = o.replanejar_apos_resultado("a", True)
    assert [t.id for t in proximo] == ["b"]


def test_sinergia_e_registrada_com_baseline_individual():
    g = GrafoTarefas()
    o = OrquestradorAdaptativo(g)
    o.registrar_resultado(["a"], 4, 1, 1, 0.8)
    o.registrar_resultado(["b"], 6, 1, 1, 0.8)
    s = o.registrar_resultado(["a", "b"], 15, 2, 1, 0.9)
    assert s is not None
    assert s.ganho_observado == 10
    assert s.confianca == 1
