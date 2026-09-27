class Runtime:
    def __init__(self):
        self.done = []

    def execute(self, step):
        if step not in self.done:
            self.done.append(step)
        return step

    def checkpoint(self):
        return list(self.done)

    def restore(self, checkpoint):
        self.done = list(checkpoint)


def test_interrupt_and_resume_without_duplicate_effects():
    r = Runtime()
    r.execute("RESEARCH")
    checkpoint = r.checkpoint()
    r.execute("WORKFLOW")
    r.restore(checkpoint)
    r.execute("WORKFLOW")
    r.execute("AGENT")
    assert r.done == ["RESEARCH", "WORKFLOW", "AGENT"]


def test_repeated_resume_is_idempotent():
    r = Runtime()
    for _ in range(3):
        r.execute("RESEARCH")
    assert r.done == ["RESEARCH"]
