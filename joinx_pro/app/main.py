from __future__ import annotations

import argparse
import json

from .models.task import Task
from .services.workbench import run_demo


def print_task_summary(task: Task) -> None:
    print("=== JoinX Pro | SPR Workflow Summary ===")
    print(f"Task ID: {task.id}")
    print(f"Target: {task.target}")
    print(f"Status: {task.status}")
    print("--- Logs ---")
    for entry in task.logs:
        print(json.dumps(entry, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="JoinX Pro Demo")
    parser.add_argument("--demo", action="store_true", help="Run demo workflow with sample data")
    parser.add_argument(
        "--manual-confirmation",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Automatically approve manual steps",
    )
    args = parser.parse_args()

    if args.demo:
        task = run_demo(manual_confirmation=bool(args.manual_confirmation))
        print_task_summary(task)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
