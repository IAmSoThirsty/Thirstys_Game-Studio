"""Task definitions and factory for the orchestration system.

This module provides task creation and queue management for
the multi-agent orchestration system.
"""

import logging
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Iterator
from queue import PriorityQueue

from agent.core.interfaces import AgentRole, Task, TaskStatus, TaskResult

logger = logging.getLogger(__name__)


class TaskFactory:
    """Factory for creating standardized tasks.

    Creates tasks with appropriate defaults and configurations
    for different agent roles.
    """

    @staticmethod
    def create_task(
        name: str,
        description: str,
        role: AgentRole,
        input_data: Optional[Dict[str, Any]] = None,
        dependencies: Optional[List[str]] = None,
    ) -> Task:
        """Create a new task.

        Args:
            name: Task name
            description: Task description
            role: Required agent role
            input_data: Input data for the task
            dependencies: Task IDs that must complete first

        Returns:
            New Task instance
        """
        return Task(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            role=role,
            input_data=input_data or {},
            dependencies=dependencies or [],
        )

    @staticmethod
    def create_community_analysis_task(
        sources: Optional[List[str]] = None,
        limit: int = 50,
    ) -> Task:
        """Create a community analysis task.

        Args:
            sources: List of sources to analyze
            limit: Maximum insights per source

        Returns:
            Community analysis task
        """
        return TaskFactory.create_task(
            name="Community Analysis",
            description="Fetch and analyze community insights from all sources",
            role=AgentRole.COMMUNITY_ANALYST,
            input_data={
                "sources": sources or ["reddit", "discord", "steam"],
                "limit_per_source": limit,
            },
        )

    @staticmethod
    def create_feature_design_task(
        insights_task_id: str,
    ) -> Task:
        """Create a feature design task.

        Args:
            insights_task_id: ID of the community analysis task

        Returns:
            Feature design task
        """
        return TaskFactory.create_task(
            name="Feature Design",
            description="Generate feature proposals from community insights",
            role=AgentRole.FEATURE_DESIGNER,
            dependencies=[insights_task_id],
        )

    @staticmethod
    def create_monetization_review_task(
        design_task_id: str,
    ) -> Task:
        """Create a monetization review task.

        Args:
            design_task_id: ID of the feature design task

        Returns:
            Monetization review task
        """
        return TaskFactory.create_task(
            name="Monetization Review",
            description="Validate proposals against F2P guardrails",
            role=AgentRole.MONETIZATION_REVIEWER,
            dependencies=[design_task_id],
        )

    @staticmethod
    def create_comparative_analysis_task(
        review_task_id: str,
    ) -> Task:
        """Create a comparative analysis task.

        Args:
            review_task_id: ID of the monetization review task

        Returns:
            Comparative analysis task
        """
        return TaskFactory.create_task(
            name="Comparative Analysis",
            description="Enrich proposals with competitive insights",
            role=AgentRole.COMPARATIVE_ANALYST,
            dependencies=[review_task_id],
        )

    @staticmethod
    def create_issue_drafting_task(
        analysis_task_id: str,
    ) -> Task:
        """Create an issue drafting task.

        Args:
            analysis_task_id: ID of the comparative analysis task

        Returns:
            Issue drafting task
        """
        return TaskFactory.create_task(
            name="Issue Drafting",
            description="Create GitHub issue drafts from proposals",
            role=AgentRole.ISSUE_DRAFTER,
            dependencies=[analysis_task_id],
        )

    @staticmethod
    def create_full_pipeline() -> List[Task]:
        """Create a full pipeline of tasks.

        Returns:
            List of tasks representing the full pipeline
        """
        community_task = TaskFactory.create_community_analysis_task()
        design_task = TaskFactory.create_feature_design_task(community_task.id)
        review_task = TaskFactory.create_monetization_review_task(design_task.id)
        analysis_task = TaskFactory.create_comparative_analysis_task(review_task.id)
        issue_task = TaskFactory.create_issue_drafting_task(analysis_task.id)

        return [community_task, design_task, review_task, analysis_task, issue_task]


@dataclass
class PrioritizedTask:
    """Wrapper for tasks with priority for queue ordering.

    Attributes:
        priority: Task priority (lower = higher priority)
        task: The wrapped task
    """

    priority: int
    task: Task

    def __lt__(self, other: "PrioritizedTask") -> bool:
        """Compare by priority for queue ordering."""
        return self.priority < other.priority


