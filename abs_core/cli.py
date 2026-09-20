import argparse
from .adapters import EchoCapability
from .capabilities import CapabilityRecord, CapabilityRegistry
from .orchestrator import Orchestrator
from .store import WorkStore

def build():
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("echo", "Echo test capability", "test", EchoCapability()))
    return Orchestrator(registry, WorkStore("abs.db"))

def main():
    parser = argparse.ArgumentParser(description="ABS capability foundation")
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("create"); create.add_argument("objective")
    run = sub.add_parser("run"); run.add_argument("work_id"); run.add_argument("--capability", default=None)
    args = parser.parse_args(); orch = build()
    if args.command == "create": print(orch.create(args.objective).id)
    else: print(orch.run(args.work_id, args.capability).result)

if __name__ == "__main__": main()
