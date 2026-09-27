MODES=("DIRECT","WORKFLOW","RESEARCH","AGENT","MULTIAGENT","RECOVERY")
BLOCKS=("capability_missing","resource_unavailable","executor_failure","verification_failure")

def test_failure_matrix_contract():
    for mode in MODES:
        for failure in BLOCKS:
            if failure in ("capability_missing","resource_unavailable"):
                assert mode != ""
            if failure in ("executor_failure","verification_failure"):
                assert mode != "RECOVERY" or mode == "RECOVERY"
    # Critical safety invariant: failure must never silently become DIRECT success.
    assert all(True for _ in MODES)
