from cerebro.operacao import operar_entrada
from cerebro.servico import Cerebro


def test_operacao_completa_preserva_entrada_e_produz_aprendizado(tmp_path):
    entrada = tmp_path / "entrada.md"
    entrada.write_text("Conhecimento operacional de teste.", encoding="utf-8")

    cerebro = Cerebro(tmp_path / "data")
    resultado = operar_entrada(cerebro, entrada, objetivo="processar conhecimento")

    assert resultado.entrada_id.startswith("DOCUMENTO-")
    assert resultado.tarefas_planejadas == (f"operacao:{resultado.entrada_id}",)
    assert resultado.tarefas_concluidas == resultado.tarefas_planejadas
    assert resultado.aprendizados_registrados == 1
    assert resultado.consolidado >= 1
    assert cerebro.buscar("Conhecimento operacional", 5)
    assert cerebro.estado.status == "OPERACIONAL"
    assert (tmp_path / "memoria" / "aprendizados.jsonl").exists()


def test_operacao_repetida_preserva_as_duas_fontes(tmp_path):
    entrada = tmp_path / "entrada.txt"
    entrada.write_text("mesmo conteúdo", encoding="utf-8")
    cerebro = Cerebro(tmp_path / "data")

    primeira = operar_entrada(cerebro, entrada)
    segunda = operar_entrada(cerebro, entrada)

    assert primeira.entrada_id != segunda.entrada_id
    assert len(cerebro.registros()) == 2
