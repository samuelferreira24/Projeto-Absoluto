from cerebro.ciclo_operacional import CicloOperacional, DecisaoOperacional, ResultadoOperacional
from cerebro.orquestrador import Missao, Orquestrador


class DecisorTeste:
    def __init__(self):
        self.chamadas = 0

    def decidir(self, missao):
        self.chamadas += 1
        if self.chamadas >= 3:
            return DecisaoOperacional(
                executar=False, concluida=True, motivo="objetivo atingido"
            )
        return DecisaoOperacional(
            executar=True,
            acao=f"etapa-{self.chamadas}",
            ferramenta="capacidade-teste",
            motivo="continuar objetivo",
        )


class ExecutorTeste:
    def __init__(self):
        self.chamadas = 0

    def executar(self, missao, decisao):
        self.chamadas += 1
        return ResultadoOperacional(
            sucesso=True,
            observacao=f"resultado-{self.chamadas}",
            dados={"passo": self.chamadas},
            aprendizado=f"aprendizado-{self.chamadas}",
        )


def test_ciclo_operacional_fecha_e_reutiliza_estado(tmp_path):
    orquestrador = Orquestrador(tmp_path / "orquestrador.json")
    missao = Missao(id="M1", objetivo="alcançar objetivo")
    orquestrador.registrar_missao(missao)

    decisor = DecisorTeste()
    executor = ExecutorTeste()
    historico = CicloOperacional(orquestrador).executar(
        "M1", decisor, executor, limite_ciclos=5
    )

    assert len(historico) == 3
    assert executor.chamadas == 2
    assert decisor.chamadas == 3
    assert orquestrador.missoes["M1"].estado == "CONCLUIDA"
    assert orquestrador.missoes["M1"].contexto["ultimo_aprendizado"] == "aprendizado-2"


def test_falha_nao_apaga_estado_e_permite_decisao_de_fallback(tmp_path):
    class ExecutorComFalha(ExecutorTeste):
        def executar(self, missao, decisao):
            self.chamadas += 1
            if self.chamadas == 1:
                return ResultadoOperacional(
                    sucesso=False,
                    observacao="fonte indisponível",
                    aprendizado="usar fallback",
                )
            return ResultadoOperacional(sucesso=True, observacao="fallback funcionou")

    class DecisorFallback(DecisorTeste):
        def decidir(self, missao):
            self.chamadas += 1
            if self.chamadas == 1:
                return DecisaoOperacional(executar=True, acao="buscar-fonte")
            if self.chamadas == 2:
                return DecisaoOperacional(executar=True, acao="usar-fallback")
            return DecisaoOperacional(executar=False, concluida=True, motivo="concluído")

    orquestrador = Orquestrador(tmp_path / "orquestrador.json")
    orquestrador.registrar_missao(Missao(id="M2", objetivo="obter informação"))
    historico = CicloOperacional(orquestrador).executar(
        "M2", DecisorFallback(), ExecutorComFalha(), limite_ciclos=4
    )

    assert len(historico) == 3
    assert orquestrador.missoes["M2"].estado == "CONCLUIDA"
    assert any(
        item["resultado"]["sucesso"] is False
        for item in historico
        if "resultado" in item
    )
