from pathlib import Path

from cerebro.ativacao_portas import AtivadorPortas
from cerebro.portas import Porta, RegistroPortas


def test_ativa_e_executa_capacidade(tmp_path: Path):
    registro = RegistroPortas(tmp_path / "portas.json")
    registro.registrar(
        Porta(
            id="ferramenta.teste",
            nome="Ferramenta de teste",
            categoria="ferramenta",
            provedor="interno",
            ambiente="teste",
            capacidades=("somar",),
        )
    )

    ativador = AtivadorPortas(registro)
    ativador.ativar("ferramenta.teste", "somar", lambda a, b: a + b)

    assert ativador.disponivel("somar") is True
    resultado = ativador.executar("somar", 2, 3)

    assert resultado.sucesso is True
    assert resultado.resultado == 5
    assert resultado.porta_id == "ferramenta.teste"


def test_nao_executa_porta_sem_handler(tmp_path: Path):
    registro = RegistroPortas(tmp_path / "portas.json")
    registro.registrar(
        Porta(
            id="ferramenta.teste",
            nome="Ferramenta de teste",
            categoria="ferramenta",
            provedor="interno",
            ambiente="teste",
            capacidades=("somar",),
        )
    )

    ativador = AtivadorPortas(registro)

    assert ativador.disponivel("somar") is False
