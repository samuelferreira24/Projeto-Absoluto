from dataclasses import dataclass


@dataclass
class Mission:
    recovery_required: bool = False
    authorization_required: bool = False
    capability_missing: bool = False
    executor_success: bool = False
    goal_achieved: bool = False


def baseline(m):
    if m.recovery_required:
        return "RECOVERY"
    if m.authorization_required:
        return "WAIT_AUTH"
    if m.capability_missing:
        return "DISCOVER"
    if not m.executor_success:
        return "RUN"
    return "COMPLETE" if m.goal_achieved else "REPLAN"


def mutated_recovery(m):
    if m.authorization_required:
        return "WAIT_AUTH"
    if m.capability_missing:
        return "DISCOVER"
    if not m.executor_success:
        return "RUN"
    return "COMPLETE" if m.goal_achieved else "REPLAN"


def mutated_auth(m):
    if m.recovery_required:
        return "RECOVERY"
    if m.capability_missing:
        return "DISCOVER"
    if not m.executor_success:
        return "RUN"
    return "COMPLETE" if m.goal_achieved else "REPLAN"


def mutated_discovery(m):
    if m.recovery_required:
        return "RECOVERY"
    if m.authorization_required:
        return "WAIT_AUTH"
    if not m.executor_success:
        return "RUN"
    return "COMPLETE" if m.goal_achieved else "REPLAN"


def mutated_verification(m):
    if m.recovery_required:
        return "RECOVERY"
    if m.authorization_required:
        return "WAIT_AUTH"
    if m.capability_missing:
        return "DISCOVER"
    if not m.executor_success:
        return "RUN"
    return "COMPLETE"


CASES = [
    (Mission(recovery_required=True, authorization_required=True), "RECOVERY"),
    (Mission(authorization_required=True), "WAIT_AUTH"),
    (Mission(capability_missing=True), "DISCOVER"),
    (Mission(executor_success=True, goal_achieved=False), "REPLAN"),
]


def test_baseline_oracle():
    for mission, expected in CASES:
        assert baseline(mission) == expected


def test_each_critical_mutation_is_detected_by_a_specific_case():
    mutants = {
        mutated_recovery: CASES[0],
        mutated_auth: CASES[1],
        mutated_discovery: CASES[2],
        mutated_verification: CASES[3],
    }
    for mutant, (mission, expected) in mutants.items():
        assert mutant(mission) != expected
