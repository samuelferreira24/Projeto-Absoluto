from __future__ import annotations

"""ABS V3 Operational Intelligence.

This layer is deliberately not a model. It is the replaceable cognitive
control layer that turns an Imperator objective into an executable strategy.
Models provide reasoning; ABS retains authority over admissibility, execution,
verification and recovery.
"""

import json
import re
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class OperationalStep:
    objective: str
    capability_id: str | None = None
    executor: str | None = None
    required_capabilities: tuple[str, ...] = ()
    priority: str = "normal"
    context: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class OperationalPlan:
    objective: str
    understanding: str
    mode: str
    steps: tuple[OperationalStep, ...]
    success_criteria: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()
    source: str = "model"
    intelligence_id: str | None = None

    def public(self) -> dict[str, Any]:
        return {
            "objective": self.objective,
            "understanding": self.understanding,
            "mode": self.mode,
            "steps": [
                {
                    "objective": s.objective,
                    "capability_id": s.capability_id,
                    "executor": s.executor,
                    "required_capabilities": list(s.required_capabilities),
                    "priority": s.priority,
                    "context": dict(s.context),
                }
                for s in self.steps
            ],
            "success_criteria": list(self.success_criteria),
            "assumptions": list(self.assumptions),
            "unknowns": list(self.unknowns),
            "source": self.source,
            "intelligence_id": self.intelligence_id,
        }


