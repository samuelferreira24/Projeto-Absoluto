import itertools

MODES={"DIRECT","WORKFLOW","RESEARCH","AGENT","MULTIAGENT","RECOVERY"}

def transition(state,event):
    if event=="auth_required": return "WAIT_AUTH"
    if event=="capability_missing": return "DISCOVER"
    if event=="context_incomplete": return "OBSERVE"
    if event in ("executor_failure","verification_failure"): return "RECOVERY"
    if event=="state_changed": return "REPLAN"
    if event=="success": return "COMPLETE"
    return state

def test_adversarial_event_sequences():
    events=["auth_required","capability_missing","context_incomplete","executor_failure","verification_failure","state_changed","success"]
    for n in range(1,5):
        for seq in itertools.product(events, repeat=n):
            state="RUNNING"
            blocked=False
            for e in seq:
                state=transition(state,e)
                if state in {"WAIT_AUTH","DISCOVER","OBSERVE","RECOVERY","REPLAN"}:
                    blocked=True
            if "success" in seq and seq[-1]=="success":
                    assert state=="COMPLETE"
            if blocked and seq[-1]!="success":
                assert state!="COMPLETE"
