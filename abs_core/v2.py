from __future__ import annotations

"""ABS V2 integrated control kernel.

This module is intentionally dependency-light. It composes the mature V1
registries/adapters while adding the sovereign V2 control contracts:
authority, policy, mode selection, execution routing, observations, evidence,
risk/budget governance, idempotency, recovery and replanning.
"""

import hashlib
import json
import os
import shlex
import sqlite3
import subprocess
import threading
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable

from .models import Work, WorkState
from .store import WorkStore


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


class V2Mode(str, Enum):
    DIRECT = "direct"
    WORKFLOW = "workflow"
    AGENT = "agent"
    MULTIAGENT = "multiagent"


class V2Status(str, Enum):
    CREATED = "created"
    PLANNING = "planning"
    WAITING_APPROVAL = "waiting_approval"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    WAITING_RESOURCE = "waiting_resource"
    RECOVERING = "recovering"
    REPLANNING = "replanning"
    UNKNOWN = "unknown"
    FAILED = "failed"
    COMPLETED = "completed"
    VERIFIED = "verified"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class Authority:
    actor: str = "imperador"
    scope: str = "work"
    approval: bool = False


@dataclass(frozen=True)
class RiskProfile:
    level: str = "low"
    impact: str = "low"
    reversible: bool = True
    irreversible: bool = False


@dataclass(frozen=True)
class Budget:
    max_attempts: int = 3
    max_subagents: int = 4
    max_seconds: int = 300


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    approval_required: bool
    reason: str
    max_mode: V2Mode = V2Mode.AGENT


@dataclass(frozen=True)
class Observation:
    id: str
    work_id: str
    attempt: int
    source: str
    kind: str
    value: Any
    timestamp: str = field(default_factory=now)


@dataclass(frozen=True)
class Evidence:
    id: str
    work_id: str
    observation_id: str
    claim: str
    method: str
    digest: str
    source: str
    timestamp: str = field(default_factory=now)


@dataclass(frozen=True)
class Verification:
    status: str
    accepted: bool
    reason: str
    evidence_ids: tuple[str, ...] = ()


@dataclass
class V2Plan:
    mode: V2Mode
    capability_id: str | None
    executor_id: str
    rationale: list[str]
    risk: RiskProfile
    budget: Budget


