from __future__ import annotations

import abc
from typing import Any, Dict, Optional


class AgentResult(Dict[str, Any]):
    """Container for agent outputs with convenience helpers."""

    summary: str

    def __getattr__(self, item: str) -> Any:  # pragma: no cover - passthrough helper
        try:
            return self[item]
        except KeyError:
            raise AttributeError(item)


class BaseAgent(abc.ABC):
    """Base class defining the contract for all agents.

    Agents encapsulate a specific engineering responsibility. Models or rules may
    be used internally, but agents own the orchestration logic and produce a
    structured result for downstream workflow steps.
    """

    name: str
    goal: str
    constraints: str

    def __init__(self, name: str, goal: str, constraints: Optional[str] = None) -> None:
        self.name = name
        self.goal = goal
        self.constraints = constraints or ""

    @abc.abstractmethod
    def run(self, context: Dict[str, Any]) -> AgentResult:
        """Execute agent logic with the provided workflow context."""

    def describe(self) -> str:
        return f"Agent<{self.name}>: {self.goal}"
