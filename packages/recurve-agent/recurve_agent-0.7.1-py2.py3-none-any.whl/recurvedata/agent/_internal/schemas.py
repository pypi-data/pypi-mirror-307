from __future__ import annotations

import datetime
from enum import Enum
from typing import Any, Generic, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel, Field

from .host import HostInfo, HostMetrics
from .utils import utcnow

T = TypeVar("T")


class RecurveEnum(str, Enum):
    """Base Enum class for Recurve."""

    def __str__(self) -> str:
        return str.__str__(self)


class ServiceStatusInfo(BaseModel):
    container_name: str
    status: str


class AgentHostInfo(BaseModel):
    ip_address: str
    hostname: str
    agent_version: str
    host_info: HostInfo


class LoginPayload(AgentHostInfo):
    tenant_domain: str
    agent_id: UUID
    auth_token: str


class Heartbeat(BaseModel):
    agent_id: UUID
    metrics: HostMetrics
    sent_time: datetime.datetime = Field(default_factory=utcnow)
    service_status: list[ServiceStatusInfo] = Field(default_factory=list)


class Pagination(BaseModel, Generic[T]):
    total: int
    items: list[T]


class TaskItem(BaseModel):
    task_instance_id: int
    agent_id: UUID
    queue: str
    max_retries: int
    max_duration: int
    handler_code: str  # base64 encoded content of the handler file
    handler_format: str  # format of the handler file, either "py" or "zip"
    payload: dict  # payload for the task, will be passed to the handler in JSON format


class TaskStatus(RecurveEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class UpdateTaskInstanceStatus(BaseModel):
    status: TaskStatus
    logs: Optional[list[str]] = None
    result: Optional[dict[str, Any]] = None
    error: Optional[dict[str, str]] = None
