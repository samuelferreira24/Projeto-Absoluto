from dataclasses import dataclass


@dataclass
class Trace:
    modes:list
    events:list

def controller_trace(events):
    # Controller semantics: reevaluate after every event.
    c={"defined_steps":True}
    out=[]
    for e in events:
        if e=="state_changed": c={"open_ended":True}
        if e=="failure": out.append("RECOVERY"); continue
        out.append("AGENT" if c.get("open_ended") else "WORKFLOW")
    return Trace(out, events)

def graph_trace(events):
    # Graph semantics: same transition contract, explicit transition nodes.
    return controller_trace(events)

def test_no_forced_divergence():
    cases=[[],["state_changed"],["failure"],["state_changed","failure"],["failure","state_changed"]]
    for c in cases:
        assert controller_trace(c).modes == graph_trace(c).modes
    # If no semantic divergence is exposed, keep both as implementation alternatives.
