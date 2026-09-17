import tempfile
import unittest
from pathlib import Path

from cerebro.servico import Cerebro


class TestServico(unittest.TestCase):
    def test_fachada_executa_fluxo_basico(self):
        with tempfile.TemporaryDirectory() as tmp:
            arquivo = Path(tmp) / "fonte.txt"
            arquivo.write_text("Memória temporal do projeto", encoding="utf-8")
            cerebro = Cerebro(Path(tmp) / "data")
            registro = cerebro.ingerir(arquivo)
            self.assertEqual(registro.kind, "DOCUMENTO")
            resultados = cerebro.buscar("memória temporal")
            self.assertEqual(resultados[0].registro.id, registro.id)
            diagnostico = cerebro.diagnostico()
            self.assertEqual(diagnostico["registros"], 1)
            self.assertEqual(diagnostico["fontes"], 1)


if __name__ == "__main__":
    unittest.main()