class V2Store:
    """Durable V2 metadata/evidence ledger beside the existing WorkStore."""

    def __init__(self, path: str):
        self.path = path
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.lock = threading.RLock()
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS v2_work (
          work_id TEXT PRIMARY KEY, objective_version INTEGER NOT NULL,
          mode TEXT, executor TEXT, authority TEXT NOT NULL, risk TEXT NOT NULL,
          budget TEXT NOT NULL, status TEXT NOT NULL, plan TEXT, updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS v2_observation (
          id TEXT PRIMARY KEY, work_id TEXT NOT NULL, attempt INTEGER NOT NULL,
          source TEXT NOT NULL, kind TEXT NOT NULL, value TEXT NOT NULL, timestamp TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS v2_evidence (
          id TEXT PRIMARY KEY, work_id TEXT NOT NULL, observation_id TEXT NOT NULL,
          claim TEXT NOT NULL, method TEXT NOT NULL, digest TEXT NOT NULL,
          source TEXT NOT NULL, timestamp TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS v2_idempotency (
          key TEXT PRIMARY KEY, status TEXT NOT NULL, result TEXT, work_id TEXT,
          updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS v2_checkpoints (
          work_id TEXT NOT NULL, seq INTEGER NOT NULL, state TEXT NOT NULL,
          payload TEXT NOT NULL, timestamp TEXT NOT NULL,
          PRIMARY KEY(work_id, seq)
        );
        """)
        self.conn.commit()

    def put_work(self, work_id: str, objective_version: int, plan: V2Plan,
                 authority: Authority, status: V2Status):
        with self.lock:
            self.conn.execute(
                "INSERT OR REPLACE INTO v2_work VALUES(?,?,?,?,?,?,?,?,?,?)",
                (work_id, objective_version, plan.mode.value, plan.executor_id,
                 json.dumps(asdict(authority)), json.dumps(asdict(plan.risk)),
                 json.dumps(asdict(plan.budget)), status.value,
                 json.dumps(asdict(plan)), now()))
            self.conn.commit()

    def status(self, work_id: str, status: V2Status):
        with self.lock:
            self.conn.execute("UPDATE v2_work SET status=?,updated_at=? WHERE work_id=?",
                              (status.value, now(), work_id))
            self.conn.commit()

    def observe(self, item: Observation):
        with self.lock:
            self.conn.execute("INSERT OR REPLACE INTO v2_observation VALUES(?,?,?,?,?,?,?)",
                              (item.id, item.work_id, item.attempt, item.source, item.kind,
                               json.dumps(item.value, ensure_ascii=False), item.timestamp))
            self.conn.commit()

    def evidence(self, item: Evidence):
        with self.lock:
            self.conn.execute("INSERT OR REPLACE INTO v2_evidence VALUES(?,?,?,?,?,?,?,?)",
                              (item.id, item.work_id, item.observation_id, item.claim,
                               item.method, item.digest, item.source, item.timestamp))
            self.conn.commit()

    def idem(self, key: str, status: str, result: Any = None, work_id: str | None = None):
        with self.lock:
            self.conn.execute(
                "INSERT OR REPLACE INTO v2_idempotency VALUES(?,?,?,?,?)",
                (key, status, json.dumps(result, ensure_ascii=False), work_id, now()))
            self.conn.commit()

    def get_idem(self, key: str):
        with self.lock:
            row = self.conn.execute("SELECT status,result,work_id FROM v2_idempotency WHERE key=?",
                                    (key,)).fetchone()
        if not row:
            return None
        return {"status": row[0], "result": json.loads(row[1]) if row[1] else None, "work_id": row[2]}

    def checkpoint(self, work_id: str, state: str, payload: dict[str, Any]):
        with self.lock:
            seq = self.conn.execute("SELECT COALESCE(MAX(seq),0)+1 FROM v2_checkpoints WHERE work_id=?",
                                    (work_id,)).fetchone()[0]
            self.conn.execute("INSERT INTO v2_checkpoints VALUES(?,?,?,?,?)",
                              (work_id, seq, state, json.dumps(payload, ensure_ascii=False), now()))
            self.conn.commit()

    def export_work(self, work_id: str) -> dict[str, Any]:
        with self.lock:
            meta = self.conn.execute("SELECT * FROM v2_work WHERE work_id=?", (work_id,)).fetchone()
            obs = self.conn.execute("SELECT * FROM v2_observation WHERE work_id=? ORDER BY timestamp", (work_id,)).fetchall()
            ev = self.conn.execute("SELECT * FROM v2_evidence WHERE work_id=? ORDER BY timestamp", (work_id,)).fetchall()
            cp = self.conn.execute("SELECT * FROM v2_checkpoints WHERE work_id=? ORDER BY seq", (work_id,)).fetchall()
        return {
            "metadata": meta,
            "observations": obs,
            "evidence": ev,
            "checkpoints": cp,
        }


class AuthorityCore:
    def issue(self, context: dict[str, Any]) -> Authority:
        actor = str(context.get("authority_actor") or "imperador")
        if actor != "imperador":
            raise PermissionError("authority_must_originate_from_imperador")
        return Authority(actor=actor, scope=str(context.get("authority_scope") or "work"),
                         approval=bool(context.get("approved", False)))


class PolicyEngine:
    HIGH_RISK = {"high", "critical"}

    def evaluate(self, objective: str, context: dict[str, Any], risk: RiskProfile) -> PolicyDecision:
        text = objective.lower()
        explicit = bool(context.get("approved", False))
        dangerous = bool(context.get("high_impact", False)) or any(
            token in text for token in ("delete", "destroy", "wipe", "drop database", "format", "shutdown")
        )
        if risk.level in self.HIGH_RISK or risk.irreversible or dangerous:
            if not explicit:
                return PolicyDecision(False, True, "high_impact_or_irreversible_action_requires_approval",
                                      V2Mode.WORKFLOW)
        return PolicyDecision(True, False, "policy_allowed", V2Mode.AGENT)


class ModeSelector:
    def choose(self, objective: str, context: dict[str, Any], risk: RiskProfile) -> tuple[V2Mode, list[str]]:
        if context.get("force_mode"):
            mode = V2Mode(str(context["force_mode"]))
            return mode, ["explicit_mode"]
        if context.get("multiagent") or int(context.get("subagents", 0) or 0) > 0:
            return V2Mode.MULTIAGENT, ["objective_requires_delegation"]
        if context.get("workflow") or len(context.get("steps", []) or []) > 1:
            return V2Mode.WORKFLOW, ["explicit_or_multistep_workflow"]
        if risk.level == "low" and not context.get("adaptive", False):
            return V2Mode.DIRECT, ["low_risk_minimal_sufficient_path"]
        return V2Mode.AGENT, ["adaptive_reasoning_required"]


class RiskGovernor:
    def profile(self, objective: str, context: dict[str, Any]) -> RiskProfile:
        level = str(context.get("risk") or "low").lower()
        if level not in {"low", "medium", "high", "critical"}:
            level = "medium"
        irreversible = bool(context.get("irreversible", False))
        impact = str(context.get("impact") or ("high" if irreversible else "low"))
        return RiskProfile(level=level, impact=impact,
                           reversible=not irreversible, irreversible=irreversible)

    def budget(self, context: dict[str, Any]) -> Budget:
        return Budget(
            max_attempts=max(1, min(int(context.get("max_attempts", 3)), 10)),
            max_subagents=max(0, min(int(context.get("max_subagents", 4)), 16)),
            max_seconds=max(1, min(int(context.get("max_seconds", 300)), 3600)),
        )


class Executor:
    id = "executor"

    def execute(self, objective: str, context: dict[str, Any]) -> Any:
        raise NotImplementedError


class DirectCapabilityExecutor(Executor):
    id = "direct"

    def __init__(self, registry):
        self.registry = registry

    def execute(self, objective: str, context: dict[str, Any]):
        cap = context.get("_v2_capability")
        if not cap:
            raise RuntimeError("v2_capability_not_selected")
        return cap.adapter.execute(objective, context)


class OpenClawExecutor(Executor):
    id = "openclaw"

    def __init__(self, command: str | None = None):
        self.command = command or os.getenv("ABS_OPENCLAW_EXEC_COMMAND", "").strip()

    def available(self) -> bool:
        return bool(self.command or _which("openclaw"))

    def execute(self, objective: str, context: dict[str, Any]):
        command = self.command
        if not command:
            command = "openclaw agent --message {objective} --json"
        rendered = command.format(objective=shlex.quote(objective))
        proc = subprocess.run(rendered, shell=True, text=True, capture_output=True,
                              timeout=int(context.get("timeout_seconds", 300)))
        value = {
            "type": "openclaw",
            "returncode": proc.returncode,
            "stdout": proc.stdout[-12000:],
            "stderr": proc.stderr[-12000:],
        }
        if proc.returncode != 0:
            value["type"] = "error"
            value["error"] = proc.stderr.strip() or f"openclaw_exit_{proc.returncode}"
        return value


class ExecutorRouter:
    def __init__(self, registry):
        self.registry = registry
        self.executors: dict[str, Executor] = {"direct": DirectCapabilityExecutor(registry)}
        self.openclaw = OpenClawExecutor()
        if self.openclaw.available():
            self.executors["openclaw"] = self.openclaw

    def choose(self, mode: V2Mode, capability_id: str | None, context: dict[str, Any]) -> tuple[str, Executor]:
        preferred = str(context.get("executor") or "").strip()
        if preferred in self.executors:
            return preferred, self.executors[preferred]
        if mode in {V2Mode.AGENT, V2Mode.MULTIAGENT} and "openclaw" in self.executors:
            return "openclaw", self.executors["openclaw"]
        return "direct", self.executors["direct"]


def _which(name: str) -> str | None:
    import shutil
    return shutil.which(name)


class VerificationEngine:
    def verify(self, result: Any, observations: list[Observation], risk: RiskProfile) -> Verification:
        if result is None:
            return Verification("unknown", False, "no_result")
        if isinstance(result, dict) and result.get("type") == "error":
            return Verification("rejected", False, "execution_error")
        if not observations:
            return Verification("unknown", False, "no_independent_observation")
        checks = []
        for item in observations:
            checks.append(item.value is not None)
        if all(checks):
            return Verification("accepted", True, "observed_execution_result",
                                 tuple(item.id for item in observations))
        return Verification("unknown", False, "insufficient_observation")


class Replanner:
    def next_context(self, context: dict[str, Any], failed_executor: str | None = None) -> dict[str, Any]:
        updated = dict(context)
        if failed_executor == "openclaw":
            updated["executor"] = "direct"
            updated["adaptive"] = False
        updated["replanned"] = True
        return updated


class ABSV2Orchestrator:
    """V2 orchestration facade compatible with the V1 Work/API contract."""

    def __init__(self, registry, store: WorkStore, *, data_layer=None, knowledge_runtime=None):
        self.registry = registry
        self.store = store
        self.data_layer = data_layer
        self.knowledge_runtime = knowledge_runtime
        db_path = str(store.path) if str(store.path) != ":memory:" else ":memory:"
        self.v2store = V2Store(db_path)
        self.authority = AuthorityCore()
        self.policy = PolicyEngine()
        self.modes = ModeSelector()
        self.governor = RiskGovernor()
        self.router = ExecutorRouter(registry)
        self.verifier = VerificationEngine()
        self.replanner = Replanner()
        self._lock = threading.RLock()

    def create(self, objective: str, context: dict[str, Any] | None = None) -> Work:
        objective = str(objective or "").strip()
        if not objective:
            raise ValueError("objective_required")
        context = dict(context or {})
        work = Work(objective, context)
        work.context["_v2"] = {
            "objective_version": 1,
            "status": V2Status.CREATED.value,
            "authority": asdict(self.authority.issue(context)),
        }
        work.emit("v2.work.created", objective_version=1)
        self.store.save(work)
        return work

    def _prepare(self, work: Work, approved: bool) -> tuple[V2Plan, PolicyDecision]:
        context = dict(work.context)
        context["approved"] = approved or bool(context.get("approved", False))
        authority = self.authority.issue(context)
        risk = self.governor.profile(work.objective, context)
        budget = self.governor.budget(context)
        decision = self.policy.evaluate(work.objective, context, risk)
        mode, rationale = self.modes.choose(work.objective, context, risk)
        if mode == V2Mode.MULTIAGENT and budget.max_subagents < 1:
            raise RuntimeError("multiagent_budget_exhausted")
        if decision.max_mode == V2Mode.WORKFLOW and mode in {V2Mode.AGENT, V2Mode.MULTIAGENT}:
            mode = V2Mode.WORKFLOW
            rationale.append("policy_mode_cap")
        cap_id = context.get("capability_id")
        if not cap_id:
            if mode == V2Mode.DIRECT and self.registry.list():
                cap_id = "echo" if any(c.id == "echo" for c in self.registry.list()) else self.registry.list()[0].id
            elif context.get("required_capability"):
                cap_id = str(context["required_capability"])
        if cap_id:
            self.registry.get(cap_id)
        executor_id, _ = self.router.choose(mode, cap_id, context)
        plan = V2Plan(mode, cap_id, executor_id, rationale, risk, budget)
        self.v2store.put_work(work.id, 1, plan, authority, V2Status.READY)
        work.context["_v2"].update({
            "mode": mode.value, "executor": executor_id, "risk": asdict(risk),
            "budget": asdict(budget), "plan_rationale": rationale,
        })
        return plan, decision

    def run(self, work_id: str, capability_id: str | None = None, approved: bool = False) -> Work:
        with self._lock:
            work = self.store.load(work_id)
            context = dict(work.context)
            if capability_id:
                context["capability_id"] = capability_id
            context["approved"] = approved or bool(context.get("approved", False))
            work.context = context
            try:
                plan, decision = self._prepare(work, approved)
            except PermissionError as exc:
                work.state = WorkState.FAILED
                work.result = {"type": "policy_error", "error": str(exc)}
                work.emit("v2.policy.rejected", reason=str(exc))
                self.store.save(work)
                return work
            if not decision.allowed:
                work.state = WorkState.PAUSED
                work.context["_v2"]["status"] = V2Status.WAITING_APPROVAL.value
                work.emit("v2.waiting_approval", reason=decision.reason)
                self.v2store.status(work.id, V2Status.WAITING_APPROVAL)
                self.store.save(work)
                return work

            if plan.mode == V2Mode.MULTIAGENT:
                requested = int(context.get("subagents", 1) or 1)
                if requested > plan.budget.max_subagents:
                    work.state = WorkState.FAILED
                    work.result = {"type": "budget_error", "error": "subagent_admission_denied"}
                    self.store.save(work)
                    return work

            idem_key = str(context.get("idempotency_key") or "").strip()
            if idem_key:
                prior = self.v2store.get_idem(idem_key)
                if prior and prior["status"] == "completed":
                    work.result = prior["result"]
                    work.state = WorkState.COMPLETED
                    work.emit("v2.idempotency.replayed", key=idem_key)
                    self.v2store.status(work.id, V2Status.VERIFIED)
                    self.store.save(work)
                    return work
                self.v2store.idem(idem_key, "reserved", work_id=work.id)

            cap_id = plan.capability_id or capability_id
            cap = self.registry.get(cap_id) if cap_id else None
            if cap:
                work.capability_id = cap.id
            if plan.executor_id == "direct" and cap is None:
                work.state = WorkState.FAILED
                work.result = {"type": "error", "error": "no_capability_for_direct_execution"}
                self.store.save(work)
                return work

            executor = self.router.executors[plan.executor_id]
            observations: list[Observation] = []
            last_error = None
            for attempt in range(1, plan.budget.max_attempts + 1):
                work.state = WorkState.RUNNING
                work.context["_v2"]["status"] = V2Status.RUNNING.value
                self.v2store.status(work.id, V2Status.RUNNING)
                self.v2store.checkpoint(work.id, V2Status.RUNNING.value, {
                    "attempt": attempt, "mode": plan.mode.value, "executor": plan.executor_id
                })
                work.emit("v2.execution.started", attempt=attempt, executor=plan.executor_id,
                          mode=plan.mode.value)
                execution_context = dict(work.context)
                # Adapters receive a serializable public context; the live capability
                # object never crosses the persistence boundary.
                execution_context.pop("_v2_capability", None)
                execution_context["_v2_capability_id"] = cap.id if cap else None
                execution_context["timeout_seconds"] = plan.budget.max_seconds
                if plan.executor_id == "direct":
                    execution_context["_v2_capability"] = cap
                try:
                    result = executor.execute(work.objective, execution_context)
                    if isinstance(result, dict):
                        result = json.loads(json.dumps(result, default=str))
                    obs = Observation(str(uuid.uuid4()), work.id, attempt, plan.executor_id,
                                      "execution_result", result)
                    observations.append(obs)
                    self.v2store.observe(obs)
                    verification = self.verifier.verify(result, observations, plan.risk)
                    evidence_ids: list[str] = []
                    for item in observations:
                        raw = json.dumps(item.value, sort_keys=True, default=str)
                        evidence = Evidence(
                            str(uuid.uuid4()), work.id, item.id,
                            "executor_result_observed", "runtime-observation",
                            hashlib.sha256(raw.encode()).hexdigest(), item.source)
                        self.v2store.evidence(evidence)
                        evidence_ids.append(evidence.id)
                    work.result = {
                        "type": "v2_result",
                        "mode": plan.mode.value,
                        "executor": plan.executor_id,
                        "attempt": attempt,
                        "result": result,
                        "verification": asdict(verification),
                        "evidence_ids": evidence_ids,
                    }
                    work.provenance.append({
                        "provenance_id": str(uuid.uuid4()), "work_id": work.id,
                        "capability_id": cap.id if cap else None,
                        "executor": plan.executor_id, "mode": plan.mode.value,
                        "attempt": attempt, "recorded_at": now(),
                        "verification": asdict(verification),
                        "evidence_ids": evidence_ids,
                    })
                    if verification.accepted:
                        work.state = WorkState.COMPLETED
                        work.context["_v2"]["status"] = V2Status.VERIFIED.value
                        self.v2store.status(work.id, V2Status.VERIFIED)
                        work.emit("v2.verified", attempt=attempt, evidence_ids=evidence_ids)
                        if idem_key:
                            self.v2store.idem(idem_key, "completed", work.result, work.id)
                        self.v2store.checkpoint(work.id, V2Status.VERIFIED.value, {
                            "attempt": attempt, "evidence_ids": evidence_ids
                        })
                        self.store.save(work)
                        if self.data_layer:
                            try:
                                self.data_layer.record_work_result(work.id, work.objective, work.result, "verified")
                            except Exception:
                                pass
                        return work
                    last_error = verification.reason
                    work.emit("v2.verification_failed", reason=verification.reason)
                except Exception as exc:
                    last_error = f"{type(exc).__name__}: {exc}"
                    work.emit("v2.execution_failed", attempt=attempt, error=last_error)

                if attempt < plan.budget.max_attempts:
                    work.state = WorkState.PAUSED
                    work.context = self.replanner.next_context(work.context, plan.executor_id)
                    work.context["_v2"]["status"] = V2Status.REPLANNING.value
                    self.v2store.status(work.id, V2Status.REPLANNING)
                    work.emit("v2.replanning", next_attempt=attempt + 1)
                    if plan.executor_id != "direct" and "direct" in self.router.executors:
                        plan = V2Plan(plan.mode, plan.capability_id, "direct",
                                      plan.rationale + ["executor_fallback"], plan.risk, plan.budget)
                        self.v2store.put_work(work.id, 1, plan, self.authority.issue(work.context), V2Status.REPLANNING)
                        executor = self.router.executors["direct"]

            work.state = WorkState.FAILED if last_error else WorkState.COMPLETED
            work.context["_v2"]["status"] = V2Status.FAILED.value
            work.result = {
                "type": "v2_failure", "error": last_error or "verification_unknown",
                "mode": plan.mode.value, "executor": plan.executor_id,
                "observations": len(observations),
            }
            self.v2store.status(work.id, V2Status.FAILED)
            if idem_key:
                self.v2store.idem(idem_key, "failed", work.result, work.id)
            self.store.save(work)
            return work

    def pause(self, work_id: str) -> Work:
        work = self.store.load(work_id)
        work.state = WorkState.PAUSED
        work.context.setdefault("_v2", {})["status"] = V2Status.PAUSED.value
        self.v2store.status(work_id, V2Status.PAUSED)
        work.emit("v2.paused")
        self.store.save(work)
        return work

    def resume(self, work_id: str, capability_id: str | None = None, approved: bool = False) -> Work:
        return self.run(work_id, capability_id, approved)

    def inspect(self, work_id: str) -> dict[str, Any]:
        work = self.store.load(work_id)
        return {
            "work": {
                "id": work.id, "objective": work.objective, "state": work.state.value,
                "capability_id": work.capability_id, "context": work.context,
                "result": work.result, "provenance": work.provenance,
                "events": [e.__dict__ for e in work.events],
            },
            "v2": self.v2store.export_work(work_id),
        }
