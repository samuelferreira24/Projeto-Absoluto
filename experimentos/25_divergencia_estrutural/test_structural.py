class ControllerA:
    def run(self, events):
        trace = []
        mode = "WORKFLOW"
        for event in events:
            if event == "state_changed":
                mode = "AGENT"
                trace.append(("REPLAN", mode))
            elif event == "failure":
                mode = "RECOVERY"
                trace.append(("RECOVER", mode))
            else:
                trace.append(("EXECUTE", mode))
        return trace


class GraphB:
    def run(self, events):
        mode = "WORKFLOW"
        trace = []
        transitions = {"state_changed": ("REPLAN", "AGENT"), "failure": ("RECOVER", "RECOVERY")}
        for event in events:
            if event in transitions:
                action, mode = transitions[event]
                trace.append((action, mode))
            else:
                trace.append(("EXECUTE", mode))
        return trace


def test_internal_structures_are_distinct_but_contract_matches():
    events = ["execute", "state_changed", "execute", "failure"]
    assert ControllerA.__dict__["run"] is not GraphB.__dict__["run"]
    assert ControllerA().run(events) == GraphB().run(events)


def test_intermediate_replan_is_observable():
    trace = ControllerA().run(["execute", "state_changed", "execute"])
    assert trace == [("EXECUTE", "WORKFLOW"), ("REPLAN", "AGENT"), ("EXECUTE", "AGENT")]


def test_failure_after_replan_recovers_from_current_state():
    for impl in (ControllerA(), GraphB()):
        trace = impl.run(["state_changed", "execute", "failure"])
        assert trace[-1] == ("RECOVER", "RECOVERY")
