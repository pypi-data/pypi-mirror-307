from typing import Dict
from uuid import UUID

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import JSONResponse

from agenticos.connectors import BaseWorkflowConfig
from agenticos.node.models import AgenticConfig, Job, JobStatus, Workflow

jobs: dict[UUID, Job] = {}
pw: dict[str, Workflow] = {}
workflows: dict[str, BaseWorkflowConfig] = {}

app = FastAPI()


def run_job(workflow: BaseWorkflowConfig, job: Job) -> None:
    try:
        runner = workflow.new_runner()
        runner.start(job.inputs)
        for step in runner.step_output():
            job.output = step
        job.status = JobStatus.COMPLETED
    except Exception as e:
        job.output = str(e)
        job.status = JobStatus.FAILED


def create_server(config: AgenticConfig) -> FastAPI:
    global pw, workflows
    workflows = config.workflows
    for k, v in workflows.items():
        pw[k] = Workflow(name=k, description=v.description(), inputs=v.inputs())
    return app


@app.get(
    "/node/description",
    summary="Get the description of the node",
    response_model=dict[str, Workflow],
)
def description() -> dict[str, Workflow]:
    return pw


@app.post("/workflow/{workflow_name}/run")
async def run(
    workflow_name: str, inputs: dict[str, str], background_tasks: BackgroundTasks
) -> str:
    if workflow_name not in workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    job = Job(inputs=inputs, status=JobStatus.RUNNING, output="")
    jobs[job.id] = job
    background_tasks.add_task(run_job, workflows[workflow_name], job)
    return str(job.id)


@app.get("/job/{job_id}")
def get_job(job_id: str) -> Job:
    if UUID(job_id) not in jobs:
        raise HTTPException(status_code=404, detail="Task not found")
    return jobs[UUID(job_id)]


@app.get("/jobs")
def get_jobs() -> list[str]:
    return [str(tk) for tk in jobs.keys()]


@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})
