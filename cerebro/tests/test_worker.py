from __future__ import annotations

import sys

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
