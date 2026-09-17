from __future__ import annotations

from pathlib import Path
from typing import Any

from .auditoria import ResultadoAuditoria, auditar_semantica
from .ingestao import DocumentoEstruturado, extrair, registrar_fonte
from .nucleo import Registro, RepositorioJSONL
from .recuperacao import ResultadoBusca, buscar_hibrido, expandir_relacoes
from .semantica import RelacaoSemantica, UnidadeSemantica


class Cerebro:
    """Fachada operacional do Cérebro, mantendo as camadas internas substituíveis."""

    def __init__(self, dados: str | Path = "cerebro/data") -> None:
        self.repo = RepositorioJSONL(dados)

    def inspecionar(self, arquivo: str | Path) -> DocumentoEstruturado:
        return extrair(arquivo)

    def ingerir(self, arquivo: str | Path) -> Registro:
        documento = self.inspecionar(arquivo)
        if documento.erros:
            raise ValueError(f"Falha na ingestão: {documento.erros}")
        return registrar_fonte(self.repo, documento)

    def registros(self) -> list[Registro]:
        return list(self.repo._iter_registros())

    def buscar(self, consulta: str, limite: int = 10) -> list[ResultadoBusca]:
        return buscar_hibrido(self.registros(), consulta, limite)

    def relacionados(self, ids: list[str], profundidade: int = 1) -> list[Registro]:
        return expandir_relacoes(self.registros(), ids, profundidade)

    def auditar(
        self,
        unidades: list[UnidadeSemantica],
        relacoes: list[RelacaoSemantica] | None = None,
    ) -> ResultadoAuditoria:
        return auditar_semantica(unidades, relacoes)

    def diagnostico(self) -> dict[str, Any]:
        registros = self.registros()
        return {
            "registros": len(registros),
            "fontes": sum(1 for r in registros if r.kind == "DOCUMENTO"),
            "tipos": {kind: sum(1 for r in registros if r.kind == kind) for kind in sorted({r.kind for r in registros})},
        }
