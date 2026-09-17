from cerebro.orquestrador import Missao, Orquestrador
from cerebro.runtime import RuntimeContinuo


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


def test_runtime_recupera_interrupcao(tmp_path):
    path = tmp_path / "runtime.json"
    path.write_text('{"estado":"EXECUTANDO","ultimo_ciclo":null,"ciclos":3,"motivo_parada":null}\n', encoding="utf-8")
    runtime = RuntimeContinuo(Orquestrador(tmp_path / "orq.json"), path)
    assert runtime.estado.estado == "RECUPERADO"
    assert runtime.estado.ciclos == 3
