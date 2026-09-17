import unittest

from cerebro.semantica import RelacaoSemantica, UnidadeSemantica
from cerebro.temporal import IntervaloTemporal, relacoes_validas_em, unidades_validas_em, valido_em


class TestTemporal(unittest.TestCase):
    def test_intervalo_e_ponto_no_tempo(self):
        intervalo = IntervaloTemporal(
            valid_from="2026-01-01T00:00:00+00:00",
            valid_until="2026-12-31T23:59:59+00:00",
            recorded_at="2026-02-01T00:00:00+00:00",
        )
        self.assertTrue(valido_em(intervalo, "2026-06-01T00:00:00+00:00"))
        self.assertFalse(valido_em(intervalo, "2027-01-01T00:00:00+00:00"))

    def test_unidade_preserva_tempo_do_fato_e_do_registro(self):
        unidade = UnidadeSemantica(
            id="F-1", source_id="DOC-1", kind="FATO", content="Fato temporal",
            provenance={"origem": "fonte"},
            metadata={"temporal": {
                "valid_from": "2025-01-01T00:00:00+00:00",
                "valid_until": "2025-06-30T23:59:59+00:00",
                "recorded_at": "2025-07-01T00:00:00+00:00",
            }},
        )
        self.assertEqual(len(unidades_validas_em([unidade], "2025-03-01T00:00:00+00:00")), 1)
        self.assertEqual(len(unidades_validas_em([unidade], "2025-08-01T00:00:00+00:00")), 0)

    def test_relacao_temporal(self):
        relacao = RelacaoSemantica(
            source_id="F-1", relation="SUSTENTA", target_id="H-1",
            provenance={"processo": "manual", "temporal": {
                "valid_from": "2026-01-01T00:00:00+00:00",
                "recorded_at": "2026-01-02T00:00:00+00:00",
            }},
        )
        self.assertEqual(len(relacoes_validas_em([relacao], "2026-05-01T00:00:00+00:00")), 1)

    def test_intervalo_inconsistente_e_rejeitado(self):
        with self.assertRaises(ValueError):
            IntervaloTemporal(
                valid_from="2026-05-01T00:00:00+00:00",
                valid_until="2026-04-01T00:00:00+00:00",
            )


if __name__ == "__main__":
    unittest.main()
