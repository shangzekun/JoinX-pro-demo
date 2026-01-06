from __future__ import annotations

import random
from typing import Any, Dict, List, Tuple

from .base_agent import AgentResult, BaseAgent


class ParameterRecommendationAgent(BaseAgent):
    """Recommends SPR parameter ranges based on task context."""

    def __init__(self) -> None:
        super().__init__(
            name="ParameterRecommendationAgent",
            goal="Recommend testable parameter windows for SPR joints",
            constraints="Use rule-of-thumb ranges when data is sparse",
        )

    def run(self, context: Dict[str, Any]) -> AgentResult:
        material = context.get("material", {})
        structure = context.get("structure", {})
        target = context.get("target", "strength")

        base_thickness = material.get("sheet_thickness_mm", 1.2)
        # Simple heuristic and mock model noise
        clamp_force = (base_thickness * 3.5) + random.uniform(-0.2, 0.2)
        punch_speed = (structure.get("stack_layers", 2) * 50) + random.uniform(-5, 5)

        ranges: Dict[str, Tuple[float, float]] = {
            "clamp_force_kN": (round(clamp_force - 0.5, 2), round(clamp_force + 0.5, 2)),
            "punch_speed_mm_s": (round(punch_speed - 10, 1), round(punch_speed + 10, 1)),
            "preload_N": (1500, 2500) if target == "strength" else (1200, 1800),
        }

        priority_params: List[str] = ["clamp_force_kN", "punch_speed_mm_s"]

        return AgentResult(
            summary="Proposed parameter ranges for bench trials",
            recommended_ranges=ranges,
            priority_params=priority_params,
            assumptions=["No coating sensitivity", "Standard SPR die"],
        )
