from __future__ import annotations

import asyncio
from typing import Any, TypeVar, overload
from uuid import UUID

import httpx
from loguru import logger
from pydantic import BaseModel

from .._version import VERSION
from ..config import AgentConfig
from ..exceptions import APIError, MaxRetriesExceededException, UnauthorizedError
from .schemas import AgentHostInfo, Heartbeat, LoginPayload, Pagination, TaskItem, UpdateTaskInstanceStatus

ResponseModelType = TypeVar("ResponseModelType", bound=BaseModel)


class AgentClient:
    _config: AgentConfig
    _client: httpx.AsyncClient

    def __init__(self, config: AgentConfig):
        self.set_config(config)

    def set_config(self, config: AgentConfig):
        self._config = config
        self._client = httpx.AsyncClient(
            base_url=config.server_url,
            timeout=config.request_timeout,
            headers={"User-Agent": f"RecurveAgent/{VERSION}"},
        )

    @overload
    async def request(
        self, method: str, path: str, response_model_class: None = None, retries: int = 3, **kwargs
    ) -> Any:
        ...

    @overload
    async def request(
        self, method: str, path: str, response_model_class: type[ResponseModelType], retries: int = 3, **kwargs
    ) -> ResponseModelType:
        ...

    async def request(
        self,
        method: str,
        path: str,
        response_model_class: type[ResponseModelType] | None = None,
        retries: int = 1,
        **kwargs,
    ) -> Any:
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self._config.agent_id}:{self._config.token.get_secret_value()}"
        headers["X-Tenant-Domain"] = self._config.tenant_domain
        kwargs["headers"] = headers

        for attempt in range(retries):
            try:
                resp = await self._client.request(method, path, **kwargs)
                duration = resp.elapsed.total_seconds() * 1000
                logger.debug(f"[{method}] {resp.url} ({resp.status_code}), elapsed: {duration:.2f}ms, {kwargs}")

                resp.raise_for_status()
                resp_content = resp.json()

                # TODO(yangliang): handle errors more gracefully
                if resp_content["code"] != "0":
                    raise APIError(f"API request failed: {resp_content['msg']}")

                if response_model_class is not None:
                    return response_model_class.model_validate(resp_content["data"])
                return resp_content["data"]
            except httpx.HTTPStatusError as e:
                logger.debug(
                    f"HTTP error on attempt {attempt + 1} for url '{e.request.url}' :"
                    f" {e.response.status_code} - {e.response.text}"
                )
                if e.response.status_code == 401:
                    raise UnauthorizedError("Unauthorized, please check your agent_id and token")
            except httpx.RequestError as e:
                logger.debug(f"Request error on attempt {attempt + 1} for url '{e.request.url}': {e}")

            if attempt < retries - 1:
                await asyncio.sleep(2**attempt)  # Exponential backoff
            else:
                raise MaxRetriesExceededException(
                    f"Failed to complete {method} request to {path} after {retries} attempts"
                )

    async def close(self):
        await self._client.aclose()

    async def healthcheck(self):
        return await self.request("GET", "/api/health")

    async def login(self, payload: "LoginPayload"):
        resp = await self._client.post("/api/agents/login", json=payload.model_dump(mode="json"))
        if resp.status_code == 401:
            raise UnauthorizedError("Unauthorized, please check your agent_id and token")
        resp.raise_for_status()

        # temporary solution
        resp_content = resp.json()
        if resp_content["code"] != "0":
            raise APIError(f"API request failed: {resp_content['msg']}")

    async def logout(self, agent_id: UUID):
        await self.request("POST", "/api/agents/logout", params={"agent_id": agent_id})

    async def report_host_info(self, payload: "AgentHostInfo"):
        await self.request("POST", "/api/agents/report-host-info", json=payload.model_dump(mode="json"))

    async def heartbeat(self, payload: "Heartbeat"):
        await self.request(
            "POST",
            "/api/agents/heartbeat",
            json=payload.model_dump(mode="json"),
            retries=3,
        )

    async def get_pending_tasks(self, agent_id: UUID) -> Pagination[TaskItem]:
        result = await self.request(
            method="GET",
            path="/api/tasks/pending",
            params={"agent_id": agent_id},
            response_model_class=Pagination[TaskItem],
        )
        return result

    async def update_task_status(self, task_instance_id: int, payload: UpdateTaskInstanceStatus):
        await self.request(
            method="POST",
            path=f"/api/tasks/{task_instance_id}/status",
            json=payload.model_dump(mode="json"),
            retries=3,
        )
