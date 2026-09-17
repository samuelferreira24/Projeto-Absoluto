from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


class ModeloEstruturado(Protocol):
    """Contrato mínimo para qualquer provedor de IA estruturada."""

    nome: str

    def gerar(self, tarefa: str, entrada: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
        ...


@dataclass
class ResultadoModelo:
    modelo: str
    papel: str
    saida: dict[str, Any]
    confianca: str = "DESCONHECIDA"
    observacoes: list[str] = field(default_factory=list)


@dataclass
class OrquestradorModelos:
    """Orquestra modelos substituíveis sem acoplar o Cérebro a um fornecedor."""

    modelos: dict[str, ModeloEstruturado] = field(default_factory=dict)

    def registrar(self, papel: str, modelo: ModeloEstruturado) -> None:
        self.modelos[papel] = modelo

    def executar(self, papel: str, tarefa: str, entrada: dict[str, Any], schema: dict[str, Any]) -> ResultadoModelo:
        if papel not in self.modelos:
            raise LookupError(f"Nenhum modelo registrado para o papel: {papel}")
        modelo = self.modelos[papel]
        saida = modelo.gerar(tarefa, entrada, schema)
        if not isinstance(saida, dict):
            raise TypeError("Modelo deve retornar um objeto estruturado")
        return ResultadoModelo(modelo=modelo.nome, papel=papel, saida=saida)

    def executar_consenso(
        self,
        papel: str,
        tarefa: str,
        entrada: dict[str, Any],
        schema: dict[str, Any],
        modelos: list[ModeloEstruturado],
    ) -> list[ResultadoModelo]:
        resultados: list[ResultadoModelo] = []
        for modelo in modelos:
            modelo_anterior = self.modelos.get(papel)
            self.modelos[papel] = modelo
            try:
                resultados.append(self.executar(papel, tarefa, entrada, schema))
            finally:
                if modelo_anterior is None:
                    self.modelos.pop(papel, None)
                else:
                    self.modelos[papel] = modelo_anterior
        return resultados
