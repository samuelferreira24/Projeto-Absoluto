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
    for module_name, class_name, capability_id, name, kind, env_name in (
        (".ai_adapters", "ClaudeCapability", "claude", "Anthropic Claude API", "external_ai", "ANTHROPIC_API_KEY"),
        (".ai_adapters", "GeminiCapability", "gemini", "Google Gemini API", "external_ai", "GEMINI_API_KEY"),
        (".openai_adapter", "OpenAICapability", "openai-api", "OpenAI API", "external_ai", "OPENAI_API_KEY"),
    ):
        if os.getenv(env_name):
            try:
                module = __import__(module_name, package=__package__, fromlist=[class_name])
                capability = getattr(module, class_name)()
                registry.register(CapabilityRecord(capability_id, name, kind, capability))
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
