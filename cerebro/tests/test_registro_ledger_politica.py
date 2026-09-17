from cerebro.eventos import Evento
from cerebro.eventos_ledger import LedgerEventos
from cerebro.identidade import identidade_agente
from cerebro.politica import PoliticaAcao, pode_executar
from cerebro.registro import Participante, RegistroParticipantes


def test_registro_participante(tmp_path):
    r = RegistroParticipantes(tmp_path / "participantes.json")
    p = Participante(identidade_agente().id, "AGENTE", "Agente de teste", capacidades=["pesquisa"])
    r.salvar(p)
    assert r.obter(p.id).nome == "Agente de teste"
    assert len(r.listar(tipo="AGENTE")) == 1


def test_ledger_preserva_correlacao_e_integridade(tmp_path):
    l = LedgerEventos(tmp_path / "eventos.jsonl")
    e = Evento(origem="A", tipo="TESTE", destino="B", payload={"x": 1}, correlation_id="c1")
    l.append(e)
    assert l.ids() == {e.event_id}
    assert len(l.por_correlacao("c1")) == 1
    assert l.validar_integridade() == []


def test_politica_exige_autorizacao_para_nivel_6():
    acao = PoliticaAcao("mudança estratégica", 6, reversivel=False, requer_autorizacao=True, justificativa="impacto alto")
    assert not pode_executar(acao, 6)


def test_politica_reversivel_pode_ser_executada_no_nivel_concedido():
    acao = PoliticaAcao("teste", 2)
    assert pode_executar(acao, 2)
    assert pode_executar(acao, 4)
