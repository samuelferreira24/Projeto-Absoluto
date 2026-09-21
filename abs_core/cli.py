import argparse
import os
from .adapters import EchoCapability
from .capabilities import CapabilityRecord, CapabilityRegistry
from .orchestrator import Orchestrator
from .store import WorkStore
from .continuity import OperationalContinuity


def build():
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("echo", "Echo test capability", "test", EchoCapability()))
    try:
        from .codex_adapter import CodexCapability
        registry.register(CapabilityRecord("codex", "OpenAI Codex CLI", "external_ai", CodexCapability()))
    except Exception:
        pass
    db_path = os.getenv("ABS_DB_PATH", "abs.db")
    store = WorkStore(db_path)
    store.recover_interrupted()
    return Orchestrator(registry, store)


def main():
    parser = argparse.ArgumentParser(description="ABS capability foundation")
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create")
    create.add_argument("objective")

    continuity = sub.add_parser("continuity")
    continuity.add_argument("action", choices=("checkpoint", "verify"))

    run = sub.add_parser("run")
    run.add_argument("work_id")
    run.add_argument("--capability", default=None)
    run.add_argument("--approved", action="store_true")

    args = parser.parse_args()
    orch = build()

    if args.command == "continuity":
        manager = OperationalContinuity(orch.store.path)
        print(manager.checkpoint() if args.action == "checkpoint" else manager.verify())
        return

    if args.command == "create":
        print(orch.create(args.objective).id)
    else:
        work = orch.run(
            args.work_id,
            args.capability,
            approved=args.approved,
        )
        print(work.result)


if __name__ == "__main__":
    main()
