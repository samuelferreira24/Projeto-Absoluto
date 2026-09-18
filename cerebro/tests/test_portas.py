from pathlib import Path

from cerebro.portas import Porta, RegistroPortas


def test_registra_e_recupera_porta(tmp_path: Path):
    registro = RegistroPortas(tmp_path / "portas.json")
    porta = Porta(
        id="agente.codex",
        nome="Codex",
        categoria="agente_programacao",
        provedor="OpenAI",
        ambiente="desenvolvimento",
        capacidades=("programacao", "testes", "edicao_repositorio"),
        ferramentas=("codex_sdk", "codex_app_server"),
        permissoes=("workspace_write",),
    )

    registro.registrar(porta)

    recuperada = registro.listar()
    assert len(recuperada) == 1
    assert recuperada[0].id == "agente.codex"
    assert recuperada[0].substituivel is True


def test_busca_por_capacidade_e_ambiente(tmp_path: Path):
    registro = RegistroPortas(tmp_path / "portas.json")
    registro.registrar(
        Porta(
            id="modelo.local",
            nome="Modelo local",
            categoria="modelo",
            provedor="local",
            ambiente="computador",
            capacidades=("raciocinio",),
            modo="local",
        )
    )
    registro.registrar(
        Porta(
            id="agente.codex",
            nome="Codex",
            categoria="agente_programacao",
            provedor="OpenAI",
            ambiente="desenvolvimento",
            capacidades=("programacao",),
        )
    )

    assert [p.id for p in registro.por_capacidade("programacao")] == ["agente.codex"]
    assert [p.id for p in registro.por_ambiente("computador")] == ["modelo.local"]