class TaskQueue:
    """Priority queue for managing tasks.

    Manages task scheduling, dependency resolution, and execution order.
    """

    def __init__(self):
        """Initialize the task queue."""
        self._queue: PriorityQueue = PriorityQueue()
        self._tasks: Dict[str, Task] = {}
        self._completed: Dict[str, TaskResult] = {}
        self._priority_counter = 0

    def add(self, task: Task, priority: Optional[int] = None) -> None:
        """Add a task to the queue.

        Args:
            task: Task to add
            priority: Optional priority override
        """
        if priority is None:
            priority = self._priority_counter
            self._priority_counter += 1

        self._tasks[task.id] = task
        self._queue.put(PrioritizedTask(priority=priority, task=task))
        logger.debug(f"Added task: {task.name} (id={task.id})")

    def add_all(self, tasks: List[Task]) -> None:
        """Add multiple tasks to the queue.

        Args:
            tasks: List of tasks to add
        """
        for task in tasks:
            self.add(task)

    def get_next(self) -> Optional[Task]:
        """Get the next task that is ready to execute.

        Returns:
            Next ready task, or None if no tasks are ready
        """
        ready_tasks = []

        while not self._queue.empty():
            prioritized = self._queue.get()
            task = prioritized.task

            # Skip completed or in-progress tasks
            if task.status in (TaskStatus.COMPLETED, TaskStatus.IN_PROGRESS):
                continue

            # Check if dependencies are met
            if self._dependencies_met(task):
                return task
            else:
                ready_tasks.append(prioritized)

        # Put back tasks that weren't ready
        for pt in ready_tasks:
            self._queue.put(pt)

        return None

    def _dependencies_met(self, task: Task) -> bool:
        """Check if all task dependencies are completed.

        Args:
            task: Task to check

        Returns:
            True if all dependencies are complete
        """
        for dep_id in task.dependencies:
            if dep_id not in self._completed:
                return False
            if not self._completed[dep_id].success:
                return False
        return True

    def mark_completed(self, task_id: str, result: TaskResult) -> None:
        """Mark a task as completed.

        Args:
            task_id: ID of the completed task
            result: Result of the task
        """
        if task_id in self._tasks:
            self._tasks[task_id].status = TaskStatus.COMPLETED
            self._tasks[task_id].result = result
        self._completed[task_id] = result
        logger.debug(f"Task completed: {task_id}")

    def mark_failed(self, task_id: str, error: str) -> None:
        """Mark a task as failed.

        Args:
            task_id: ID of the failed task
            error: Error message
        """
        result = TaskResult(task_id=task_id, success=False, error=error)
        if task_id in self._tasks:
            self._tasks[task_id].status = TaskStatus.FAILED
            self._tasks[task_id].result = result
        self._completed[task_id] = result
        logger.error(f"Task failed: {task_id} - {error}")

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID.

        Args:
            task_id: Task ID

        Returns:
            Task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_result(self, task_id: str) -> Optional[TaskResult]:
        """Get a task result by ID.

        Args:
            task_id: Task ID

        Returns:
            TaskResult if task is completed, None otherwise
        """
        return self._completed.get(task_id)

    def get_dependency_data(self, task: Task) -> Dict[str, Any]:
        """Get output data from all completed dependencies.

        Args:
            task: Task to get dependency data for

        Returns:
            Merged output data from all dependencies
        """
        data = {}
        for dep_id in task.dependencies:
            if dep_id in self._completed:
                result = self._completed[dep_id]
                if result.success and result.output_data:
                    data.update(result.output_data)
        return data

    def is_empty(self) -> bool:
        """Check if the queue is empty.

        Returns:
            True if no tasks remain
        """
        return self._queue.empty()

    def pending_count(self) -> int:
        """Get count of pending tasks.

        Returns:
            Number of pending tasks
        """
        return sum(
            1
            for t in self._tasks.values()
            if t.status == TaskStatus.PENDING
        )

    def completed_count(self) -> int:
        """Get count of completed tasks.

        Returns:
            Number of completed tasks
        """
        return len(self._completed)

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the queue state.

        Returns:
            Queue summary dictionary
        """
        status_counts: Dict[str, int] = {}
        for task in self._tasks.values():
            status = task.status.value
            status_counts[status] = status_counts.get(status, 0) + 1

        return {
            "total_tasks": len(self._tasks),
            "completed": self.completed_count(),
            "pending": self.pending_count(),
            "by_status": status_counts,
        }
