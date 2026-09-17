from datetime import datetime, timedelta, timezone

import pytest

from cerebro.orquestrador import Missao, Orquestrador
from cerebro.runtime import RuntimeContinuo


def futuro(segundos: int = 300) -> str:
    return (datetime.now(timezone.utc) + timedelta(seconds=segundos)).replace(microsecond=0).isoformat()


def passado(segundos: int = 300) -> str:
    return (datetime.now(timezone.utc) - timedelta(seconds=segundos)).replace(microsecond=0).isoformat()


def test_runtime_persiste_ciclo(tmp_path):
    o = Orquestrador(tmp_path / "orq.json")
    o.registrar_missao(Missao("M-1", "continuar"))
    runtime = RuntimeContinuo(o, tmp_path / "runtime.json")
    resultado = runtime.executar_ciclo(
        "M-1",
        lambda _: [("caminho-a", 1.0)],
        lambda _, caminho: {"caminho": caminho},
    )
    assert resultado["executado"] is True
    assert runtime.estado.ciclos == 1
    assert runtime.estado.estado == "AGUARDANDO_PROXIMO_CICLO"
    assert not runtime.lease_path.exists()


def test_runtime_nao_recupera_lease_ainda_valido(tmp_path):
    path = tmp_path / "runtime.json"
    path.write_text(
        '{"estado":"EXECUTANDO","ultimo_ciclo":null,"ciclos":3,"motivo_parada":null,'
        '"runtime_id":"r1","lease_id":"x","lease_expira_em":"' + futuro() + '","heartbeat_em":null}\n',
        encoding="utf-8",
    )
    runtime = RuntimeContinuo(Orquestrador(tmp_path / "orq.json"), path)
    assert runtime.estado.estado == "EXECUTANDO"
    assert runtime.estado.lease_id == "x"


def test_runtime_recupera_lease_expirado(tmp_path):
    path = tmp_path / "runtime.json"
    path.write_text(
        '{"estado":"EXECUTANDO","ultimo_ciclo":null,"ciclos":3,"motivo_parada":null,'
        '"runtime_id":"r1","lease_id":"x","lease_expira_em":"' + passado() + '","heartbeat_em":null}\n',
        encoding="utf-8",
    )
    runtime = RuntimeContinuo(Orquestrador(tmp_path / "orq.json"), path)
    assert runtime.estado.estado == "RECUPERADO"
    assert runtime.estado.ciclos == 3
    assert runtime.estado.lease_id is None


def test_runtime_lease_atomico_impede_concorrencia(tmp_path):
    runtime_a = RuntimeContinuo(Orquestrador(tmp_path / "orq.json"), tmp_path / "runtime.json")
    runtime_b = RuntimeContinuo(Orquestrador(tmp_path / "orq.json"), tmp_path / "runtime.json")
    runtime_a.adquirir_lease("a", futuro())
    try:
        with pytest.raises(RuntimeError, match="lease ativo"):
            runtime_b.adquirir_lease("b", futuro())
    finally:
        runtime_a.liberar_lease("a")


def test_runtime_renova_lease(tmp_path):
    runtime = RuntimeContinuo(Orquestrador(tmp_path / "orq.json"), tmp_path / "runtime.json")
    runtime.adquirir_lease("a", futuro())
    antes = runtime.estado.heartbeat_em
    runtime.renovar_lease("a", futuro(600))
    assert runtime.estado.lease_id == "a"
    assert runtime.estado.heartbeat_em is not None
    assert runtime.estado.heartbeat_em >= antes
    runtime.liberar_lease("a")


def test_runtime_nao_renova_lease_expirado(tmp_path):
    runtime = RuntimeContinuo(Orquestrador(tmp_path / "orq.json"), tmp_path / "runtime.json")
    runtime.adquirir_lease("a", passado())
    with pytest.raises(RuntimeError, match="lease expirado"):
        runtime.renovar_lease("a")
    runtime.estado.lease_id = "a"
    runtime.liberar_lease("a")
