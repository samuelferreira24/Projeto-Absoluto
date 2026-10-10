from __future__ import annotations

import subprocess
from pathlib import Path

from abs_core.project_knowledge import RepositoryScanner, synchronize, trace_trajectory, validate_trajectory
from abs_core.trajectory import TrajectoryGraph


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, stdout=subprocess.DEVNULL)


def test_bidirectional_trace_and_validation():
    graph = TrajectoryGraph(
        [{"id": "A"}, {"id": "B"}, {"id": "C"}],
        [
            {"id": "r1", "source": "A", "relation": "led_to", "target": "B"},
            {"id": "r2", "source": "B", "relation": "led_to", "target": "C"},
        ],
    )
    assert graph.descendants("A")[-1] == ["A", "B", "C"]
    assert graph.ancestors("C")[-1] == ["C", "B", "A"]
    assert graph.validate() == []


def test_strict_cycle_is_rejected():
    graph = TrajectoryGraph(
        [{"id": "A"}, {"id": "B"}],
        [
            {"id": "r1", "source": "A", "relation": "precedes", "target": "B"},
            {"id": "r2", "source": "B", "relation": "precedes", "target": "A"},
        ],
    )
    assert any(issue.kind == "strict_cycle" for issue in graph.validate())


def test_repository_trajectory_uses_git_and_explicit_registry(tmp_path: Path):
    (tmp_path / "abs_core").mkdir()
    file_path = tmp_path / "abs_core" / "orchestrator.py"
    file_path.write_text("v1", encoding="utf-8")
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.email", "test@example.invalid")
    _git(tmp_path, "config", "user.name", "Test")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-qm", "origin")
    file_path.write_text("v2", encoding="utf-8")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-qm", "change")

    # A minimal repository without the project registry still has a valid Git
    # trajectory; semantic registry is optional at scan time.
    knowledge = RepositoryScanner(tmp_path).scan()
    assert knowledge.schema_version == "1.4"
    assert not validate_trajectory(knowledge)
    assert any(r.relation == "precedes" for r in knowledge.relations)
    assert any(r.relation == "changed" for r in knowledge.relations)


def test_current_project_registry_is_observable():
    knowledge = RepositoryScanner(Path(".")).scan()
    ids = {r.id for r in knowledge.relations}
    assert "traj:navigation-points-handoff" in ids
    assert "source:trajectory-registry" in {s.id for s in knowledge.knowledge_sources}
    assert not validate_trajectory(knowledge)


def test_projection_contains_bidirectional_trajectory(tmp_path: Path):
    (tmp_path / "abs_core").mkdir()
    (tmp_path / "abs_core" / "orchestrator.py").write_text("x", encoding="utf-8")
    result = synchronize(tmp_path, tmp_path / "knowledge")
    projection = Path(result["map"]).read_text(encoding="utf-8")
    assert "## Trajetória" in projection
    assert "## Relações de trajetória" in projection


def test_strict_validation_handles_trajectories_deeper_than_recursion_limit():
    size = 1500
    nodes = [{"id": f"N{i}"} for i in range(size)]
    relations = [
        {"id": f"r{i}", "source": f"N{i}", "relation": "precedes", "target": f"N{i + 1}"}
        for i in range(size - 1)
    ]
    graph = TrajectoryGraph(nodes, relations)
    assert graph.validate() == []

    relations.append({"id": "cycle", "source": f"N{size - 1}", "relation": "precedes", "target": "N0"})
    graph_with_cycle = TrajectoryGraph(nodes, relations)
    assert any(issue.kind == "strict_cycle" for issue in graph_with_cycle.validate())


def test_non_strict_cycles_do_not_repeat_paths():
    graph = TrajectoryGraph(
        [{"id": "A"}, {"id": "B"}, {"id": "C"}],
        [
            {"id": "r1", "source": "A", "relation": "points_to", "target": "B"},
            {"id": "r2", "source": "B", "relation": "points_to", "target": "C"},
            {"id": "r3", "source": "C", "relation": "points_to", "target": "A"},
        ],
    )
    paths = graph.trace("A", direction="forward", max_depth=8)
    assert all(len(path) == len(set(path)) for path in paths)
