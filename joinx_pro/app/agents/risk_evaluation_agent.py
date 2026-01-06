from __future__ import annotations

import random
from typing import Any, Dict

from .base_agent import AgentResult, BaseAgent


class RiskEvaluationAgent(BaseAgent):
    """Assigns a coarse risk level to the proposed process plan."""

    def __init__(self) -> None:
        super().__init__(
            name="RiskEvaluationAgent",
            goal="Quantify execution risk before releasing plan",
            constraints="Only uses heuristics; not validated for launch decisions",
        )

    def run(self, context: Dict[str, Any]) -> AgentResult:
        window = context.get("process_window", {})
        variability = context.get("variability", 0.1)

        spread = sum(abs(v["max"] - v["min"]) for v in window.values()) or 1
        noise = random.uniform(0, variability)
        score = spread * (1 + noise)

        if score > 50:
            level = "HIGH"
        elif score > 25:
            level = "MEDIUM"
        else:
            level = "LOW"

        rationale = "High parameter spread" if level == "HIGH" else "Within pilot tolerance"

        return AgentResult(
            summary="Risk evaluated for release",
            risk_level=level,
            rationale=rationale,
        )