class OperationalIntelligence:
    """Objective interpreter, strategist and delegation layer."""

    MODES = {"direct", "workflow", "agent", "multiagent"}

    def __init__(self, registry, selector, cost_policy, *, state_store=None):
        self.registry = registry
        self.selector = selector
        self.cost_policy = cost_policy
        self.state_store = state_store

    def _available_capabilities(self) -> list[dict[str, Any]]:
        return [
            {
                "id": c.id,
                "name": c.name,
                "kind": c.kind,
                "metadata": dict(getattr(c, "metadata", {}) or {}),
            }
            for c in self.registry.list()
        ]

    def _candidate_prompt(self, objective: str, context: dict[str, Any]) -> str:
        capabilities = self._available_capabilities()
        return (
            "You are the planning intelligence inside ABS. You are NOT the authority. "
            "Return ONLY valid JSON, no markdown. Interpret the Imperator objective and "
            "produce the smallest sufficient executable strategy. Never invent capability "
            "IDs: use only IDs in AVAILABLE_CAPABILITIES. Use mode direct for one direct "
            "operation, workflow for ordered steps, agent when autonomous tool use is "
            "needed, and multiagent only when genuinely parallel independent work is "
            "useful. State unknowns explicitly. Do not claim completion.\n\n"
            f"OBJECTIVE:\n{objective}\n\n"
            f"CONTEXT:\n{json.dumps(context, ensure_ascii=False, default=str)}\n\n"
            f"AVAILABLE_CAPABILITIES:\n{json.dumps(capabilities, ensure_ascii=False, default=str)}\n\n"
            'JSON schema: {"understanding":"...", "mode":"direct|workflow|agent|multiagent", '
            '"steps":[{"objective":"...","capability_id":"...","executor":"direct|workflow|agent|multiagent",'
            '"required_capabilities":["..."],"priority":"normal|high|critical","context":{}}],'
            '"success_criteria":["..."],"assumptions":["..."],"unknowns":["..."]}'
        )

    def _extract_json(self, value: Any) -> dict[str, Any]:
        text = value
        if isinstance(value, dict):
            text = value.get("final_response", value.get("response", value))
        if isinstance(text, dict):
            return text
        text = str(text or "").strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", text, re.S)
            if not match:
                raise ValueError("operational_intelligence_invalid_plan")
            return json.loads(match.group(0))

    def _fallback(self, objective: str, context: dict[str, Any]) -> OperationalPlan:
        capability = context.get("capability_id")
        if capability:
            try:
                self.registry.get(str(capability))
            except KeyError:
                capability = None
        if not capability:
            # Safe fallback: no invented executor/capability.
            return OperationalPlan(
                objective=objective,
                understanding=objective,
                mode="direct",
                steps=(OperationalStep(objective=objective),),
                unknowns=("No validated capability was selected by the planning intelligence.",),
                source="deterministic_fallback",
            )
        return OperationalPlan(
            objective=objective,
            understanding=objective,
            mode="direct",
            steps=(OperationalStep(objective=objective, capability_id=str(capability)),),
            source="deterministic_fallback",
        )

    def plan(self, objective: str, context: dict[str, Any] | None = None) -> OperationalPlan:
        objective = str(objective or "").strip()
        if not objective:
            raise ValueError("objective_required")
        context = dict(context or {})

        # If the Imperator explicitly supplies a capability, planning still
        # exists, but does not need to spend another intelligence call.
        if context.get("capability_id") and context.get("skip_planning") is True:
            return self._fallback(objective, context)

        policy = self.cost_policy.policy(context)
        budget = self.cost_policy
        candidates = []
        for cap in self.registry.list():
            if "ai" not in str(getattr(cap, "kind", "")).lower():
                continue
            try:
                candidates.append(self._candidate(cap))
            except Exception:
                continue
        ranked = self.selector.rank(candidates, policy, self._budget(context))
        if not ranked:
            return self._fallback(objective, context)

        selected = ranked[0]
        capability = self.registry.get(selected.id)
        prompt = self._candidate_prompt(objective, context)
        try:
            result = capability.adapter.execute(prompt, {
                **context,
                "_capabilities": self._available_capabilities(),
                "operational_planning": True,
            })
            raw = self._extract_json(result)
            return self._validate(raw, objective, selected.id)
        except Exception:
            # Planning failure must not manufacture a strategy. Fall back to a
            # validated explicit capability only; otherwise return an UNKNOWN
            # plan that the execution governor can safely hold.
            return self._fallback(objective, context)

    def _budget(self, context: dict[str, Any]):
        from .v3 import CostBudget
        return CostBudget(
            float(context.get("max_spend", 0) or 0),
            float(context.get("spent", 0) or 0),
        )

    def _candidate(self, cap):
        return self._candidate_from_capability(cap)

    @staticmethod
    def _candidate_from_capability(cap):
        from .v3 import CostClass, IntelligenceCandidate
        meta = getattr(cap, "metadata", {}) or {}
        kind = str(getattr(cap, "kind", "")).lower()
        raw = str(meta.get("cost_class") or "").lower()
        if not raw:
            raw = CostClass.FREE_LOCAL.value if kind == "local_ai" else CostClass.FREE_EXTERNAL.value
        try:
            cost = CostClass(raw)
        except ValueError:
            cost = CostClass.FREE_EXTERNAL
        caps = tuple(meta.get("capabilities") or ())
        if not caps and kind == "local_ai":
            caps = ("chat", "reasoning")
        return IntelligenceCandidate(
            cap.id, cost, caps, float(meta.get("estimated_cost", 0) or 0),
            True, float(meta.get("latency_ms", 0) or 0),
            cost is CostClass.FREE_LOCAL, float(meta.get("quality", .5) or .5),
            int(meta.get("context_window", 0) or 0),
        )

    def _validate(self, raw: dict[str, Any], objective: str, intelligence_id: str) -> OperationalPlan:
        mode = str(raw.get("mode") or "direct").lower()
        if mode not in self.MODES:
            mode = "direct"
        valid_ids = {c.id for c in self.registry.list()}
        steps: list[OperationalStep] = []
        unknowns = [str(x) for x in raw.get("unknowns") or []]
        for item in list(raw.get("steps") or []):
            if not isinstance(item, dict):
                continue
            cid = item.get("capability_id")
            if cid is not None:
                cid = str(cid)
                if cid not in valid_ids:
                    unknowns.append(f"Unknown capability requested by planning intelligence: {cid}")
                    cid = None
            step_obj = str(item.get("objective") or "").strip()
            if not step_obj:
                continue
            executor = str(item.get("executor") or mode).lower()
            if executor not in self.MODES:
                executor = mode
            priority = str(item.get("priority") or "normal").lower()
            if priority not in {"normal", "high", "critical"}:
                priority = "normal"
            steps.append(OperationalStep(
                objective=step_obj,
                capability_id=cid,
                executor=executor,
                required_capabilities=tuple(str(x) for x in item.get("required_capabilities") or []),
                priority=priority,
                context=dict(item.get("context") or {}) if isinstance(item.get("context"), dict) else {},
            ))
        if not steps:
            raise ValueError("operational_plan_has_no_steps")
        # Never allow a model to escalate execution mode solely by assertion.
        if mode == "multiagent" and len(steps) < 2:
            mode = "direct"
        return OperationalPlan(
            objective=objective,
            understanding=str(raw.get("understanding") or objective),
            mode=mode,
            steps=tuple(steps),
            success_criteria=tuple(str(x) for x in raw.get("success_criteria") or []),
            assumptions=tuple(str(x) for x in raw.get("assumptions") or []),
            unknowns=tuple(dict.fromkeys(unknowns)),
            source="model",
            intelligence_id=intelligence_id,
        )

    def execute(self, objective: str, context: dict[str, Any], orchestrator) -> dict[str, Any]:
        plan = self.plan(objective, context)
        if plan.unknowns and not any(s.capability_id for s in plan.steps):
            return {
                "type": "operational_unknown",
                "plan": plan.public(),
                "completed": False,
                "reason": "no_validated_execution_capability",
            }

        results = []
        for index, step in enumerate(plan.steps, 1):
            step_context = dict(context)
            step_context.update(step.context)
            step_context["priority"] = step.priority
            step_context["operational_plan"] = plan.public()
            step_context["operational_step"] = index
            if step.executor and step.executor != "direct":
                step_context["executor"] = step.executor
            work = orchestrator.create(step.objective, step_context)
            done = orchestrator.run(work.id, step.capability_id, approved=bool(context.get("approved", False)))
            result = {
                "index": index,
                "work_id": done.id,
                "state": done.state.value,
                "capability_id": done.capability_id,
                "result": done.result,
            }
            results.append(result)
            if done.state.value != "completed":
                return {
                    "type": "operational_result",
                    "completed": False,
                    "plan": plan.public(),
                    "steps": results,
                    "failed_step": index,
                }
        return {
            "type": "operational_result",
            "completed": True,
            "plan": plan.public(),
            "steps": results,
        }
