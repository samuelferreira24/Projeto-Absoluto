from __future__ import annotations

import sys

from cerebro.politica_execucao import Acao, EscopoExecucao, NivelAutonomia, PoliticaExecucao


def test_escopo_bloqueia_por_padrao():
    politica = PoliticaExecucao(NivelAutonomia.DELEGAR)
    acao = Acao("executor", NivelAutonomia.DELEGAR, reversivel=False)

    permitido, motivo = politica.validar_executor_externo(acao, [sys.executable])

    assert permitido is False
    assert "escopo" in motivo


def test_escopo_permite_executavel_explicitamente_autorizado():
    politica = PoliticaExecucao(
        NivelAutonomia.DELEGAR,
        escopo=EscopoExecucao(executaveis_permitidos=(sys.executable,)),
    )
    acao = Acao("executor", NivelAutonomia.DELEGAR, reversivel=False)

    permitido, motivo = politica.validar_executor_externo(acao, [sys.executable, "-c", "print(1)"])

    assert permitido is True
    assert motivo == "OK"


def test_escopo_rejeita_executavel_nao_autorizado():
    politica = PoliticaExecucao(
        NivelAutonomia.DELEGAR,
        escopo=EscopoExecucao(executaveis_permitidos=("outro-programa",)),
    )
    acao = Acao("executor", NivelAutonomia.DELEGAR, reversivel=False)

    permitido, motivo = politica.validar_executor_externo(acao, [sys.executable])

    assert permitido is False
    assert "não permitido" in motivo
