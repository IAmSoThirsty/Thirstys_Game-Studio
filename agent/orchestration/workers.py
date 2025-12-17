"""Worker implementations for the multi-agent system.

This module provides concrete worker implementations for each
agent role in the orchestration system.
"""

import logging
import time
from agent.core.interfaces import (
    AgentRole,
    Task,
    TaskResult,
    Worker,
    TaskStatus,
)
from agent.community.pipeline import CommunityPipeline
from agent.monetization.guardrails import MonetizationGuardrailChecker
from agent.comparative.age_of_origins import AgeOfOriginsAnalyzer
from agent.issues.drafting import IssueDrafter

logger = logging.getLogger(__name__)


class CommunityAnalystWorker(Worker):
    """Worker for community analysis tasks.

    Fetches and analyzes community insights from configured sources.
    """

    def __init__(self):
        """Initialize the community analyst worker."""
        super().__init__(AgentRole.COMMUNITY_ANALYST)
        self.pipeline = CommunityPipeline()

    def can_handle(self, task: Task) -> bool:
        """Check if this worker can handle the task."""
        return task.role == AgentRole.COMMUNITY_ANALYST

    def execute(self, task: Task) -> TaskResult:
        """Execute the community analysis task."""
        start_time = time.time()
        task.status = TaskStatus.IN_PROGRESS

        try:
            # Get configuration from task input
            limit = task.input_data.get("limit_per_source", 50)

            # Run the community pipeline
            results = self.pipeline.run(limit_per_source=limit)

            # Generate proposals
            proposals = self.pipeline.generate_proposals()

            execution_time = time.time() - start_time

            return TaskResult(
                task_id=task.id,
                success=True,
                output_data={
                    "insights": results.get("insights", []),
                    "summary": results.get("summary", {}),
                    "proposals": [p.to_dict() for p in proposals],
                    "raw_proposals": proposals,
                },
                execution_time=execution_time,
            )

        except Exception as e:
            logger.exception(f"Community analysis failed: {e}")
            return TaskResult(
                task_id=task.id,
                success=False,
                error=str(e),
                execution_time=time.time() - start_time,
            )


class FeatureDesignerWorker(Worker):
    """Worker for feature design tasks.

    Generates feature proposals from community insights.
    """

    def __init__(self):
        """Initialize the feature designer worker."""
        super().__init__(AgentRole.FEATURE_DESIGNER)

    def can_handle(self, task: Task) -> bool:
        """Check if this worker can handle the task."""
        return task.role == AgentRole.FEATURE_DESIGNER

    def execute(self, task: Task) -> TaskResult:
        """Execute the feature design task."""
        start_time = time.time()
        task.status = TaskStatus.IN_PROGRESS

        try:
            # Get proposals from dependency data
            proposals = task.input_data.get("raw_proposals", [])

            # If no proposals from dependencies, get from serialized data
            if not proposals:
                proposal_dicts = task.input_data.get("proposals", [])
                from agent.core.interfaces import FeatureProposal

                proposals = [FeatureProposal.from_dict(p) for p in proposal_dicts]

            execution_time = time.time() - start_time

            return TaskResult(
                task_id=task.id,
                success=True,
                output_data={
                    "proposals": [p.to_dict() for p in proposals],
                    "raw_proposals": proposals,
                    "count": len(proposals),
                },
                execution_time=execution_time,
            )

        except Exception as e:
            logger.exception(f"Feature design failed: {e}")
            return TaskResult(
                task_id=task.id,
                success=False,
                error=str(e),
                execution_time=time.time() - start_time,
            )


class MonetizationReviewerWorker(Worker):
    """Worker for monetization review tasks.

    Validates proposals against F2P guardrails.
    """

    def __init__(self):
        """Initialize the monetization reviewer worker."""
        super().__init__(AgentRole.MONETIZATION_REVIEWER)
        self.checker = MonetizationGuardrailChecker()

    def can_handle(self, task: Task) -> bool:
        """Check if this worker can handle the task."""
        return task.role == AgentRole.MONETIZATION_REVIEWER

    def execute(self, task: Task) -> TaskResult:
        """Execute the monetization review task."""
        start_time = time.time()
        task.status = TaskStatus.IN_PROGRESS

        try:
            # Get proposals from dependency data
            proposals = task.input_data.get("raw_proposals", [])

            # If no proposals from dependencies, get from serialized data
            if not proposals:
                proposal_dicts = task.input_data.get("proposals", [])
                from agent.core.interfaces import FeatureProposal

                proposals = [FeatureProposal.from_dict(p) for p in proposal_dicts]

            # Validate proposals
            validation_results = self.checker.validate_proposals(proposals)

            execution_time = time.time() - start_time

            return TaskResult(
                task_id=task.id,
                success=True,
                output_data={
                    "proposals": [p.to_dict() for p in proposals],
                    "raw_proposals": proposals,
                    "validation": validation_results,
                    "compliant_count": validation_results.get("compliant_proposals", 0),
                    "total_count": len(proposals),
                },
                execution_time=execution_time,
            )

        except Exception as e:
            logger.exception(f"Monetization review failed: {e}")
            return TaskResult(
                task_id=task.id,
                success=False,
                error=str(e),
                execution_time=time.time() - start_time,
            )


