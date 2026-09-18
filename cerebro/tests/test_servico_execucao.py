from pathlib import Path

from cerebro.orquestrador import Missao
from cerebro.servico import Cerebro


def test_cerebro_expoe_missao_e_runtime(tmp_path: Path) -> None:
    cerebro = Cerebro(tmp_path / "data")
    cerebro.registrar_missao(Missao("M-1", "Executar um ciclo"))

    resultado = cerebro.executar_missao(
        "M-1",
        lambda _: [("caminho-a", 1.0)],
        lambda _, caminho: {"caminho": caminho},
    )

    assert resultado["executado"] is True
    diagnostico = cerebro.diagnostico()
    assert diagnostico["missoes"] == 1
    assert diagnostico["ciclos"] == 1
    assert diagnostico["runtime"] == "AGUARDANDO_PROXIMO_CICLO"
