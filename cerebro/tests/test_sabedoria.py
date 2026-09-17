from __future__ import annotations

import pytest

from cerebro.sabedoria import (
    Experiencia,
    LicaoAprendida,
    SabedoriaAplicada,
    validar_experiencias,
    validar_licoes,
    validar_sabedoria,
)


def experiencia_base() -> Experiencia:
    return Experiencia(
        id="EXP-001",
        objetivo="testar uma abordagem",
        contexto={"tipo": "teste"},
        acao="aplicar abordagem",
        resultado="funcionou",
        evidencias=["EVID-001"],
        decisoes=["DEC-001"],
        estado="APRENDIDA",
    )


def licao_base() -> LicaoAprendida:
    return LicaoAprendida(
        id="LIC-001",
        principio="o contexto influencia o resultado",
        recomendacao="verificar o contexto antes de reutilizar a abordagem",
        baseada_em=["EXP-001"],
        contexto_aplicabilidade={"tipo": "teste"},
        evidencias=["EVID-001"],
        estado="VALIDADA",
        confianca="MEDIA",
    )


def sabedoria_base() -> SabedoriaAplicada:
    return SabedoriaAplicada(
        id="SAB-001",
        principio="reutilizar a abordagem somente em contexto compatível",
        quando_aplicar=["contexto equivalente ao validado"],
        quando_evitar=["contexto incompatível"],
        como_adaptar=["reavaliar parâmetros quando houver diferença relevante"],
        baseada_em=["LIC-001"],
        evidencias=["EVID-001"],
        resultados_observados=["funcionou em contexto equivalente"],
        consequencias_conhecidas=["reduz reutilização fora de contexto"],
        limites=["validada apenas para contexto de teste"],
        estado="VALIDADA",
        confianca="MEDIA",
        metadata={"requisitos_contextuais": {"tipo": "teste"}},
    )


def test_experiencia_exige_resultado_quando_aprendida() -> None:
    experiencia = experiencia_base()
    experiencia.resultado = ""
    assert any("resultado" in erro for erro in validar_experiencias([experiencia]))


def test_licao_precisa_de_experiencia_de_origem() -> None:
    licao = licao_base()
    assert validar_licoes([licao], [experiencia_base()]) == []
    assert validar_licoes([licao], [])


def test_sabedoria_validada_precisa_de_evidencia_e_limites() -> None:
    assert validar_sabedoria([sabedoria_base()], [licao_base()]) == []

    sem_limites = sabedoria_base()
    sem_limites.limites = []
    assert validar_sabedoria([sem_limites], [licao_base()])


def test_sabedoria_so_e_aplicavel_em_contexto_compativel() -> None:
    sabedoria = sabedoria_base()
    assert sabedoria.pode_ser_aplicada({"tipo": "teste"}) is True
    assert sabedoria.pode_ser_aplicada({"tipo": "producao"}) is False


def test_sabedoria_nao_pode_ser_validada_sem_evidencia() -> None:
    with pytest.raises(ValueError):
        SabedoriaAplicada(
            id="SAB-002",
            principio="regra sem evidencia",
            quando_aplicar=["qualquer contexto"],
            baseada_em=["LIC-001"],
            estado="VALIDADA",
        )
