from __future__ import annotations

import sys

import cerebro.worker as worker
from cerebro.orquestrador import Missao
from cerebro.servico import Cerebro
from cerebro.worker import executar_pedidos_pendentes


def test_worker_processa_pedido_com_executor_externo(tmp_path):
    cerebro = Cerebro(tmp_path)
    cerebro.registrar_missao(Missao("m1", "objetivo"))
    pedido = cerebro.solicitar_despertar("m1", "teste")

    comando = f'{sys.executable} -c "import json,sys; d=json.load(sys.stdin); print(json.dumps({{\"ok\": True, \"missao\": d[\"missao\"][\"id\"]}}))"'
    resultado = executar_pedidos_pendentes(cerebro, comando)

    assert resultado[0]["executado"] is True
    assert resultado[0]["resultado"]["missao"] == "m1"
    assert cerebro.despertador.pedidos[0].id == pedido.id
    assert cerebro.despertador.pedidos[0].estado == "CONCLUIDO"


def test_worker_registra_falha_do_executor(tmp_path):
    cerebro = Cerebro(tmp_path)
    cerebro.registrar_missao(Missao("m1", "objetivo"))
    cerebro.solicitar_despertar("m1", "teste")

    comando = f'{sys.executable} -c "import sys; print(\"falhou\", file=sys.stderr); sys.exit(3)"'
    resultado = executar_pedidos_pendentes(cerebro, comando)

    assert resultado[0]["executado"] is False
    assert cerebro.despertador.pedidos[0].estado == "FALHOU"


def test_worker_continuo_respeita_limite(monkeypatch):
    chamadas = []

    def fake_lote(cerebro, comando):
        chamadas.append((cerebro, comando))
        return [{"executado": True}]

    monkeypatch.setattr(worker, "executar_pedidos_pendentes", fake_lote)
    resultados = worker.executar_continuamente(object(), "executor", intervalo_segundos=0, max_ciclos=2)

    assert len(chamadas) == 2
    assert len(resultados) == 2


def test_worker_rejeita_intervalo_negativo():
    try:
        worker.executar_continuamente(object(), "executor", intervalo_segundos=-1, max_ciclos=1)
    except ValueError as exc:
        assert "intervalo_segundos" in str(exc)
    else:
        raise AssertionError("intervalo negativo deveria ser rejeitado")
