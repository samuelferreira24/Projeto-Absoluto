from cerebro.sinergia import DetectorSinergia, ResultadoCombinacao


def test_detecta_ganho_de_combinacao():
    detector = DetectorSinergia()
    detector.registrar(ResultadoCombinacao("a", ("A",), 10, 1, 1, 0.8))
    detector.registrar(ResultadoCombinacao("b", ("B",), 8, 1, 1, 0.8))
    detector.registrar(ResultadoCombinacao("ab1", ("A", "B"), 25, 2, 1, 0.9))
    detector.registrar(ResultadoCombinacao("ab2", ("B", "A"), 24, 2, 1, 0.9))

    sinais = detector.detectar()
    assert sinais[0].capacidades == ("A", "B")
    assert sinais[0].ganho_relativo > 1.0
    assert sinais[0].evidencias == 2


def test_gera_combinacoes_ainda_nao_testadas():
    detector = DetectorSinergia()
    detector.registrar(ResultadoCombinacao("ab", ("A", "B"), 10, 1, 1, 0.5))

    candidatos = detector.combinações_promissoras(["A", "B", "C"])
    assert ("A", "B") not in candidatos
    assert ("A", "C") in candidatos
    assert ("B", "C") in candidatos
