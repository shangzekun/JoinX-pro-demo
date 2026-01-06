from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Task:
    """Represents a SPR process development task."""

    id: str
    material: Dict[str, Any]
    structure: Dict[str, Any]
    target: str
    status: str = "CREATED"
    workflow_stage: str = "INIT"
    logs: List[Dict[str, Any]] = field(default_factory=list)

    def add_log(self, entry: Dict[str, Any]) -> None:
        self.logs.append(entry)
