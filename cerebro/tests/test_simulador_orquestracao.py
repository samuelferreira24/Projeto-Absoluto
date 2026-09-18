from cerebro.agendador import AgendadorAdaptativo
from cerebro.grafo_tarefas import GrafoTarefas, NoTarefa
from cerebro.simulador_orquestracao import CenarioSimulacao, SimuladorOrquestracao


def _base():
    g = GrafoTarefas()
    g.adicionar_varias([
        NoTarefa("a", "A", recursos=("cpu",), valor_estimado=10, custo_estimado=1, tempo_estimado=10),
        NoTarefa("b", "B", recursos=("gpu",), valor_estimado=9, custo_estimado=1, tempo_estimado=2),
    ])
    return g


def test_simulacao_nao_muda_estado():
    g = _base()
    plano = AgendadorAdaptativo(g).planejar({"cpu", "gpu"})
    antes = {k: v.estado for k, v in g.tarefas.items()}
    resultado = SimuladorOrquestracao(g).simular(plano, [CenarioSimulacao("BASE")])[0]
    assert resultado.executaveis
    assert antes == {k: v.estado for k, v in g.tarefas.items()}


def test_makespan_paralelo_e_cenario_lento():
    g = _base()
    plano = AgendadorAdaptativo(g).planejar({"cpu", "gpu"})
    sim = SimuladorOrquestracao(g)
    base = sim.simular(plano, [CenarioSimulacao("BASE")])[0]
    lento = sim.simular(plano, [CenarioSimulacao("LENTO", fator_tempo=1.5)])[0]
    assert base.makespan == 10
    assert lento.makespan > base.makespan
    assert lento.robustez < base.robustez


def test_selecao_robusta_preserva_alternativas():
    g = _base()
    planos = AgendadorAdaptativo(g).planos_candidatos({"cpu", "gpu"}, limite=2)
    escolhido, diagnostico = SimuladorOrquestracao(g).selecionar_robusto(planos)
    assert escolhido is not None
    assert diagnostico["avaliados"] >= 1
    assert diagnostico["escolhido"] == [t.id for t in escolhido.tarefas]
