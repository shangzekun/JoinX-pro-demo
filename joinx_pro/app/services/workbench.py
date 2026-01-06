from __future__ import annotations

import uuid
from typing import Any, Dict, Optional

from ..data.store import InMemoryStore
from ..models.task import Task
from ..workflow.spr_workflow import run_default_workflow


def create_task(material: Dict[str, Any], structure: Dict[str, Any], target: str) -> Task:
    return Task(
        id=str(uuid.uuid4()),
        material=material,
        structure=structure,
        target=target,
    )


def execute_workflow(
    material: Dict[str, Any],
    structure: Dict[str, Any],
    target: str,
    store: Optional[InMemoryStore] = None,
    manual_confirmation: bool = True,
) -> Task:
    data_store = store or InMemoryStore()
    task = create_task(material, structure, target)
    data_store.save_task(task)
    run_default_workflow(task, manual_confirmation=manual_confirmation)
    return task


def run_demo(manual_confirmation: bool = True) -> Task:
    material = {"material_pair": "Al/Steel", "sheet_thickness_mm": 1.5}
    structure = {"joint_type": "SPR", "stack_layers": 2}
    target = "strength"

    return execute_workflow(
        material=material,
        structure=structure,
        target=target,
        manual_confirmation=manual_confirmation,
    )
