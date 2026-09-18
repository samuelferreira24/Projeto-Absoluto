from datetime import datetime, timedelta, timezone

import pytest

from cerebro.controle_execucao import ClaimTarefa, ControleExecucao


def test_claim_impede_dispatch_duplicado(tmp_path):
    controle = ControleExecucao(tmp_path / "controle.json", lease_segundos=60)
    controle.claim("t1")

    with pytest.raises(RuntimeError):
        controle.claim("t1")


def test_claim_expirado_pode_ser_reivindicado_novamente(tmp_path):
    controle = ControleExecucao(tmp_path / "controle.json", lease_segundos=60)
    controle.claims["t1"] = ClaimTarefa(
        tarefa_id="t1",
        claim_id="old",
        adquirido_em="2026-01-01T00:00:00+00:00",
        expira_em=(datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat(),
    )
    novo = controle.claim("t1")

    assert novo.tarefa_id == "t1"
    assert novo.tentativa == 2
    assert novo.claim_id != "old"


def test_falha_agenda_retry_e_reconcilia_expiracao(tmp_path):
    controle = ControleExecucao(tmp_path / "controle.json", lease_segundos=60)
    controle.claim("t1")
    controle.falhar("t1", "falha transitória", retry_segundos=0)

    assert controle.prontas_para_retry() == ["t1"]

    controle.claims["t2"] = ClaimTarefa(
        tarefa_id="t2",
        claim_id="expired",
        adquirido_em="2026-01-01T00:00:00+00:00",
        expira_em=(datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat(),
    )
    assert controle.reconciliar() == ["t2"]
    assert controle.claims["t2"].estado == "EXPIRADA"


def test_persistencia_recarrega_claims(tmp_path):
    caminho = tmp_path / "controle.json"
    primeiro = ControleExecucao(caminho)
    primeiro.claim("t1")

    segundo = ControleExecucao(caminho)

    assert "t1" in segundo.claims
    assert segundo.claims["t1"].claim_id == primeiro.claims["t1"].claim_id


def test_claim_recarrega_e_impede_claim_duplicado(tmp_path):
    caminho = tmp_path / "controle.json"
    primeiro = ControleExecucao(caminho)
    primeiro.claim("t1")
    segundo = ControleExecucao(caminho)
    with pytest.raises(RuntimeError):
        segundo.claim("t1")
    segundo.liberar("t1")
    terceiro = ControleExecucao(caminho)
    assert terceiro.claim("t1").tentativa == 2


def test_reconciliacao_do_servico_desbloqueia_tarefa_expirada(tmp_path):
    from cerebro.servico import Cerebro
    from cerebro.grafo_tarefas import NoTarefa, EstadoTarefa, GrafoTarefas
    cerebro = Cerebro(tmp_path / "data")
    cerebro.adicionar_tarefa(NoTarefa("t1", "executar"))
    cerebro.grafo_tarefas.marcar("t1", EstadoTarefa.EXECUTANDO)
    cerebro.controle_execucao.claims["t1"] = ClaimTarefa(
        tarefa_id="t1",
        claim_id="expired",
        adquirido_em="2026-01-01T00:00:00+00:00",
        expira_em=(datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat(),
    )
    cerebro.controle_execucao.salvar()
    assert cerebro.reconciliar_execucao() == ["t1"]
    assert cerebro.grafo_tarefas.tarefas["t1"].estado == EstadoTarefa.PENDENTE
