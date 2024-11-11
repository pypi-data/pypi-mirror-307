from functools import partial
from uuid import UUID

import anyio
from loguru import logger
from typing_extensions import Self

from .._internal.task_scheduler import TaskScheduler
from .._version import VERSION
from ..config import CONFIG, AgentConfig
from ..exceptions import UnauthorizedError
from . import host, worker
from .client import AgentClient
from .schemas import AgentHostInfo, Heartbeat, LoginPayload
from .service_loop import critical_service_loop


class Agent:
    _config: AgentConfig
    client: AgentClient

    def __init__(self, config: AgentConfig):
        self.set_config(config)

    @classmethod
    def default(cls) -> Self:
        return cls(CONFIG)

    @classmethod
    def from_config_file(cls, filename: str) -> Self:
        config = AgentConfig.load(filename)
        return cls(config)

    @property
    def config(self) -> AgentConfig:
        return self._config

    def set_config(self, value: AgentConfig):
        self._config = value
        self.client = AgentClient(value)

    @property
    def id(self) -> UUID:
        return self.config.agent_id

    @property
    def has_logged_in(self) -> bool:
        return self.config.is_valid() and self.config.logged_in

    async def login(self, encoded_token: str):
        self.config.set_auth_token(encoded_token)
        # update the client with the new config (server_url and token)
        self.client.set_config(self.config)

        hostname, ip_address = host.get_hostname_ip()
        await self.client.login(
            LoginPayload(
                tenant_domain=self.config.tenant_domain,
                agent_id=self.id,
                auth_token=self.config.token.get_secret_value(),
                hostname=hostname,
                ip_address=ip_address,
                agent_version=VERSION,
                host_info=host.get_host_info(),
            )
        )
        self.config.logged_in = True
        self.config.save()

    async def report_host_info(self):
        hostname, ip_address = host.get_hostname_ip()
        payload = AgentHostInfo(
            hostname=hostname,
            ip_address=ip_address,
            agent_version=VERSION,
            host_info=host.get_host_info(),
        )
        await self.client.report_host_info(payload)

    async def logout(self):
        await self.client.logout(agent_id=self.id)
        self.config.clear_auth_token()
        self.config.logged_in = False
        self.client.set_config(self.config)
        self.config.save()

    async def send_heartbeat(self):
        path = worker.get_docker_root_dir()
        payload = Heartbeat(
            agent_id=self.id,
            metrics=host.get_host_metrics(path=path),
            service_status=worker.get_service_status(),
        )
        await self.client.heartbeat(payload)

    async def sync_with_server(self):
        try:
            await self.send_heartbeat()
        except UnauthorizedError as e:
            raise e
        except Exception as e:
            logger.error(f"Failed to sync with server: {e}")

    async def start(self):
        async with anyio.create_task_group() as tg:
            # wait for an initial heartbeat to configure the worker
            await self.sync_with_server()

            logger.info("Start sending heartbeats.")
            tg.start_soon(
                partial(
                    critical_service_loop,
                    workload=self.sync_with_server,
                    interval=self.config.heartbeat_interval,
                    printer=logger.info,
                    jitter_range=0.3,
                    backoff=4,
                )
            )

            logger.info("Start polling for new tasks.")
            scheduler = TaskScheduler(self)
            tg.start_soon(
                partial(
                    critical_service_loop,
                    workload=scheduler.get_and_dispatch_tasks,
                    interval=self.config.poll_interval,
                    printer=logger.info,
                    backoff=4,
                )
            )
