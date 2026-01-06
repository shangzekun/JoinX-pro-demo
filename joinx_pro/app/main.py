from __future__ import annotations

import argparse
import json
import uuid
from typing import Any, Dict

from .data.store import InMemoryStore
from .models.task import Task
from .workflow.spr_workflow import run_default_workflow


def create_task(material: Dict[str, Any], structure: Dict[str, Any], target: str) -> Task:
    return Task(
        id=str(uuid.uuid4()),
        material=material,
        structure=structure,
        target=target,
    )


def run_demo(manual_confirmation: bool = True) -> Task:
    material = {"material_pair": "Al/Steel", "sheet_thickness_mm": 1.5}
    structure = {"joint_type": "SPR", "stack_layers": 2}
    target = "strength"

    task = create_task(material, structure, target)
    store = InMemoryStore()
    store.save_task(task)

    run_default_workflow(task, manual_confirmation=manual_confirmation)
    return task


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
