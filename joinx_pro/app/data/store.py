from __future__ import annotations

from typing import Dict, Optional

from ..models.task import Task


class InMemoryStore:
    """Simplified data holder for tasks and workflow state."""

    def __init__(self) -> None:
        self.tasks: Dict[str, Task] = {}

    def save_task(self, task: Task) -> None:
        self.tasks[task.id] = task

    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)
