import json
import logging
import time
from typing import Type
from uuid import UUID

import requests
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, stop_after_delay, wait_fixed

from agenticos.node.models import Job, JobStatus, Workflow
from agenticos.node.settings import settings

log = logging.getLogger(__name__)
# Round robin counter for selecting the host
host_ord: int = 0
session: requests.Session = requests.Session()


class PlaceHolderSchema(BaseModel): ...


class DirectAgenticNodeTool(BaseTool):
    node_urls: list[str] = ["http://localhost:8000"]
    workflow: str = "research"
    name: str = ""
    description: str = ""
    args_schema: Type[BaseModel] = PlaceHolderSchema

    def __init__(self, node_urls: str | list[str], **kwargs) -> None:
        """DirectAgenticNodeTool constructor
        Keyword arguments:
        node_urls -- The URL of the node (str) or a list of URLs (list[str])
        workflow -- The workflow to run
        timeout -- The timeout for the job
        """
        try:
            if isinstance(node_urls, str):
                node_urls = [node_urls]
            args_schema, name, description = self.query_workflow(
                node_url=node_urls[0], workflow=kwargs["workflow"]
            )
            kwargs["node_urls"] = node_urls
            kwargs["name"] = name
            kwargs["description"] = description
            kwargs["args_schema"] = args_schema
        except Exception as e:
            log.error(f"Failed to properly initialize DirectAgenticNodeTool {e}")

        super().__init__(**kwargs)

    def _run(self, **kwargs) -> str:
        return self._do_run(**kwargs)

    @retry(stop=stop_after_attempt(3))
    def _do_run(self, **kwargs) -> str:
        global host_ord
        # Round robin selection of host
        host_ord = (host_ord + 1) % len(self.node_urls)
        # post the argument as request body to the node_url
        url = self.node_urls[host_ord]
        res = requests.post(f"{url}/workflow/{self.workflow}/run", json=kwargs)
        tid = res.text.strip('"')

        for _ in range(0, 30):
            res = requests.get(f"{url}/job/{tid}")
            job = Job.model_validate_json(res.text)
            if job.status != JobStatus.RUNNING:
                return job.output or ""
            time.sleep(1)
        log.error("Job took too long to complete")
        raise Exception("Job took too long to complete")

    @retry(stop=stop_after_delay(30), wait=wait_fixed(2))
    def query_workflow(
        self, node_url: str, workflow: str
    ) -> tuple[Type[BaseModel], str, str]:
        try:
            if isinstance(node_url, list):
                node_url = node_url[0]
            res = requests.get(f"{node_url}/node/description")
            if res.status_code != 200:
                raise Exception("Failed to get node description")
            wfs = json.loads(res.text)
            wf = Workflow(**wfs[workflow])

            fields = {k: Field(..., description=v) for k, v in wf.inputs.items()}
            fields["__annotations__"] = {k: str for k in wf.inputs.keys()}

            Schema = type(
                "AgenticToolSchema",
                (BaseModel,),
                fields,
            )

            return Schema, wf.name, wf.description
        except Exception as e:
            log.warning(f"Failed to query workflow: {e}")
            raise Exception(f"Failed to query workflow: {e}")


class RegistryAgenticNodeTool(BaseTool):
    node_ids: list[UUID] = [UUID("00000000-0000-0000-0000-000000000000")]
    workflow: str = "research"
    name: str = ""
    description: str = ""
    args_schema: Type[BaseModel] = PlaceHolderSchema

    def __init__(self, node_ids: UUID | list[UUID], **kwargs) -> None:
        """DirectAgenticNodeTool constructor
        Keyword arguments:
        node_ids -- The ID of the node (UUID) or a list of IDs (list[UUID])
        workflow -- The workflow to run
        timeout -- The timeout for the job
        When connecting to the registry it also requires following environment variables:
        REGISTRY_URL, BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD
        """
        try:
            if settings.has_basic_auth():
                session.auth = (
                    settings.BASIC_AUTH_USERNAME,
                    settings.BASIC_AUTH_PASSWORD,
                )
            if isinstance(node_ids, UUID):
                node_ids = [node_ids]
            args_schema, name, description = self.query_workflow(
                node_id=str(node_ids[0]), workflow=kwargs["workflow"]
            )
            kwargs["node_ids"] = node_ids
            kwargs["name"] = name
            kwargs["description"] = description
            kwargs["args_schema"] = args_schema
        except Exception as e:
            log.error(f"Failed to properly initialize DirectAgenticNodeTool {e}")

        super().__init__(**kwargs)

    def _run(self, **kwargs) -> str:
        return self._do_run(**kwargs)

    @retry(stop=stop_after_attempt(3))
    def _do_run(self, **kwargs) -> str:
        global host_ord
        # Round robin selection of host
        host_ord = (host_ord + 1) % len(self.node_ids)
        # post the argument as request body to the node_url
        node_id = self.node_ids[host_ord]
        body = {"workflow": self.workflow, "inputs": kwargs, "node_id": str(node_id)}
        res = session.post(f"{settings.registry_rest_url()}/api/v1/jobs", json=body)
        if res.status_code != 200:
            raise Exception("Failed to start job")
        tid = res.text.strip('"')

        for _ in range(0, 30):
            res = session.get(f"{settings.registry_rest_url()}/api/v1/jobs/{tid}")
            log.info(f"Response: {res.text}")
            job = res.json()
            log.info(f"Job: {job}")
            if job["status"] != JobStatus.RUNNING:
                return job["result"] or ""
            time.sleep(1)
        log.error("Job took too long to complete")
        raise Exception("Job took too long to complete")

    @retry(stop=stop_after_delay(30), wait=wait_fixed(2))
    def query_workflow(
        self, node_id: str, workflow: str
    ) -> tuple[Type[BaseModel], str, str]:
        try:
            if isinstance(node_id, list):
                node_id = node_id[0]
            res = session.get(
                f"{settings.registry_rest_url()}/api/v1/nodes/{node_id}",
            )
            if res.status_code != 200:
                raise Exception(
                    f"Failed to fetch node description with status code {res.status_code}"
                )
            wfs = json.loads(res.text)["workflows"]
            wf = Workflow(**wfs[workflow])

            fields = {k: Field(..., description=v) for k, v in wf.inputs.items()}
            fields["__annotations__"] = {k: str for k in wf.inputs.keys()}

            Schema = type(
                "AgenticToolSchema",
                (BaseModel,),
                fields,
            )

            return Schema, wf.name, wf.description
        except Exception as e:
            log.warning(f"Failed to query workflow: {e}")
            raise Exception(f"Failed to query workflow: {e}")
