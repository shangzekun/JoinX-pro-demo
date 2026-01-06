from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from ..data.store import InMemoryStore
from ..models.task import Task
from ..services.workbench import create_task
from ..workflow.spr_workflow import run_default_workflow


BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(title="JoinX Pro Demo", description="SPR agentic workflow showcase")
store = InMemoryStore()


def _list_tasks() -> List[Task]:
    return list(store.tasks.values())[::-1]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, task_id: Optional[str] = None) -> HTMLResponse:
    task = store.get_task(task_id) if task_id else None
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "task": task,
            "tasks": _list_tasks(),
        },
    )


@app.post("/run", response_class=HTMLResponse)
async def run_workflow(
    request: Request,
    material_pair: str = Form(...),
    sheet_thickness_mm: float = Form(...),
    joint_type: str = Form(...),
    stack_layers: int = Form(...),
    target: str = Form(...),
    manual_confirmation: bool = Form(False),
) -> HTMLResponse:
    material = {"material_pair": material_pair, "sheet_thickness_mm": float(sheet_thickness_mm)}
    structure = {"joint_type": joint_type, "stack_layers": int(stack_layers)}

    task = create_task(material, structure, target)
    store.save_task(task)
    run_default_workflow(task, manual_confirmation=manual_confirmation)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "task": task,
            "tasks": _list_tasks(),
        },
    )


@app.get("/tasks/{task_id}", response_class=HTMLResponse)
async def view_task(task_id: str, request: Request) -> HTMLResponse:
    task = store.get_task(task_id)
    if not task:
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "task": task, "tasks": _list_tasks()},
    )
