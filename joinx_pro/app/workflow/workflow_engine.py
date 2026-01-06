from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from ..agents.base_agent import BaseAgent
from ..models.task import Task


@dataclass
class WorkflowStep:
    name: str
    agent: Optional[BaseAgent] = None
    condition: Optional[Callable[[Dict[str, Any]], bool]] = None
    manual_confirmation_required: bool = False


class WorkflowEngine:
    """Simple workflow executor supporting sequential steps and branching."""

    def __init__(self, steps: List[WorkflowStep]) -> None:
        self.steps = steps

    def run(self, task: Task, manual_confirmation: bool = True) -> Dict[str, Any]:
        context: Dict[str, Any] = {
            "task_id": task.id,
            "material": task.material,
            "structure": task.structure,
            "target": task.target,
        }

        for step in self.steps:
            if step.condition and not step.condition(context):
                task.add_log({"step": step.name, "status": "SKIPPED"})
                continue

            if step.manual_confirmation_required and not manual_confirmation:
                task.add_log({
                    "step": step.name,
                    "status": "AWAITING_CONFIRMATION",
                    "detail": "Manual confirmation required",
                })
                break

            if step.agent:
                result = step.agent.run(context)
                context.update(result)
                task.add_log({"step": step.name, "status": "COMPLETED", "result": result})
                task.workflow_stage = step.name
            else:
                task.add_log({"step": step.name, "status": "COMPLETED"})

        task.status = "COMPLETED"
        return context
