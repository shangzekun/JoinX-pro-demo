from __future__ import annotations

from typing import Any, Dict, Tuple

from .base_agent import AgentResult, BaseAgent


class ProcessWindowAgent(BaseAgent):
    """Creates a simplified process window visualization payload."""

    def __init__(self) -> None:
        super().__init__(
            name="ProcessWindowAgent",
            goal="Outline feasible SPR parameter space with guardrails",
            constraints="Assumes clean surfaces and calibrated equipment",
        )

    def run(self, context: Dict[str, Any]) -> AgentResult:
        recommendations: Dict[str, Tuple[float, float]] = context.get("recommended_ranges", {})
        window = {
            k: {"min": v[0], "max": v[1], "center": round((v[0] + v[1]) / 2, 2)}
            for k, v in recommendations.items()
        }
        risks = [
            "Clamp force drift may reduce joint button formation",
            "Punch speed variation impacts splash and burr",
        ]

        return AgentResult(
            summary="Process window drafted for pilot build",
            process_window=window,
            risk_highlights=risks,
        )
