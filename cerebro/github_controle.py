from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Mapping


TERMINAL_RUN_STATES = {"completed"}
SUCCESS_CONCLUSIONS = {"success"}
FAILURE_CONCLUSIONS = {
    "failure",
    "cancelled",
    "timed_out",
    "action_required",
    "startup_failure",
    "stale",
}


def agora() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def correlation_id(*parts: str) -> str:
    """Cria um identificador determinístico para correlacionar uma execução."""
    payload = "|".join(str(part) for part in parts)
    return "CORR-" + sha256(payload.encode("utf-8")).hexdigest()[:20]


def idempotency_key(repo: str, ref: str, operation: str) -> str:
    return "IDEM-" + sha256(f"{repo}|{ref}|{operation}".encode("utf-8")).hexdigest()[:24]


@dataclass(frozen=True)
class GitHubExecution:
    repository: str
    ref: str
    commit: str
    workflow: str | None
    run_id: int | None
    status: str | None
    conclusion: str | None
    correlation_id: str
    observed_at: str

    @property
    def terminal(self) -> bool:
        return self.status in TERMINAL_RUN_STATES

    @property
    def successful(self) -> bool:
        return self.terminal and self.conclusion in SUCCESS_CONCLUSIONS

    @property
    def failed(self) -> bool:
        return self.terminal and self.conclusion in FAILURE_CONCLUSIONS

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalizar_execucao(
    payload: Mapping[str, Any],
    *,
    repository: str,
    ref: str | None = None,
    workflow: str | None = None,
    observed_at: str | None = None,
) -> GitHubExecution:
    """Converte resposta do GitHub em um registro estável do Projeto."""
    commit = str(payload.get("head_sha") or payload.get("sha") or "")
    resolved_ref = str(ref or payload.get("head_branch") or payload.get("ref") or "")
    resolved_workflow = workflow or payload.get("name") or payload.get("workflow_name")
    raw_run_id = payload.get("id") or payload.get("run_id")
    run_id = int(raw_run_id) if raw_run_id is not None else None
    status = payload.get("status")
    conclusion = payload.get("conclusion")
    return GitHubExecution(
        repository=repository,
        ref=resolved_ref,
        commit=commit,
        workflow=str(resolved_workflow) if resolved_workflow else None,
        run_id=run_id,
        status=str(status) if status else None,
        conclusion=str(conclusion) if conclusion else None,
        correlation_id=correlation_id(repository, resolved_ref, commit, str(run_id or "")),
        observed_at=observed_at or agora(),
    )


def classificar_estado(execucao: GitHubExecution) -> str:
    """Estado operacional simples, sem confundir execução com validação do sistema inteiro."""
    if execucao.successful:
        return "VALIDADO_CI"
    if execucao.failed:
        return "FALHOU_CI"
    if execucao.status in {"queued", "in_progress", "waiting", "requested", "pending"}:
        return "EM_VALIDACAO_CI"
    return "ESTADO_DESCONHECIDO_CI"


def registro_evento(
    execucao: GitHubExecution,
    *,
    event_type: str,
    result: str,
    evidence: list[str] | None = None,
    details: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Formato portátil para devolver observações do GitHub ao estado do Projeto."""
    return {
        "event_id": "GH-EVENT-" + sha256(
            f"{execucao.correlation_id}|{event_type}|{result}".encode("utf-8")
        ).hexdigest()[:20],
        "event_type": event_type,
        "repository": execucao.repository,
        "ref": execucao.ref,
        "commit": execucao.commit,
        "run_id": execucao.run_id,
        "correlation_id": execucao.correlation_id,
        "idempotency_key": idempotency_key(execucao.repository, execucao.ref, event_type),
        "observed_at": execucao.observed_at,
        "result": result,
        "evidence": evidence or [],
        "details": dict(details or {}),
    }


def json_canonico(data: Mapping[str, Any]) -> str:
    """Serialização determinística para evidências, testes e comparação de estado."""
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
