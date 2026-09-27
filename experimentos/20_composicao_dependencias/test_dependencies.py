from dataclasses import dataclass


@dataclass(frozen=True)
class Step:
    name: str
    deps: tuple[str, ...] = ()


def ready(steps, done):
    return [s.name for s in steps if s.name not in done and all(d in done for d in s.deps)]


def test_research_then_multiagent_dependency():
    steps = [Step("RESEARCH"), Step("MULTIAGENT", ("RESEARCH",))]
    assert ready(steps, set()) == ["RESEARCH"]
    assert ready(steps, {"RESEARCH"}) == ["MULTIAGENT"]


def test_parallel_branches_and_join():
    steps = [Step("RESEARCH"), Step("WORKFLOW"), Step("AGENT", ("RESEARCH", "WORKFLOW"))]
    assert ready(steps, set()) == ["RESEARCH", "WORKFLOW"]
    assert ready(steps, {"RESEARCH"}) == ["WORKFLOW"]
    assert ready(steps, {"RESEARCH", "WORKFLOW"}) == ["AGENT"]


def test_dependency_cycle_is_not_executable():
    steps = [Step("A", ("B",)), Step("B", ("A",))]
    assert ready(steps, set()) == []
