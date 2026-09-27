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


def test_mutations_are_detected():
    cases = [
        (Mission(recovery_required=True, authorization_required=True), "RECOVERY"),
        (Mission(authorization_required=True), "WAIT_AUTH"),
        (Mission(capability_missing=True), "DISCOVER"),
        (Mission(executor_success=True, goal_achieved=False), "REPLAN"),
    ]
    mutants = [
        mutated_recovery,
        mutated_auth,
        mutated_discovery,
        mutated_verification,
    ]
    for mutant in mutants:
        assert any(mutant(mission) != expected for mission, expected in cases)


def test_baseline_oracle():
    assert baseline(Mission(recovery_required=True, authorization_required=True)) == "RECOVERY"
    assert baseline(Mission(authorization_required=True)) == "WAIT_AUTH"
    assert baseline(Mission(capability_missing=True)) == "DISCOVER"
    assert baseline(Mission(executor_success=True, goal_achieved=False)) == "REPLAN"
