from __future__ import annotations

from typing import List

from ..agents.parameter_recommendation_agent import ParameterRecommendationAgent
from ..agents.process_window_agent import ProcessWindowAgent
from ..agents.risk_evaluation_agent import RiskEvaluationAgent
from ..models.task import Task
from .workflow_engine import WorkflowEngine, WorkflowStep


def create_spr_workflow() -> WorkflowEngine:
    steps: List[WorkflowStep] = [
        WorkflowStep(name="ParameterRecommendation", agent=ParameterRecommendationAgent()),
        WorkflowStep(
            name="ProcessWindow",
            agent=ProcessWindowAgent(),
            condition=lambda ctx: "recommended_ranges" in ctx,
        ),
        WorkflowStep(
            name="RiskEvaluation",
            agent=RiskEvaluationAgent(),
            condition=lambda ctx: "process_window" in ctx,
        ),
        WorkflowStep(
            name="ManualConfirm",
            manual_confirmation_required=True,
            condition=lambda ctx: ctx.get("risk_level") == "HIGH",
        ),
        WorkflowStep(name="FinalizeProcessPlan"),
    ]
    return WorkflowEngine(steps)


def run_default_workflow(task: Task, manual_confirmation: bool = True) -> Task:
    engine = create_spr_workflow()
    engine.run(task, manual_confirmation=manual_confirmation)
    return task
