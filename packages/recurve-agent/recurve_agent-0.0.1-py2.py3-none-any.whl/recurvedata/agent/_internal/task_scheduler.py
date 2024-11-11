import asyncio
from typing import TYPE_CHECKING

from loguru import logger

from ..exceptions import UnauthorizedError
from .task_executor import TaskExecutor

if TYPE_CHECKING:
    from .agent import Agent


class TaskScheduler:
    def __init__(self, agent: "Agent"):
        self.agent = agent
        self.task_executor = TaskExecutor(agent.client)

        self._last_schedule_failed = False

    async def get_and_dispatch_tasks(self):
        try:
            paged_tasks = await self.agent.client.get_pending_tasks(agent_id=self.agent.id)
            if self._last_schedule_failed:
                logger.info("Connection to server is restored.")
                self._last_schedule_failed = False

            if paged_tasks.total > 0:
                logger.info(f"Got {paged_tasks.total} pending tasks, sending them to executor.")
            for task in paged_tasks.items:
                # fire and forget, let the task executor handle the task
                asyncio.create_task(self.task_executor.execute(task))
        except UnauthorizedError as e:
            raise e
        except Exception as e:
            logger.error(f"Failed to get pending tasks: {e}")
            self._last_schedule_failed = True
