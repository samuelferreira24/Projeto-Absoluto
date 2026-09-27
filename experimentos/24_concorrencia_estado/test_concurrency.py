class VersionedState:
    def __init__(self):
        self.version = 0
        self.value = "WORKFLOW"

    def read(self):
        return self.version, self.value

    def commit(self, expected_version, value):
        if expected_version != self.version:
            return False
        self.value = value
        self.version += 1
        return True


def test_stale_plan_is_rejected():
    s = VersionedState()
    v1, _ = s.read()
    v2, _ = s.read()
    assert s.commit(v1, "AGENT") is True
    assert s.commit(v2, "DIRECT") is False
    assert s.value == "AGENT"
    assert s.version == 1


def test_fresh_replan_can_commit_after_conflict():
    s = VersionedState()
    v, _ = s.read()
    assert s.commit(v, "AGENT")
    fresh, _ = s.read()
    assert s.commit(fresh, "RECOVERY")
    assert s.value == "RECOVERY"
