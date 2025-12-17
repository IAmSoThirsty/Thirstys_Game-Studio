"""Agent manager for coordinating the multi-agent system.

This module provides the central manager that orchestrates task
assignment and execution across agent workers.
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

from agent.core.interfaces import AgentRole, Task, TaskResult, TaskStatus
from agent.orchestration.roles import RoleRegistry
from agent.orchestration.tasks import TaskQueue, TaskFactory
from agent.orchestration.workers import create_worker_for_role

logger = logging.getLogger(__name__)


class AgentManager:
    """Central manager for coordinating the agent team.

    Manages task assignment, worker coordination, and execution
    monitoring for the multi-agent orchestration system.

    Attributes:
        role_registry: Registry of available roles
        task_queue: Queue of tasks to execute
        workers: Dictionary of active workers
        results: Collected results from task execution
    """

    def __init__(self):
        """Initialize the agent manager."""
        self.role_registry = RoleRegistry()
        self.task_queue = TaskQueue()
        self.workers: Dict[AgentRole, Any] = {}
        self.results: List[TaskResult] = []
        self._start_time: Optional[datetime] = None
        self._end_time: Optional[datetime] = None

    def initialize_workers(self) -> None:
        """Initialize workers for all available roles."""
        for role_def in self.role_registry.get_all():
            try:
                worker = create_worker_for_role(role_def.role)
                self.workers[role_def.role] = worker
                logger.info(f"Initialized worker for role: {role_def.name}")
            except ValueError as e:
                logger.warning(f"Could not create worker: {e}")

    def add_task(self, task: Task) -> None:
        """Add a task to the queue.

        Args:
            task: Task to add
        """
        self.task_queue.add(task)

    def add_tasks(self, tasks: List[Task]) -> None:
        """Add multiple tasks to the queue.

        Args:
            tasks: Tasks to add
        """
        self.task_queue.add_all(tasks)

    def create_full_pipeline(self) -> List[Task]:
        """Create and add a full pipeline of tasks.

        Returns:
            List of created tasks
        """
        tasks = TaskFactory.create_full_pipeline()
        self.add_tasks(tasks)
        return tasks

    def execute_next(self) -> Optional[TaskResult]:
        """Execute the next available task.

        Returns:
            Result of the executed task, or None if no tasks are ready
        """
        task = self.task_queue.get_next()
        if task is None:
            return None

        logger.info(f"Executing task: {task.name}")

        # Get worker for task role
        worker = self.workers.get(task.role)
        if worker is None:
            error = f"No worker available for role: {task.role}"
            logger.error(error)
            self.task_queue.mark_failed(task.id, error)
            return TaskResult(task_id=task.id, success=False, error=error)

        # Inject dependency data into task
        dep_data = self.task_queue.get_dependency_data(task)
        task.input_data.update(dep_data)

        # Execute task
        try:
            result = worker.execute(task)
            if result.success:
                self.task_queue.mark_completed(task.id, result)
            else:
                self.task_queue.mark_failed(task.id, result.error or "Unknown error")
            self.results.append(result)
            return result
        except Exception as e:
            logger.exception(f"Task execution failed: {e}")
            self.task_queue.mark_failed(task.id, str(e))
            result = TaskResult(task_id=task.id, success=False, error=str(e))
            self.results.append(result)
            return result

    def run_all(self) -> Dict[str, Any]:
        """Run all tasks in the queue.

        Returns:
            Summary of the execution run
        """
        self._start_time = datetime.utcnow()
        logger.info("Starting agent manager run")

        while not self.task_queue.is_empty() and self.task_queue.pending_count() > 0:
            result = self.execute_next()
            if result is None:
                # No tasks ready - might have unmet dependencies
                if self.task_queue.pending_count() > 0:
                    logger.warning("Tasks remain but none are ready - possible dependency issue")
                break

        self._end_time = datetime.utcnow()

        return self.get_run_summary()

    def get_run_summary(self) -> Dict[str, Any]:
        """Get a summary of the current/completed run.

        Returns:
            Run summary dictionary
        """
        successful = sum(1 for r in self.results if r.success)
        failed = sum(1 for r in self.results if not r.success)
        total_time = sum(r.execution_time for r in self.results)

        # Get final output data
        final_data = {}
        for result in self.results:
            if result.success and result.output_data:
                # Exclude internal/raw data
                for key, value in result.output_data.items():
                    if not key.startswith("raw_"):
                        final_data[key] = value

        return {
            "timestamp": (self._start_time or datetime.utcnow()).isoformat(),
            "end_time": (self._end_time or datetime.utcnow()).isoformat(),
            "total_tasks": len(self.results),
            "successful": successful,
            "failed": failed,
            "total_execution_time": total_time,
            "queue_summary": self.task_queue.get_summary(),
            "output_data": final_data,
            "results": [r.to_dict() for r in self.results],
        }

    def reset(self) -> None:
        """Reset the manager for a new run."""
        self.task_queue = TaskQueue()
        self.results = []
        self._start_time = None
        self._end_time = None