class ComparativeAnalystWorker(Worker):
    """Worker for comparative analysis tasks.

    Enriches proposals with competitive insights.
    """

    def __init__(self):
        """Initialize the comparative analyst worker."""
        super().__init__(AgentRole.COMPARATIVE_ANALYST)
        self.analyzer = AgeOfOriginsAnalyzer()

    def can_handle(self, task: Task) -> bool:
        """Check if this worker can handle the task."""
        return task.role == AgentRole.COMPARATIVE_ANALYST

    def execute(self, task: Task) -> TaskResult:
        """Execute the comparative analysis task."""
        start_time = time.time()
        task.status = TaskStatus.IN_PROGRESS

        try:
            # Get proposals from dependency data
            proposals = task.input_data.get("raw_proposals", [])

            # If no proposals from dependencies, get from serialized data
            if not proposals:
                proposal_dicts = task.input_data.get("proposals", [])
                from agent.core.interfaces import FeatureProposal

                proposals = [FeatureProposal.from_dict(p) for p in proposal_dicts]

            # Enrich proposals with competitive analysis
            enriched_proposals = self.analyzer.enrich_proposals(proposals)

            # Generate competitive report
            competitive_report = self.analyzer.generate_report()

            execution_time = time.time() - start_time

            return TaskResult(
                task_id=task.id,
                success=True,
                output_data={
                    "proposals": [p.to_dict() for p in enriched_proposals],
                    "raw_proposals": enriched_proposals,
                    "competitive_report": competitive_report,
                },
                execution_time=execution_time,
            )

        except Exception as e:
            logger.exception(f"Comparative analysis failed: {e}")
            return TaskResult(
                task_id=task.id,
                success=False,
                error=str(e),
                execution_time=time.time() - start_time,
            )


class IssueDrafterWorker(Worker):
    """Worker for issue drafting tasks.

    Creates GitHub issue drafts from proposals.
    """

    def __init__(self):
        """Initialize the issue drafter worker."""
        super().__init__(AgentRole.ISSUE_DRAFTER)
        self.drafter = IssueDrafter()

    def can_handle(self, task: Task) -> bool:
        """Check if this worker can handle the task."""
        return task.role == AgentRole.ISSUE_DRAFTER

    def execute(self, task: Task) -> TaskResult:
        """Execute the issue drafting task."""
        start_time = time.time()
        task.status = TaskStatus.IN_PROGRESS

        try:
            # Get proposals from dependency data
            proposals = task.input_data.get("raw_proposals", [])

            # If no proposals from dependencies, get from serialized data
            if not proposals:
                proposal_dicts = task.input_data.get("proposals", [])
                from agent.core.interfaces import FeatureProposal

                proposals = [FeatureProposal.from_dict(p) for p in proposal_dicts]

            # Draft issues from proposals
            issues = self.drafter.batch_draft(proposals)

            # Generate report
            issue_report = self.drafter.generate_issue_report(issues)

            execution_time = time.time() - start_time

            return TaskResult(
                task_id=task.id,
                success=True,
                output_data={
                    "issues": [i.to_dict() for i in issues],
                    "issue_report": issue_report,
                    "count": len(issues),
                },
                execution_time=execution_time,
            )

        except Exception as e:
            logger.exception(f"Issue drafting failed: {e}")
            return TaskResult(
                task_id=task.id,
                success=False,
                error=str(e),
                execution_time=time.time() - start_time,
            )


def create_worker_for_role(role: AgentRole) -> Worker:
    """Factory function to create a worker for a given role.

    Args:
        role: The agent role

    Returns:
        Worker instance for the role

    Raises:
        ValueError: If no worker exists for the role
    """
    workers = {
        AgentRole.COMMUNITY_ANALYST: CommunityAnalystWorker,
        AgentRole.FEATURE_DESIGNER: FeatureDesignerWorker,
        AgentRole.MONETIZATION_REVIEWER: MonetizationReviewerWorker,
        AgentRole.COMPARATIVE_ANALYST: ComparativeAnalystWorker,
        AgentRole.ISSUE_DRAFTER: IssueDrafterWorker,
    }

    if role not in workers:
        raise ValueError(f"No worker available for role: {role}")

    return workers[role]()
