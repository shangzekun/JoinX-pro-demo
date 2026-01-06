# JoinX Pro – Intelligent Connection Process Development Platform (Demo)

JoinX Pro is an engineering-oriented demo that frames self-piercing rivet (SPR) process
engineering as **agents + agentic workflows** instead of a single model invocation.
The goal is to keep agent responsibilities explicit, make workflow decisions auditable,
and provide a minimal runnable skeleton that can be extended with real models and data.

## Architecture Overview

- **Agents** – The smallest capability unit. Each agent owns a goal, contextual inputs,
  constraints, reasoning strategy, and produces structured outputs. Models may be used
  internally but never directly exposed to users.
- **Workflow Engine** – Drives the multi-stage process development lifecycle, enabling
  sequential execution, conditional branching, and manual confirmation gates. All
  intermediate results are logged for traceability.
- **Data & State** – In-memory task store holding task metadata and workflow logs. Can
  be swapped for JSON/DB storage later.
- **Workbench (CLI) & Web UI** – Minimal CLI plus FastAPI web page to create a task,
  execute the SPR workflow, and display agent outputs.

```
joinx_pro/
├─ app/
│  ├─ agents/
│  │  ├─ base_agent.py                # Agent contract + AgentResult helper
│  │  ├─ parameter_recommendation_agent.py
│  │  ├─ process_window_agent.py
│  │  └─ risk_evaluation_agent.py
│  ├─ workflow/
│  │  ├─ workflow_engine.py           # Sequential executor with branching + manual gate
│  │  └─ spr_workflow.py              # SPR-specific workflow definition
│  ├─ models/
│  │  └─ task.py                      # Task entity + logs
│  ├─ data/
│  │  └─ store.py                     # In-memory storage abstraction
│  ├─ api/
│  │  ├─ server.py                    # FastAPI app serving a simple web UI
│  │  └─ templates/
│  │     └─ index.html                # Single-page workflow viewer
│  └─ main.py                         # CLI entrypoint / workbench
├─ README.md
└─ requirements.txt
```

## Modules and Responsibilities

### Agents
- **BaseAgent / AgentResult**: Defines the agent contract and a lightweight result
  container with attribute access.
- **ParameterRecommendationAgent**: Generates recommended parameter ranges using
  heuristics plus mock model noise. Outputs `recommended_ranges`, `priority_params`,
  and key assumptions.
- **ProcessWindowAgent**: Builds a simplified process window payload from the recommended
  ranges and highlights operational risks.
- **RiskEvaluationAgent**: Assigns a coarse risk level (LOW/MEDIUM/HIGH) based on window
  spread and variability.

### Workflow
- **WorkflowEngine**: Executes `WorkflowStep` items in order, supports conditional
  execution, and optional manual confirmation steps. Each step appends a log entry to the
  task for traceability.
- **SPR Workflow (`spr_workflow.py`)**: Encapsulates the demo workflow:
  1. `ParameterRecommendation`
  2. `ProcessWindow` (runs only if recommendations exist)
  3. `RiskEvaluation` (runs only if a process window exists)
  4. `ManualConfirm` (required when risk is HIGH)
  5. `FinalizeProcessPlan`

### Data & State
- **Task**: Minimal representation of a process development task including material,
  structure, target, workflow stage, and execution logs.
- **InMemoryStore**: Tiny placeholder for persistence; replace with JSON/DB as needed.

### Workbench (CLI)
`joinx_pro/app/main.py` exposes a CLI to run the demo workflow with sample inputs and view
agent outputs. `joinx_pro/app/api/server.py` serves a minimal web UI to trigger workflow
runs and visualize agent outputs in the browser.

## Running the Demo

> Requires Python 3.10+; no external dependencies are needed for the CLI demo.

### CLI (unchanged)

```bash
python -m joinx_pro.app.main --demo
```

Optional flags:
- `--manual-confirmation` / `--no-manual-confirmation`: simulate whether manual steps are
  auto-approved when high risk is detected.

### Web UI

```bash
pip install -r requirements.txt
uvicorn joinx_pro.app.api.server:app --reload --port 8000
```

Open http://localhost:8000 to:
- submit material/structure/target inputs
- toggle auto/manual confirmation for HIGH-risk branches
- inspect per-step agent outputs and workflow logs

## Extending the Demo

- Swap the `InMemoryStore` with a persistence layer (JSON, SQLite, etc.).
- Replace mock logic inside agents with calibrated models or rules while keeping the
  agent contracts stable.
- Introduce additional workflow branches (e.g., re-run recommendations if risk stays
  HIGH) or human-in-the-loop review steps.

## Notes

- The demo intentionally keeps data synthetic; it focuses on clean separation between
  agents and the workflow that orchestrates them.
- Key decisions and intermediate outputs are logged on the `Task` object for
  traceability and auditability.
