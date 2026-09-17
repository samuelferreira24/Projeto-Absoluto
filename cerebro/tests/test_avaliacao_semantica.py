import unittest

from cerebro.auditoria import auditar_semantica
from cerebro.semantica import RelacaoSemantica, UnidadeSemantica
from cerebro.temporal import valido_em


class TestAvaliacaoSemantica(unittest.TestCase):
    def test_fato_explicito_preserva_origem(self):
        unidade = UnidadeSemantica(
            id="F-1",
            source_id="DOC-1",
            kind="FATO",
            content="A fonte afirma explicitamente o fato.",
            provenance={"origem": "DOC-1", "processo": "extracao"},
        )
        self.assertEqual(unidade.kind, "FATO")
        self.assertEqual(unidade.provenance["origem"], "DOC-1")
        self.assertEqual(auditar_semantica([unidade]).ok, True)

    def test_hipotese_nao_e_promovida_para_fato(self):
        unidade = UnidadeSemantica(
            id="H-1",
            source_id="DOC-1",
            kind="HIPOTESE",
            content="Pode ser que a causa seja X.",
            provenance={"origem": "DOC-1"},
        )
        self.assertEqual(unidade.kind, "HIPOTESE")
        self.assertNotEqual(unidade.kind, "FATO")

    def test_interpretacao_exige_origem_derivada(self):
        unidade = UnidadeSemantica(
            id="I-1",
            source_id="DOC-1",
            kind="INTERPRETACAO",
            content="Síntese derivada das evidências.",
            derived_from=["F-1", "F-2"],
            provenance={"processo": "analise", "origem": "DOC-1"},
            metadata={"origin": "inferencia"},
        )
        resultado = auditar_semantica([unidade])
        self.assertTrue(resultado.ok)
        self.assertTrue(unidade.is_derived)

    def test_decisao_e_distinta_de_fato(self):
        unidade = UnidadeSemantica(
            id="D-1",
            source_id="DOC-2",
            kind="DECISAO",
            content="O projeto adotará esta abordagem.",
            provenance={"origem": "DECISAO-REGISTRO", "motivo": "trade-off"},
        )
        self.assertEqual(unidade.kind, "DECISAO")
        self.assertNotEqual(unidade.kind, "FATO")

    def test_ambiguidade_pode_ser_mantida_como_outro(self):
        unidade = UnidadeSemantica(
            id="A-1",
            source_id="DOC-3",
            kind="OUTRO",
            content="A afirmação não permite classificação segura.",
            provenance={"origem": "DOC-3", "motivo": "ambiguidade"},
            confidence="DESCONHECIDA",
        )
        self.assertEqual(unidade.kind, "OUTRO")
        self.assertEqual(unidade.confidence, "DESCONHECIDA")
        self.assertTrue(auditar_semantica([unidade]).ok)

    def test_contradicao_preserva_as_duas_unidades(self):
        a = UnidadeSemantica(
            id="F-1", source_id="DOC-A", kind="FATO",
            content="A fonte A afirma X.", provenance={"origem": "DOC-A"}
        )
        b = UnidadeSemantica(
            id="F-2", source_id="DOC-B", kind="FATO",
            content="A fonte B afirma não-X.", provenance={"origem": "DOC-B"}
        )
        relacao = RelacaoSemantica(
            source_id="F-1", relation="CONTRADIZ", target_id="F-2",
            provenance={"processo": "analise_contradicao"}
        )
        resultado = auditar_semantica([a, b], [relacao])
        self.assertTrue(resultado.ok)
        self.assertEqual({u.id for u in [a, b]}, {"F-1", "F-2"})
        self.assertEqual(relacao.relation, "CONTRADIZ")

    def test_tempo_do_fato_e_tempo_do_registro_sao_distintos(self):
        unidade = UnidadeSemantica(
            id="F-T",
            source_id="DOC-T",
            kind="FATO",
            content="O fato era válido em janeiro.",
            provenance={"origem": "DOC-T"},
            metadata={
                "temporal": {
                    "valid_from": "2026-01-01T00:00:00+00:00",
                    "valid_until": "2026-01-31T23:59:59+00:00",
                    "recorded_at": "2026-03-01T00:00:00+00:00",
                }
            },
        )
        self.assertTrue(valido_em(unidade, "2026-01-15T00:00:00+00:00"))
        self.assertFalse(valido_em(unidade, "2026-02-15T00:00:00+00:00"))
        temporal = unidade.metadata["temporal"]
        self.assertNotEqual(temporal["valid_from"], temporal["recorded_at"])

    def test_referencia_externa_e_aceita(self):
        unidade = UnidadeSemantica(
            id="I-EXT",
            source_id="DOC-LOCAL",
            kind="INTERPRETACAO",
            content="Interpretação baseada em fonte externa.",
            derived_from=["EXTERNO-99"],
            provenance={"origem": "DOC-LOCAL", "processo": "analise"},
            metadata={"origin": "inferencia"},
        )
        resultado = auditar_semantica([unidade])
        self.assertTrue(resultado.ok)


if __name__ == "__main__":
    unittest.main()
