from __future__ import annotations

from pathlib import Path
from typing import Any

from .auditoria import ResultadoAuditoria, auditar_semantica
from .estado import EstadoSistema
from .ingestao import DocumentoEstruturado, extrair, registrar_fonte
from .nucleo import Registro, RepositorioJSONL
from .recuperacao import ResultadoBusca, buscar_hibrido, expandir_relacoes
from .rastreabilidade import ElementoConstrucao, MapaConstrucao, RelacaoConstrucao
from .rede_evolutiva import ArestaRede, NoRede, RedeEvolutiva
from .semantica import RelacaoSemantica, UnidadeSemantica


class Cerebro:
    """Fachada operacional do Cérebro, mantendo as camadas internas substituíveis."""

    def __init__(self, dados: str | Path = "cerebro/data") -> None:
        self.repo = RepositorioJSONL(dados)
        self.estado_path = self.repo.root / "estado.json"
        self.estado = EstadoSistema()
        if self.estado_path.exists():
            self.estado = EstadoSistema.carregar(self.estado_path)
        self.mapa = MapaConstrucao()
        self.rede = RedeEvolutiva()

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

    def adicionar_elemento_construcao(self, elemento: ElementoConstrucao) -> None:
        self.mapa.adicionar(elemento)

    def adicionar_relacao_construcao(self, relacao: RelacaoConstrucao) -> None:
        self.mapa.relacionar(relacao)

    def validar_construcao(self) -> list[str]:
        return self.mapa.validar()

    def adicionar_no_rede(self, no: NoRede) -> None:
        self.rede.adicionar_no(no)

    def adicionar_nos_rede(self, nos: list[NoRede]) -> None:
        self.rede.adicionar_nos(nos)

    def conectar_rede(self, aresta: ArestaRede) -> None:
        self.rede.conectar(aresta)

    def relacionados_rede(self, no_id: str) -> list[str]:
        return self.rede.relacionados(no_id)

    def candidatos_rede(self, contexto: dict[str, float] | None = None) -> list[tuple[str, float]]:
        """Fornece sinais contextuais; não cria uma ordem fixa de execução."""
        return self.rede.candidatos_contextuais(contexto)

    def pontos_de_alavancagem(self, limite: int = 10) -> list[tuple[str, float]]:
        return self.rede.pontos_de_alavancagem(limite)

    def validar_rede(self) -> list[str]:
        return self.rede.validar()

    def salvar_estado(self) -> None:
        self.estado.salvar(self.estado_path)

    def diagnostico(self) -> dict[str, Any]:
        registros = self.registros()
        return {
            "registros": len(registros),
            "fontes": sum(1 for r in registros if r.kind == "DOCUMENTO"),
            "tipos": {kind: sum(1 for r in registros if r.kind == kind) for kind in sorted({r.kind for r in registros})},
            "estado": self.estado.status,
            "arquitetura": self.estado.architecture_version,
            "elementos_construcao": len(self.mapa.elementos),
            "relacoes_construcao": len(self.mapa.relacoes),
            "integridade_construcao": self.validar_construcao(),
            "nos_rede": len(self.rede.nos),
            "arestas_rede": len(self.rede.arestas),
            "integridade_rede": self.validar_rede(),
        }
