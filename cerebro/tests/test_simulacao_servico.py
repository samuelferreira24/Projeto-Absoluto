from cerebro.servico import Cerebro
from cerebro.grafo_tarefas import NoTarefa


def test_cerebro_expone_simulacao_sem_alterar_grafo(tmp_path):
    cerebro = Cerebro(tmp_path / "data")
    cerebro.adicionar_tarefa(NoTarefa("a", "A", valor_estimado=5, custo_estimado=1, tempo_estimado=3))
    planos = cerebro.planos_candidatos(limite=1)
    estado_antes = cerebro.grafo_tarefas.tarefas["a"].estado
    resultados = cerebro.simular_planos(planos)
    assert resultados
    assert resultados[0]["resultados"]
    assert cerebro.grafo_tarefas.tarefas["a"].estado == estado_antes


def test_cerebro_seleciona_plano_robusto(tmp_path):
    cerebro = Cerebro(tmp_path / "data")
    cerebro.adicionar_tarefa(NoTarefa("a", "A", valor_estimado=5, custo_estimado=1, tempo_estimado=3))
    escolhido = cerebro.selecionar_plano_robusto(cerebro.planos_candidatos(limite=1))
    assert escolhido is not None
    assert escolhido.tarefas[0].id == "a"
