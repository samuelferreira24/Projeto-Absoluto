from cerebro.grafo_tarefas import GrafoTarefas, NoTarefa
from cerebro.orquestracao_adaptativa import OrquestradorAdaptativo, Recurso


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


def test_tempo_de_lote_paralelo_e_o_maximo_das_duracoes():
    g = GrafoTarefas()
    g.adicionar_varias([
        NoTarefa("a", "A", recursos=("cpu",), valor_estimado=5, tempo_estimado=10),
        NoTarefa("b", "B", recursos=("gpu",), valor_estimado=5, tempo_estimado=4),
    ])
    o = OrquestradorAdaptativo(g)
    plano = o.plano_adaptativo({"cpu", "gpu"})
    assert [t.id for t in plano] == ["a", "b"]
    assert o.decisoes[-1]["tempo"] == 10

def test_capacidade_de_recurso_limita_concorrencia():
    g = GrafoTarefas()
    g.adicionar_varias([
        NoTarefa("a", "A", recursos=("cpu",), valor_estimado=5),
        NoTarefa("b", "B", recursos=("cpu",), valor_estimado=4),
    ])
    o = OrquestradorAdaptativo(
        g,
        recursos={"cpu": Recurso("cpu", capacidade=1.0)},
    )
    plano = o.plano_adaptativo({"cpu"})
    assert len(plano) == 1


def test_facade_delega_capacity_de_tempo_ao_scheduler():
    g = GrafoTarefas()
    g.adicionar_varias([
        NoTarefa("a", "A", recursos=("cpu",), valor_estimado=5, tempo_estimado=10),
        NoTarefa("b", "B", recursos=("gpu",), valor_estimado=4, tempo_estimado=4),
    ])
    o = OrquestradorAdaptativo(g)
    plano = o.plano_adaptativo({"cpu", "gpu"}, capacidade_de_tempo=5)
    assert [t.id for t in plano] == ["b"]


def test_replanejamento_apos_falha_ativa_fallback():
    g = GrafoTarefas()
    g.adicionar(NoTarefa("a", "principal", fallbacks=("b",), valor_estimado=10))
    g.adicionar(NoTarefa("b", "fallback", valor_estimado=5))
    o = OrquestradorAdaptativo(g)
    o.plano_adaptativo()
    proximo = o.replanejar_apos_resultado("a", False, fallback_tarefa_id="b")
    assert [t.id for t in proximo] == ["b"]
