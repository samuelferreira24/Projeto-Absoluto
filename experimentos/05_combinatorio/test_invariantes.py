import sys
from itertools import product
sys.path.insert(0, "../02_validacao_prototipos")
from prototipos import ControllerA, Mission, MoldGraphB


def invariant_suite():
    a = ControllerA()
    b = MoldGraphB()
    flags = [
        "research_required", "defined_steps", "open_ended", "parallelizable",
        "context_incomplete", "authorization_required", "required_capability_missing",
        "recovery_required",
    ]

    tested = 0
    for values in product([False, True], repeat=len(flags)):
        ctx = dict(zip(flags, values))
        if ctx["parallelizable"]:
            ctx["independent_parts"] = 2

        da = a.step(Mission("x", ctx))
        pb = b.plan(Mission("x", ctx))

        if ctx["recovery_required"]:
            assert da.modes == ["RECOVERY"] and pb == ["RECOVERY"]
        elif ctx["authorization_required"]:
            assert da.control == "WAIT_AUTH" and pb == ["WAIT_AUTH"]
        elif ctx["required_capability_missing"]:
            assert da.control == "DISCOVER" and pb == ["DISCOVER"]
        elif ctx["context_incomplete"]:
            assert da.control == "OBSERVE" and pb == ["OBSERVE"]
        else:
            forbidden = set(ctx.get("forbid_modes", []))
            assert not (set(da.modes) & forbidden)
            assert not (set(pb) & forbidden)
        tested += 1

    # Explicit AV constraints are checked separately.
    for max_complexity in range(1, 5):
        for mode in ("DIRECT", "WORKFLOW", "RESEARCH", "AGENT", "MULTIAGENT"):
            ctx = {"max_complexity": max_complexity}
            if mode == "DIRECT": pass
            elif mode == "WORKFLOW": ctx["defined_steps"] = True
            elif mode == "RESEARCH": ctx["research_required"] = True
            elif mode == "AGENT": ctx["open_ended"] = True
            elif mode == "MULTIAGENT": ctx.update(parallelizable=True, independent_parts=2)

            da = a.step(Mission("x", ctx))
            pb = b.plan(Mission("x", ctx))
            weights = {"DIRECT":1, "WORKFLOW":2, "RESEARCH":2, "AGENT":3, "MULTIAGENT":4}
            for selected in da.modes:
                assert weights[selected] <= max_complexity
            for selected in pb:
                if selected in weights:
                    assert weights[selected] <= max_complexity

    print("EXPERIMENTO_05: PASS")
    print("Combinações de contexto testadas:", tested)
    print("Restrições de complexidade testadas:", 20)


if __name__ == "__main__":
    invariant_suite()
