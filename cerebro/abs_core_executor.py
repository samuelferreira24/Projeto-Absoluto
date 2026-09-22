from __future__ import annotations

from typing import Any

from abs_core.capabilities import CapabilityRegistry
from abs_core.models import WorkState
from abs_core.orchestrator import Orchestrator as AbsOrchestrator
from abs_core.store import WorkStore

from .orquestrador import Missao


class AbsCoreExecutor:
    """Adaptador mínimo entre uma missão do Cérebro e o ABS Core.

    O Cérebro não conhece o executor concreto. Ele entrega uma missão; o
    ABS Core cria e executa um Work usando a capability selecionada.
    """

    def __init__(
        self,
        registry: CapabilityRegistry,
        store: WorkStore,
        capability_id: str,
        approved: bool = False,
    ) -> None:
        self.orchestrator = AbsOrchestrator(registry, store)
        self.registry = registry
        self.capability_id = capability_id
        self.approved = approved

    def consultar_work(self, work_id: str) -> dict[str, Any]:
        """Read back the authoritative ABS Core state for a Cerebro work."""
        work = self.orchestrator.store.load(work_id)
        return {
            "work_id": work.id,
            "objective": work.objective,
            "state": work.state.value,
            "capability_id": work.capability_id,
            "result": work.result,
            "provenance": work.provenance,
            "events": [event.type for event in work.events],
            "sessions": work.sessions,
        }

    def executar(self, missao: Missao, caminho: Any) -> dict[str, Any]:
        context = {
            **missao.contexto,
            "cerebro_missao_id": missao.id,
            "caminho": caminho,
        }
        work = self.orchestrator.create(missao.objetivo, context)
        concluido = self.orchestrator.run(
            work.id,
            capability_id=self.capability_id,
            approved=self.approved,
        )
        return {
            "mission_id": missao.id,
            "work_id": concluido.id,
            "state": concluido.state.value,
            "result": concluido.result,
            "provenance": concluido.provenance,
            "events": [event.type for event in concluido.events],
            "completed": concluido.state is WorkState.COMPLETED,
        }
