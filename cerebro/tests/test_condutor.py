from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from cerebro.ciclo_operacional import ResultadoOperacional
from cerebro.condutor import (
    CondutorCerebro,
    capacidade_buscar,
    capacidade_ingerir_arquivo,
    capacidade_obter_arquivo,
)
from cerebro.modelos import OrquestradorModelos
from cerebro.orquestrador import Missao
from cerebro.servico import Cerebro


class ModeloSequencial:
    nome = "modelo-teste"

    def __init__(self):
        self.chamadas = 0

    def gerar(self, tarefa, entrada, schema):
        self.chamadas += 1
        if self.chamadas == 1:
            return {
                "executar": True,
                "ferramenta": "obter",
                "argumentos": {"caminho": "pesquisa.docx"},
                "motivo": "obter fonte",
            }
        if self.chamadas == 2:
            path = entrada["contexto"]["ultimo_resultado"]["dados"]["path"]
            return {
                "executar": True,
                "ferramenta": "ingerir",
                "argumentos": {"path": path},
                "motivo": "ingerir fonte",
            }
        if self.chamadas == 3:
            return {
                "executar": True,
                "ferramenta": "buscar",
                "argumentos": {"consulta": "representação armazenamento informação"},
                "motivo": "recuperar conhecimento",
            }
        return {"executar": False, "concluida": True, "motivo": "objetivo atingido"}


def _docx_bytes(texto: str) -> bytes:
    xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        "<w:body><w:p><w:r><w:t>"
        + texto
        + "</w:t></w:r></w:p></w:body></w:document>"
    )
    from io import BytesIO
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as z:
        z.writestr("word/document.xml", xml)
    return buffer.getvalue()


def test_ciclo_realista_github_documento_memoria_e_recuperacao(tmp_path):
    cerebro = Cerebro(tmp_path / "data")
    cerebro.registrar_missao(Missao("M1", "encontrar e utilizar pesquisa sobre representação"))

    fonte = _docx_bytes(
        "Pesquisa sobre representação, armazenamento e informação em sistemas de IA."
    )
    chamadas = []

    def github(caminho):
        chamadas.append(caminho)
        return fonte

    modelo = ModeloSequencial()
    modelos = OrquestradorModelos({"decisor": modelo})
    condutor = CondutorCerebro(cerebro, modelos)
    condutor.registrar_capacidade(
        "obter",
        capacidade_obter_arquivo("pesquisa.docx", github, tmp_path / "fontes", fonte="github"),
        descricao="obtém bytes de uma fonte externa",
    )
    condutor.registrar_capacidade(
        "ingerir",
        capacidade_ingerir_arquivo(cerebro),
        descricao="ingere arquivo preservando origem",
    )
    condutor.registrar_capacidade(
        "buscar",
        capacidade_buscar(cerebro),
        descricao="recupera informação do Cérebro",
    )

    historico = condutor.executar_objetivo("M1", limite_ciclos=5)

    assert len(chamadas) == 1
    assert chamadas == ["pesquisa.docx"]
    assert cerebro.orquestrador.missoes["M1"].estado == "CONCLUIDA"
    assert any(r.kind == "DOCUMENTO" for r in cerebro.registros())
    assert any(r.kind == "EXPERIENCIA" for r in cerebro.registros())
    assert any("representação" in r.content.lower() for r in cerebro.registros() if r.kind == "DOCUMENTO")
    assert len(historico) == 4


def test_capacidade_obter_preserva_hash(tmp_path):
    dados = b"arquivo de teste"
    capacidade = capacidade_obter_arquivo(
        "x.docx",
        lambda caminho: dados,
        tmp_path,
        fonte="github",
    )
    resultado = capacidade({"caminho": "x.docx"}, Missao("M", "obter"))
    assert resultado.sucesso is True
    assert resultado.dados["sha256"]
    assert Path(resultado.dados["path"]).read_bytes() == dados
