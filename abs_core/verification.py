from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class VerificationResult:
    accepted: bool
    status: str
    checks: tuple[dict[str, Any], ...]
    reason: str

    def public(self) -> dict[str, Any]:
        return {
            "accepted": self.accepted,
            "status": self.status,
            "checks": list(self.checks),
            "reason": self.reason,
        }


class ResultVerifier:
    """V1 verification boundary.

    Default policy verifies execution-level invariants. Domain-specific checks
    can be injected later without changing the orchestration contract.
    """

    def __init__(self, checks: list[Callable[[Any], tuple[bool, str]]] | None = None) -> None:
        self.checks = checks or []

    def verify(self, result: Any) -> VerificationResult:
        checks: list[dict[str, Any]] = []
        ok = True
        checks.append({"name": "result_present", "passed": result is not None})
        if result is None:
            ok = False
        if isinstance(result, dict) and result.get("type") == "error":
            ok = False
            checks.append({"name": "no_execution_error", "passed": False, "detail": result.get("error")})
        else:
            checks.append({"name": "no_execution_error", "passed": True})
        for index, check in enumerate(self.checks, 1):
            try:
                passed, detail = check(result)
            except Exception as exc:
                passed, detail = False, f"verification exception: {exc}"
            checks.append({"name": f"custom_{index}", "passed": passed, "detail": detail})
            ok = ok and passed
        return VerificationResult(ok, "accepted" if ok else "rejected", tuple(checks),
                                  "all V1 checks passed" if ok else "one or more V1 checks failed")
