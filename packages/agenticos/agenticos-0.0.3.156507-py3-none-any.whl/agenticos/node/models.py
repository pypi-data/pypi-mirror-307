from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable, Dict, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from agenticos.connectors.base import BaseWorkflowConfig

MSG_HS_NODE = "MSG_HS_NODE"
MSG_HS_ACK = "MSG_HS_ACK"
MSG_JOB_REQ = "MSG_JOB_REQ"
MSG_JOB_FIN = "MSG_JOB_FIN"
MSG_STEP_FIN = "MSG_STEP_FIN"
MSG_HEARTBEAT = "MSG_HEARTBEAT"

class Workflow(BaseModel):
    name: str
    description: str
    inputs: Dict[str, str]

class JobStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AgenticConfig:
    def __init__(self, name: str, workflows: Dict[str, BaseWorkflowConfig]):
        self.name = name
        self.workflows = workflows

    id: Optional[UUID] = None
    name: str
    workflows: Dict[str, BaseWorkflowConfig] = {}

    def model_dump(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "workflows": {k: v.model_dump(k) for k, v in self.workflows.items()},
        }


class Job(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    inputs: Dict[str, str]
    status: JobStatus = Field()
    output: str | None


class WrongFolderError(Exception):
    pass


class AgenticMessage(BaseModel):
    type: str


class AgenticHandshakeMessage(AgenticMessage):
    type: str = MSG_HS_NODE
    node: str


class JobFinishedMessage(AgenticMessage):
    type: str = MSG_JOB_FIN
    job_id: str
    status: JobStatus
    result: str | None


class StepFinishedMessage(AgenticMessage):
    type: str = MSG_STEP_FIN
    job_id: str
    step: int
    result: str


class JobRequest(BaseModel):
    workflow: str
    inputs: Dict[str, str]
    job_id: UUID = Field(default_factory=uuid4)
    node_id: str


class AgenticJobRequestMessage(BaseModel):
    type: str = MSG_JOB_REQ
    job: JobRequest
