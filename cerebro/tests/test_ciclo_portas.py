from pathlib import Path

from cerebro.ciclo_operacional import DecisaoOperacional
from cerebro.executor_portas import ExecutorOperacionalPortas
from cerebro.ativacao_portas import AtivadorPortas
from cerebro.orquestrador import Missao, Orquestrador
from cerebro.portas import Porta, RegistroPortas
from cerebro.servico import Cerebro


class DecisorTeste:
    def __init__(self):
        self.chamadas = 0

    def decidir(self, missao):
        self.chamadas += 1
        if self.chamadas == 1:
            return DecisaoOperacional(
                executar=True,
                acao="somar",
                ferramenta="somar",
                argumentos={"a": 4, "b": 6},
            )
        return DecisaoOperacional(
            executar=False,
            concluida=True,
            motivo="objetivo concluído",
        )


def test_executor_operacional_resolve_porta(tmp_path: Path):
    registro = RegistroPortas(tmp_path / "portas.json")
    registro.registrar(
        Porta(
            id="calculadora",
            nome="Calculadora",
            categoria="ferramenta",
            provedor="teste",
            ambiente="teste",
            capacidades=("somar",),
        )
    )
    ativador = AtivadorPortas(registro)
    ativador.ativar("calculadora", "somar", lambda a, b, **_: a + b)

    executor = ExecutorOperacionalPortas(ativador)
    resultado = executor.executar(
        Missao("m1", "somar dois números"),
        DecisaoOperacional(
            executar=True,
            acao="somar",
            ferramenta="somar",
            argumentos={"a": 4, "b": 6},
        ),
    )

    assert resultado.sucesso is True
    assert resultado.dados["resultado"] == 10
    assert resultado.dados["porta_id"] == "calculadora"


def test_ciclo_com_portas_passa_por_decisao_execucao_resultado_e_proximo_ciclo(tmp_path: Path):
    cerebro = Cerebro(tmp_path / "data")
    cerebro.registrar_porta(
        Porta(
            id="calculadora",
            nome="Calculadora",
            categoria="ferramenta",
            provedor="teste",
            ambiente="teste",
            capacidades=("somar",),
        )
    )
    cerebro.ativar_capacidade("calculadora", "somar", lambda a, b, **_: a + b)
    cerebro.registrar_missao(Missao("m1", "somar dois números"))

    historico = cerebro.executar_objetivo_com_portas(
        "m1",
        DecisorTeste(),
        limite_ciclos=3,
    )

    assert len(historico) == 2
    assert historico[0]["resultado"]["sucesso"] is True
    assert historico[1]["concluida"] is True
    assert cerebro.orquestrador.missoes["m1"].estado == "CONCLUIDA"
