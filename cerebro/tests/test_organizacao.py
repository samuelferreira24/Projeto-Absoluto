from cerebro.nucleo import RepositorioJSONL, novo_registro
from cerebro.organizacao import FilaOrganizacao


def test_fila_cria_tarefa_idempotente(tmp_path):
    repo = RepositorioJSONL(tmp_path / "data")
    registro = novo_registro(repo, "DESCOBERTA", "Descoberta", "conteúdo")
    fila = FilaOrganizacao(tmp_path / "data" / "organizacao.jsonl")

    primeira = fila.adicionar(registro, sinal=0.8)
    segunda = fila.adicionar(registro, sinal=0.9)

    assert primeira.idempotency_key == segunda.idempotency_key
    assert len(fila.pendentes()) == 1
    assert fila.pendentes()[0].prioridade_sinal == 0.8


def test_fila_conclui_tarefa(tmp_path):
    repo = RepositorioJSONL(tmp_path / "data")
    registro = novo_registro(repo, "ENTENDIMENTO", "Entendimento", "conteúdo")
    fila = FilaOrganizacao(tmp_path / "data" / "organizacao.jsonl")
    tarefa = fila.adicionar(registro)

    fila.concluir(tarefa.idempotency_key, {"relacoes": 2})

    assert fila.pendentes() == []
