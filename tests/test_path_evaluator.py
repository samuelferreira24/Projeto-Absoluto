from abs_core.path_evaluator import PathEvaluator
from abs_core.project_knowledge import Evidence, PathRecord


def test_path_requires_explicit_evidence_for_promotion():
    path = PathRecord("P1", "x", "a", "b", "observed", evidence=["E1"])
    ev = Evidence("E1", "repository_scan", "repo", "2026-01-01T00:00:00Z", "observed")
    assert PathEvaluator().evaluate(path, [ev]).state == "observed"


def test_path_promotes_to_tested_only_from_test_evidence():
    path = PathRecord("P1", "x", "a", "b", "observed", evidence=["E1"])
    ev = Evidence("E1", "test", "ci", "2026-01-01T00:00:00Z", "tested")
    assert PathEvaluator().evaluate(path, [ev]).state == "tested"


def test_failure_degrades_path():
    path = PathRecord("P1", "x", "a", "b", "operational", evidence=["E1"])
    ev = Evidence("E1", "runtime", "run", "2026-01-01T00:00:00Z", "failure")
    assert PathEvaluator().evaluate(path, [ev]).state == "degraded"
