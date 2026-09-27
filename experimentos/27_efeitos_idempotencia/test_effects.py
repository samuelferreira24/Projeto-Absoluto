class EffectLedger:
    def __init__(self):
        self.applied = set()

    def apply(self, effect_id):
        if effect_id in self.applied:
            return False
        self.applied.add(effect_id)
        return True


def test_same_effect_is_applied_once():
    ledger = EffectLedger()
    assert ledger.apply("email-1") is True
    assert ledger.apply("email-1") is False
    assert ledger.applied == {"email-1"}


def test_distinct_effects_are_independent():
    ledger = EffectLedger()
    assert ledger.apply("a") is True
    assert ledger.apply("b") is True
    assert ledger.applied == {"a", "b"}
