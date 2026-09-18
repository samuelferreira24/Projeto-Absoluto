"""Fontes-base oficiais do conhecimento do Projeto Absoluto.

Este módulo registra as três fontes primárias sem transformar nenhuma delas em
autoridade absoluta. Ele organiza a função de cada fonte e deixa a interpretação
para as camadas semânticas/derivadas do Cérebro.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .ingestao import DocumentoEstruturado, extrair, registrar_fonte
from .nucleo import Registro, RepositorioJSONL


@dataclass(frozen=True)
class FonteBase:
    id: str
    arquivo: str
    funcao: str
    descricao: str
    prioridade: str = "PRIMARIA"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


FONTES_BASE: tuple[FonteBase, ...] = (
    FonteBase(
        id="projeto-absoluto-ebook-humano-v10",
        arquivo="Projeto_Absoluto_EBOOK_HUMANO_V10_ATUALIZADO.docx",
        funcao="VISAO_E_PROJETO",
        descricao="Fonte principal para a visão, propósito, estrutura conceitual e entendimento do Projeto Absoluto pelo lado humano.",
    ),
    FonteBase(
        id="projeto-absoluto-memoria-ia-v10",
        arquivo="Projeto_Absoluto_MEMORIA_IA_V10_ATUALIZADO.docx",
        funcao="MEMORIA_E_CEREBRO",
        descricao="Fonte principal para a concepção de memória, continuidade, conhecimento e papel do Cérebro como infraestrutura cognitiva do projeto.",
    ),
    FonteBase(
        id="pesquisa-representacao-armazenamento-informacao-ia-v1",
        arquivo="Pesquisa_Representacao_Armazenamento_Informacao_IA_Projeto_Absoluto_v1.docx",
        funcao="REPRESENTACAO_E_ARMAZENAMENTO",
        descricao="Fonte de pesquisa para representar, armazenar, relacionar, recuperar e evoluir informação em sistemas de IA.",
    ),
)


def localizar_fontes(raiz_projeto: str | Path) -> list[tuple[FonteBase, Path]]:
    raiz = Path(raiz_projeto)
    return [(fonte, raiz / fonte.arquivo) for fonte in FONTES_BASE]


def auditar_fontes(raiz_projeto: str | Path) -> list[dict[str, Any]]:
    resultado: list[dict[str, Any]] = []
    for fonte, caminho in localizar_fontes(raiz_projeto):
        item: dict[str, Any] = {"fonte": fonte.to_dict(), "caminho": str(caminho), "existe": caminho.is_file()}
        if caminho.is_file():
            documento = extrair(caminho)
            item.update({
                "formato": documento.formato,
                "tamanho": documento.tamanho,
                "sha256": documento.sha256,
                "texto_extraido": bool(documento.texto.strip()),
                "erros": documento.erros,
                "estrutura_itens": len(documento.estrutura),
            })
        resultado.append(item)
    return resultado


def _ja_ingerida(repo: RepositorioJSONL, sha256: str) -> Registro | None:
    for registro in repo._iter_registros():
        if registro.kind == "DOCUMENTO" and registro.provenance.get("sha256") == sha256:
            return registro
    return None


def ingerir_fontes_base(repo: RepositorioJSONL, raiz_projeto: str | Path) -> dict[str, Any]:
    """Ingere as três fontes sem duplicar documentos já registrados por hash."""
    resultados: list[dict[str, Any]] = []
    for fonte, caminho in localizar_fontes(raiz_projeto):
        if not caminho.is_file():
            resultados.append({"id": fonte.id, "status": "AUSENTE", "arquivo": str(caminho)})
            continue

        documento: DocumentoEstruturado = extrair(caminho)
        if documento.erros:
            resultados.append({
                "id": fonte.id,
                "status": "ERRO_EXTRACAO",
                "arquivo": str(caminho),
                "erros": documento.erros,
            })
            continue

        existente = _ja_ingerida(repo, documento.sha256)
        if existente is not None:
            resultados.append({
                "id": fonte.id,
                "status": "JA_INGESTA",
                "registro_id": existente.id,
                "sha256": documento.sha256,
            })
            continue

        registro = registrar_fonte(repo, documento)
        registro.metadata["fonte_base_id"] = fonte.id
        registro.metadata["funcao_fonte_base"] = fonte.funcao
        registro.metadata["prioridade_fonte"] = fonte.prioridade
        registro.provenance["papel_da_fonte"] = fonte.funcao
        registro.provenance["fonte_base"] = True
        repo.atualizar(registro)
        resultados.append({
            "id": fonte.id,
            "status": "INGERIDA",
            "registro_id": registro.id,
            "sha256": documento.sha256,
        })

    return {
        "fontes": [fonte.to_dict() for fonte in FONTES_BASE],
        "resultados": resultados,
        "regra": "fonte original preservada; derivacoes posteriores devem apontar para o documento",
    }
