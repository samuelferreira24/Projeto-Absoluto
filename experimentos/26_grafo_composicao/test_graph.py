from dataclasses import dataclass


@dataclass(frozen=True)
class Node:
    name: str
    deps: tuple[str, ...] = ()


def topo_ready(nodes, done):
    return [n.name for n in nodes if n.name not in done and all(dep in done for dep in n.deps)]


def test_dag_allows_parallel_research_and_workflow():
    nodes = [Node("RESEARCH"), Node("WORKFLOW"), Node("AGENT", ("RESEARCH", "WORKFLOW"))]
    assert topo_ready(nodes, set()) == ["RESEARCH", "WORKFLOW"]


def test_join_waits_for_all_dependencies():
    nodes = [Node("A"), Node("B"), Node("JOIN", ("A", "B"))]
    assert topo_ready(nodes, {"A"}) == ["B"]
    assert topo_ready(nodes, {"A", "B"}) == ["JOIN"]


def test_cycle_has_no_ready_node():
    nodes = [Node("A", ("B",)), Node("B", ("A",))]
    assert topo_ready(nodes, set()) == []
