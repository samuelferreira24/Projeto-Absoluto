from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class EstadoTarefa(str, Enum):
    PENDENTE = "PENDENTE"
    PRONTA = "PRONTA"
    EXECUTANDO = "EXECUTANDO"
    CONCLUIDA = "CONCLUIDA"
    BLOQUEADA = "BLOQUEADA"
    FALHOU = "FALHOU"
    CANCELADA = "CANCELADA"


@dataclass(frozen=True)
class NoTarefa:
    id: str
    objetivo: str
    depende_de: tuple[str, ...] = ()
    recursos: tuple[str, ...] = ()
    capacidades: tuple[str, ...] = ()
    estado: EstadoTarefa = EstadoTarefa.PENDENTE
    prioridade: float = 0.0
    valor_estimado: float = 0.0
    custo_estimado: float = 0.0
    tempo_estimado: float = 0.0
    risco: float = 0.0
    prazo: float | None = None
    preferencias: tuple[str, ...] = ()
    restricoes: tuple[str, ...] = ()
    oportunidade: float = 0.0
    incerteza: float = 0.0
    comunicacao_estimado: float = 0.0
    fallbacks: tuple[str, ...] = ()
    combustivel_estimado: float = 0.0
    prazo_critico: bool = False
    nivel_autonomia: int = 2
    reversivel: bool = True
    exige_aprovacao: bool = False
    ferramenta: str | None = None


@dataclass
class GrafoTarefas:
    tarefas: dict[str, NoTarefa] = field(default_factory=dict)

    def adicionar(self, tarefa: NoTarefa) -> None:
        if tarefa.id in self.tarefas:
            raise ValueError(f"Tarefa já existente: {tarefa.id}")
        self.tarefas[tarefa.id] = tarefa

    def adicionar_varias(self, tarefas: Iterable[NoTarefa]) -> None:
        for tarefa in tarefas:
            self.adicionar(tarefa)

    def validar(self) -> list[str]:
        erros: list[str] = []
        for tarefa in self.tarefas.values():
            for dependencia in tarefa.depende_de:
                if dependencia not in self.tarefas:
                    erros.append(f"{tarefa.id}: dependência inexistente: {dependencia}")
            for fallback in tarefa.fallbacks:
                if fallback not in self.tarefas:
                    erros.append(f"{tarefa.id}: fallback inexistente: {fallback}")
        if self._tem_ciclo():
            erros.append("grafo contém ciclo de dependências")
        return erros

    def prontas(self, recursos_disponiveis: set[str] | None = None) -> list[NoTarefa]:
        # None significa que o scheduler não impôs filtro de disponibilidade.
        # Um conjunto vazio, quando fornecido explicitamente, significa que nenhum
        # recurso externo está disponível. Essa distinção evita bloquear tarefas
        # autossuficientes quando o chamador não fornece um inventário de recursos.
        recursos = recursos_disponiveis
        resultado: list[NoTarefa] = []
        for tarefa in self.tarefas.values():
            if tarefa.estado != EstadoTarefa.PENDENTE:
                continue
            if any(dependencia not in self.tarefas for dependencia in tarefa.depende_de):
                continue
            if any(self.tarefas[d].estado != EstadoTarefa.CONCLUIDA for d in tarefa.depende_de):
                continue
            if tarefa.recursos and not set(tarefa.recursos).issubset(recursos):
                continue
            resultado.append(tarefa)
        return sorted(resultado, key=lambda t: (-t.prioridade, t.id))

    def lotes_paralelos(self, recursos_disponiveis: set[str] | None = None) -> list[list[NoTarefa]]:
        lote: list[NoTarefa] = []
        usados: set[str] = set()
        for tarefa in self.prontas(recursos_disponiveis):
            recursos = set(tarefa.recursos)
            if recursos & usados:
                continue
            lote.append(tarefa)
            usados.update(recursos)
        return [lote] if lote else []

    def marcar(self, tarefa_id: str, estado: EstadoTarefa) -> None:
        tarefa = self.tarefas[tarefa_id]
        self.tarefas[tarefa_id] = NoTarefa(
            id=tarefa.id, objetivo=tarefa.objetivo, depende_de=tarefa.depende_de,
            recursos=tarefa.recursos, capacidades=tarefa.capacidades, estado=estado,
            prioridade=tarefa.prioridade, valor_estimado=tarefa.valor_estimado,
            custo_estimado=tarefa.custo_estimado, tempo_estimado=tarefa.tempo_estimado,
            risco=tarefa.risco, prazo=tarefa.prazo, preferencias=tarefa.preferencias,
            restricoes=tarefa.restricoes, oportunidade=tarefa.oportunidade,
            incerteza=tarefa.incerteza, comunicacao_estimado=tarefa.comunicacao_estimado,
            fallbacks=tarefa.fallbacks, combustivel_estimado=tarefa.combustivel_estimado,
            prazo_critico=tarefa.prazo_critico, nivel_autonomia=tarefa.nivel_autonomia,
            reversivel=tarefa.reversivel, exige_aprovacao=tarefa.exige_aprovacao,
            ferramenta=tarefa.ferramenta,
        )

    def dependentes_de(self, tarefa_id: str) -> list[NoTarefa]:
        return sorted(
            (t for t in self.tarefas.values() if tarefa_id in t.depende_de),
            key=lambda t: (-t.prioridade, t.id),
        )

    def cancelar_dependentes(self, tarefa_id: str) -> list[str]:
        canceladas: list[str] = []
        for tarefa in self.dependentes_de(tarefa_id):
            if tarefa.estado in {EstadoTarefa.PENDENTE, EstadoTarefa.PRONTA}:
                self.marcar(tarefa.id, EstadoTarefa.CANCELADA)
                canceladas.append(tarefa.id)
                canceladas.extend(self.cancelar_dependentes(tarefa.id))
        return canceladas

    def _tem_ciclo(self) -> bool:
        visitados: set[str] = set()
        caminho: set[str] = set()

        def visitar(no_id: str) -> bool:
            if no_id in caminho:
                return True
            if no_id in visitados:
                return False
            visitados.add(no_id)
            caminho.add(no_id)
            for dep in self.tarefas[no_id].depende_de:
                if dep in self.tarefas and visitar(dep):
                    return True
            caminho.remove(no_id)
            return False

        return any(visitar(no_id) for no_id in self.tarefas)
