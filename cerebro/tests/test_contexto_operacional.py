from pathlib import Path

from cerebro.contexto_operacional import AcaoContexto, ContextoOperacional, DecisaoContexto, construir_contexto, gerar_prompt_contexto, validar_contexto
from cerebro.servico import Cerebro
from cerebro.grafo_tarefas import NoTarefa


def test_contexto_carrega_o_que_como_por_que_e_proximo_passo(tmp_path: Path):
    cerebro = Cerebro(tmp_path / "data")
    cerebro.estado.atualizar(next_priority="implementar continuidade", in_construction=["contexto compartilhado"], open_problems=["validar handoff"], risks=["contexto desatualizado"])
    cerebro.adicionar_tarefa(NoTarefa(id="t1", objetivo="testar contexto", prioridade=10))

    contexto = construir_contexto(cerebro, objetivo="garantir continuidade entre chats", proximo_passo="executar testes", contexto_da_sessao={"como_esta_sendo_feito": ["blackboard estruturado"], "por_que_esta_sendo_feito": ["qualquer chat precisa entender o trabalho atual"], "restricoes": ["não perder histórico"]})

    assert contexto.objetivo == "garantir continuidade entre chats"
    assert "contexto compartilhado" in contexto.o_que_esta_sendo_feito
    assert "blackboard estruturado" in contexto.como_esta_sendo_feito
    assert contexto.por_que_esta_sendo_feito == ["qualquer chat precisa entender o trabalho atual"]
    assert contexto.proximo_passo == "executar testes"
    assert "validar handoff" in contexto.bloqueios


def test_contexto_e_serializavel_e_validavel(tmp_path: Path):
    contexto = ContextoOperacional(objetivo="teste", o_que_esta_sendo_feito=["x"], como_esta_sendo_feito=["y"], proximo_passo="z", decisoes=[DecisaoContexto(id="d1", decisao="usar blackboard", motivo="continuidade")], acoes_recentes=[AcaoContexto(id="a1", acao="pesquisar", motivo="validar arquitetura", resultado="evidências")])
    assert validar_contexto(contexto.to_dict()) == []
    caminho = tmp_path / "contexto.json"
    contexto.salvar(caminho)
    carregado = ContextoOperacional.carregar(caminho)
    assert carregado.objetivo == "teste"
    assert carregado.decisoes[0].decisao == "usar blackboard"
    assert carregado.acoes_recentes[0].resultado == "evidências"


def test_prompt_explica_estado_e_regras_antes_da_acao():
    contexto = {"objetivo": "continuar projeto", "o_que_esta_sendo_feito": ["orquestração"], "como_esta_sendo_feito": ["grafo de tarefas"], "por_que_esta_sendo_feito": ["manter continuidade"], "plano_atual": ["pesquisar", "implementar", "validar"], "proximo_passo": "pesquisar", "decisoes": [], "acoes_recentes": [], "mudancas_desde_ultima_sessao": [], "bloqueios": [], "riscos": [], "restricoes": []}
    prompt = gerar_prompt_contexto(contexto)
    assert "O que está sendo feito" in prompt
    assert "Como está sendo feito" in prompt
    assert "Por que está sendo feito" in prompt
    assert "Antes de agir" in prompt
