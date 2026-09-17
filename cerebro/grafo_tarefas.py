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
        if self._tem_ciclo():
            erros.append("grafo contém ciclo de dependências")
        return erros

    def prontas(self, recursos_disponiveis: set[str] | None = None) -> list[NoTarefa]:
        recursos = recursos_disponiveis if recursos_disponiveis is not None else set()
        resultado: list[NoTarefa] = []
        for tarefa in self.tarefas.values():
            if tarefa.estado != EstadoTarefa.PENDENTE:
                continue
            dependencias = [self.tarefas[d] for d in tarefa.depende_de if d in self.tarefas]
            if any(d.estado != EstadoTarefa.CONCLUIDA for d in dependencias):
                continue
            if tarefa.recursos and not set(tarefa.recursos).issubset(recursos):
                continue
            resultado.append(tarefa)
        return sorted(resultado, key=lambda t: (-t.prioridade, t.id))

    def lotes_paralelos(self, recursos_disponiveis: set[str] | None = None) -> list[list[NoTarefa]]:
        """Forma um lote máximo simples sem compartilhar o mesmo recurso."""
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
            id=tarefa.id,
            objetivo=tarefa.objetivo,
            depende_de=tarefa.depende_de,
            recursos=tarefa.recursos,
            capacidades=tarefa.capacidades,
            estado=estado,
            prioridade=tarefa.prioridade,
            valor_estimado=tarefa.valor_estimado,
            custo_estimado=tarefa.custo_estimado,
            tempo_estimado=tarefa.tempo_estimado,
            risco=tarefa.risco,
            prazo=tarefa.prazo,
            preferencias=tarefa.preferencias,
        )

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
