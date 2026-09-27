from moldes import Mission, MoldRuntime, MoldSelector, default_registry


def expect(name, actual, expected):
    assert actual == expected, f"{name}: expected {expected!r}, got {actual!r}"

registry = default_registry()
selector = MoldSelector(registry)
runtime = MoldRuntime(registry)

cases = [
    ("direct", Mission("x"), ["DIRECT"]),
    ("workflow", Mission("x", {"defined_steps": True}), ["WORKFLOW"]),
    ("agent", Mission("x", {"open_ended": True}), ["AGENT"]),
    ("multiagent", Mission("x", {"parallelizable": True, "independent_parts": 3}), ["MULTIAGENT"]),
    ("research", Mission("x", {"high_uncertainty": True}), ["RESEARCH"]),
    ("recovery", Mission("x", {"recovery_required": True}), ["RECOVERY"]),
]
for name, mission, expected in cases:
    expect(name, selector.choose(mission).molds, expected)

p = selector.choose(Mission("research and parallelize", {"high_uncertainty": True, "parallelizable": True, "independent_parts": 4}))
expect("research+multiagent", p.molds, ["RESEARCH", "MULTIAGENT"])

p = selector.choose(Mission("workflow with reasoning", {"defined_steps": True, "open_ended": True}))
expect("workflow+agent", p.molds, ["WORKFLOW", "AGENT"])

p = selector.choose(Mission("continue", {"recovery_required": True, "high_uncertainty": True, "parallelizable": True, "independent_parts": 5}))
expect("recovery priority", p.molds, ["RECOVERY"])

p = selector.choose(Mission("simple", explicit_molds=["AGENT"]))
expect("explicit override", p.molds, ["AGENT"])
expect("override not automatic", p.automatic, False)

p = selector.choose(Mission("mission", explicit_molds=["RESEARCH", "WORKFLOW", "AGENT"]))
expect("explicit composition", p.molds, ["RESEARCH", "WORKFLOW", "AGENT"])

p = selector.choose(Mission("parallel under budget", {"parallelizable": True, "independent_parts": 3, "max_complexity": 2}))
expect("complexity budget", p.molds, ["DIRECT"])

p = selector.choose(Mission("open problem but agent prohibited", {"open_ended": True, "forbid_molds": ["AGENT"]}))
expect("forbidden fallback", p.molds, ["DIRECT"])

a = selector.choose(Mission("known operation", {"resource": "phone"}))
b = selector.choose(Mission("known operation", {"resource": "vps"}))
expect("resource independence", a.molds, b.molds)

a = selector.choose(Mission("collect datum"))
b = selector.choose(Mission("collect datum", {"high_uncertainty": True}))
expect("same objective baseline", a.molds, ["DIRECT"])
expect("same objective changed context", b.molds, ["RESEARCH"])

p = selector.choose(Mission("combined", {"high_uncertainty": True, "defined_steps": True, "open_ended": True}))
results = runtime.run(p, Mission("combined", {"high_uncertainty": True, "defined_steps": True, "open_ended": True}))
expect("runtime result count", len(results), len(p.molds))

try:
    selector.choose(Mission("invalid", explicit_molds=["UNKNOWN"]))
except ValueError:
    pass
else:
    raise AssertionError("unknown mold accepted")

print("PROTO_MOLDES_V0_1: PASS — 11 groups")
print("Moldes:", ", ".join(registry.available()))
