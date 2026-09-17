from __future__ import annotations

from cerebro.orquestrador import Missao
from cerebro.servico import Cerebro


def test_cerebro_expõe_despertar_persistente(tmp_path):
    cerebro = Cerebro(tmp_path)
    cerebro.registrar_missao(Missao("m1", "objetivo"))

    pedido = cerebro.solicitar_despertar("m1", "evento_externo", correlation_id="corr-1")

    recarregado = Cerebro(tmp_path)
    assert recarregado.despertares_pendentes("m1")[0].id == pedido.id
    assert recarregado.diagnostico()["despertares_pendentes"] == 1
