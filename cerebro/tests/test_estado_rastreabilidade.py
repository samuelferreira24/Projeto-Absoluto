import tempfile
import unittest
from pathlib import Path

from cerebro.estado import EstadoSistema, validar_estado
from cerebro.rastreabilidade import ElementoConstrucao, MapaConstrucao, RelacaoConstrucao


class TestEstado(unittest.TestCase):
    def test_estado_salva_carrega_e_atualiza(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "estado.json"
            estado = EstadoSistema(active_branch="base-cerebro-v0.1")
            estado.salvar(path)
            carregado = EstadoSistema.carregar(path)
            self.assertEqual(carregado.state_id, estado.state_id)
            self.assertEqual(carregado.active_branch, "base-cerebro-v0.1")
            carregado.atualizar(status="OPERACIONAL")
            self.assertEqual(carregado.status, "OPERACIONAL")

    def test_validacao_rejeita_estado_incompleto(self):
        erros = validar_estado({"status": "INVALIDO"})
        self.assertIn("campo obrigatório ausente: project_id", erros)
        self.assertIn("status inválido", erros)


class TestRastreabilidade(unittest.TestCase):
    def test_mapa_relaciona_e_detecta_dependencias(self):
        mapa = MapaConstrucao()
        mapa.adicionar(ElementoConstrucao("OBJ-1", "OBJETIVO", "Objetivo"))
        mapa.adicionar(ElementoConstrucao("CAP-1", "CAPACIDADE", "Capacidade"))
        mapa.relacionar(RelacaoConstrucao("CAP-1", "HABILITA", "OBJ-1"))
        self.assertEqual(mapa.dependencias("OBJ-1"), [])
        self.assertEqual(mapa.validar(), [])

    def test_mapa_rejeita_relacao_para_elemento_inexistente(self):
        mapa = MapaConstrucao()
        mapa.adicionar(ElementoConstrucao("A", "COMPONENTE", "A"))
        with self.assertRaises(KeyError):
            mapa.relacionar(RelacaoConstrucao("A", "AFETA", "B"))


if __name__ == "__main__":
    unittest.main()
