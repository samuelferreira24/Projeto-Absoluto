from prototipo import CandidateA, CandidateB, Mission, ScriptedExecutor


def test_candidates():
    for Candidate in (CandidateA, CandidateB):
        runner = Candidate()
        trace, status = runner.run(
            Mission("x", {"defined_steps": True}),
            ScriptedExecutor(["failure", "success"]),
        )
        assert status == "COMPLETE"
        assert trace[:2] == ["WORKFLOW", "RECOVERY"]


def test_context_change_replans():
    for Candidate in (CandidateA, CandidateB):
        runner = Candidate()
        trace, status = runner.run(
            Mission("x", {"defined_steps": True}),
            ScriptedExecutor(["state_changed", "success"]),
        )
        assert status == "COMPLETE"
        assert trace[:2] == ["WORKFLOW", "AGENT"]


if __name__ == "__main__":
    test_candidates()
    test_context_change_replans()
    print("PROTO_EXECUTAVEL: PASS")
