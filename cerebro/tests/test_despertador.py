from __future__ import annotations

from datetime import datetime, timedelta, timezone

from cerebro.despertador import Despertador


def test_pedido_de_despertar_persiste_e_pode_ser_processado(tmp_path):
    path = tmp_path / "despertar.json"
    despertador = Despertador(path)
    pedido = despertador.solicitar("m1", "github", correlation_id="corr-1")

    recarregado = Despertador(path)
    assert [p.id for p in recarregado.pendentes()] == [pedido.id]

    recarregado.iniciar(pedido.id)
    assert recarregado.pendentes() == []
    recarregado.concluir(pedido.id)

    final = Despertador(path)
    assert final.pedidos[0].estado == "CONCLUIDO"


def test_pedido_falho_preserva_erro(tmp_path):
    despertador = Despertador(tmp_path / "despertar.json")
    pedido = despertador.solicitar("m1", "manual")
    despertador.iniciar(pedido.id)
    despertador.falhar(pedido.id, "executor indisponível")

    recarregado = Despertador(tmp_path / "despertar.json")
    assert recarregado.pedidos[0].estado == "FALHOU"
    assert recarregado.pedidos[0].detalhes["erro"] == "executor indisponível"


def test_pedido_processando_abandonado_pode_ser_recuperado(tmp_path):
    path = tmp_path / "despertar.json"
    despertador = Despertador(path, timeout_segundos=1)
    pedido = despertador.solicitar("m1", "worker")
    despertador.iniciar(pedido.id)

    pedido.processando_em = (datetime.now(timezone.utc) - timedelta(seconds=10)).isoformat()
    despertador._salvar()

    recuperado = Despertador(path, timeout_segundos=1)
    assert recuperado.pendentes()[0].id == pedido.id
    recuperado.iniciar(pedido.id)
    assert recuperado.pedidos[0].tentativas == 2
