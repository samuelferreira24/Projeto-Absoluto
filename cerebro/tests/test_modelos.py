import unittest

from cerebro.modelos import OrquestradorModelos


class ModeloFalso:
    def __init__(self, nome):
        self.nome = nome

    def gerar(self, tarefa, entrada, schema):
        return {"modelo": self.nome, "tarefa": tarefa, "entrada": entrada, "schema": schema}


class TestModelos(unittest.TestCase):
    def test_modelo_e_substituivel(self):
        orq = OrquestradorModelos()
        a = ModeloFalso("A")
        b = ModeloFalso("B")
        orq.registrar("classificador", a)
        self.assertEqual(orq.executar("classificador", "x", {}, {}).modelo, "A")
        orq.registrar("classificador", b)
        self.assertEqual(orq.executar("classificador", "x", {}, {}).modelo, "B")

    def test_consenso_executa_varios_modelos(self):
        orq = OrquestradorModelos()
        resultados = orq.executar_consenso(
            "auditor",
            "verificar",
            {"x": 1},
            {"type": "object"},
            [ModeloFalso("A"), ModeloFalso("B"), ModeloFalso("C")],
        )
        self.assertEqual([r.modelo for r in resultados], ["A", "B", "C"])
        self.assertNotIn("auditor", orq.modelos)


if __name__ == "__main__":
    unittest.main()
