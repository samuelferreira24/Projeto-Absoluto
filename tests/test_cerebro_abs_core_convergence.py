from pathlib import Path

from abs_core.adapters import EchoCapability
from abs_core.capabilities import CapabilityRecord, CapabilityRegistry
from abs_core.store import WorkStore
from cerebro.abs_core_executor import AbsCoreExecutor
from cerebro.orquestrador import Missao, Orquestrador
from cerebro.runtime import RuntimeContinuo


def test_cerebro_abs_core_echo_convergencia(tmp_path: Path) -> None:
    cerebro = Orquestrador(tmp_path / "cerebro.json")
    cerebro.registrar_missao(Missao("M-ABS-ECHO", "Responda pelo ABS Core"))

    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("echo", "Echo", "test", EchoCapability()))
    store = WorkStore(tmp_path / "abs.db")
    executor = AbsCoreExecutor(registry, store, "echo")
    runtime = RuntimeContinuo(
        cerebro,
        path=tmp_path / "runtime.json",
        lease_path=tmp_path / "runtime.lease",
    )

    resultado = runtime.executar_ciclo(
        "M-ABS-ECHO",
        lambda _: [("abs-core-echo", 1.0)],
        executor.executar,
    )

    missao = cerebro.missoes["M-ABS-ECHO"]
    assert resultado["executado"] is True
    assert resultado["caminho"] == "abs-core-echo"
    assert resultado["resultado"]["completed"] is True
    assert resultado["resultado"]["state"] == "completed"
    assert resultado["resultado"]["result"]["type"] == "echo"
    assert resultado["resultado"]["result"]["objective"] == "Responda pelo ABS Core"
    assert missao.resultado["work_id"] == resultado["resultado"]["work_id"]
    assert cerebro.historico[-1].estado == "CONCLUIDO"
    assert runtime.estado.ciclos == 1
    assert runtime.estado.estado == "AGUARDANDO_PROXIMO_CICLO"


def test_cerebro_can_read_back_authoritative_abs_work(tmp_path: Path) -> None:
    cerebro = Orquestrador(tmp_path / "cerebro.json")
    cerebro.registrar_missao(Missao("M-ABS-READ", "Ler estado pelo ABS Core"))

    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("echo", "Echo", "test", EchoCapability()))
    store = WorkStore(tmp_path / "abs.db")
    executor = AbsCoreExecutor(registry, store, "echo")

    resultado = executor.executar(
        cerebro.missoes["M-ABS-READ"],
        "abs-core-readback",
    )
    estado = executor.consultar_work(resultado["work_id"])

    assert estado["work_id"] == resultado["work_id"]
    assert estado["objective"] == "Ler estado pelo ABS Core"
    assert estado["state"] == "completed"
    assert estado["capability_id"] == "echo"
    assert estado["result"]["type"] == "echo"
