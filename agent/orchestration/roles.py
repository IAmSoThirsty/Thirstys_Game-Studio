"""Role definitions for the multi-agent system.

This module defines the roles that agents can assume and their
capabilities within the orchestration system.
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Set

from agent.core.interfaces import AgentRole

logger = logging.getLogger(__name__)


@dataclass
class RoleDefinition:
    """Definition of an agent role.

    Attributes:
        role: The agent role enum
        name: Human-readable name
        description: Role description
        capabilities: List of capabilities this role has
        required_inputs: Types of inputs this role requires
        produced_outputs: Types of outputs this role produces
        dependencies: Roles that must complete before this one
    """

    role: AgentRole
    name: str
    description: str
    capabilities: List[str] = field(default_factory=list)
    required_inputs: List[str] = field(default_factory=list)
    produced_outputs: List[str] = field(default_factory=list)
    dependencies: List[AgentRole] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "role": self.role.value,
            "name": self.name,
            "description": self.description,
            "capabilities": self.capabilities,
            "required_inputs": self.required_inputs,
            "produced_outputs": self.produced_outputs,
            "dependencies": [d.value for d in self.dependencies],
        }


class RoleRegistry:
    """Registry of all available agent roles.

    Manages role definitions and their relationships.
    """

    def __init__(self):
        """Initialize the role registry with default roles."""
        self._roles: Dict[AgentRole, RoleDefinition] = {}
        self._register_default_roles()

    def _register_default_roles(self) -> None:
        """Register the default agent roles."""
        self.register(
            RoleDefinition(
                role=AgentRole.MANAGER,
                name="Team Manager",
                description="Orchestrates the agent team and coordinates task execution",
                capabilities=[
                    "task_assignment",
                    "workflow_control",
                    "status_monitoring",
                    "result_aggregation",
                ],
                required_inputs=["task_queue"],
                produced_outputs=["execution_report", "team_status"],
            )
        )

        self.register(
            RoleDefinition(
                role=AgentRole.COMMUNITY_ANALYST,
                name="Community Analyst",
                description="Analyzes community feedback from various sources",
                capabilities=[
                    "data_ingestion",
                    "sentiment_analysis",
                    "topic_extraction",
                    "insight_aggregation",
                ],
                required_inputs=["community_sources"],
                produced_outputs=["community_insights", "sentiment_report"],
            )
        )

        self.register(
            RoleDefinition(
                role=AgentRole.FEATURE_DESIGNER,
                name="Feature Designer",
                description="Generates feature proposals from community insights",
                capabilities=[
                    "proposal_generation",
                    "feature_scoping",
                    "priority_assessment",
                ],
                required_inputs=["community_insights"],
                produced_outputs=["feature_proposals"],
                dependencies=[AgentRole.COMMUNITY_ANALYST],
            )
        )

        self.register(
            RoleDefinition(
                role=AgentRole.MONETIZATION_REVIEWER,
                name="Monetization Reviewer",
                description="Reviews proposals for F2P compliance",
                capabilities=[
                    "guardrail_checking",
                    "f2p_validation",
                    "policy_enforcement",
                ],
                required_inputs=["feature_proposals"],
                produced_outputs=["validated_proposals", "compliance_report"],
                dependencies=[AgentRole.FEATURE_DESIGNER],
            )
        )

        self.register(
            RoleDefinition(
                role=AgentRole.COMPARATIVE_ANALYST,
                name="Comparative Analyst",
                description="Enriches proposals with competitive analysis",
                capabilities=[
                    "competitor_research",
                    "feature_comparison",
                    "best_practice_identification",
                ],
                required_inputs=["validated_proposals"],
                produced_outputs=["enriched_proposals"],
                dependencies=[AgentRole.MONETIZATION_REVIEWER],
            )
        )

        self.register(
            RoleDefinition(
                role=AgentRole.ISSUE_DRAFTER,
                name="Issue Drafter",
                description="Creates GitHub issue drafts from proposals",
                capabilities=[
                    "issue_formatting",
                    "label_assignment",
                    "milestone_suggestion",
                ],
                required_inputs=["enriched_proposals"],
                produced_outputs=["drafted_issues"],
                dependencies=[AgentRole.COMPARATIVE_ANALYST],
            )
        )

        self.register(
            RoleDefinition(
                role=AgentRole.PR_CREATOR,
                name="PR Creator",
                description="Creates pull request templates from proposals",
                capabilities=[
                    "pr_formatting",
                    "branch_naming",
                    "checklist_generation",
                ],
                required_inputs=["enriched_proposals"],
                produced_outputs=["drafted_prs"],
                dependencies=[AgentRole.COMPARATIVE_ANALYST],
            )
        )

    def register(self, definition: RoleDefinition) -> None:
        """Register a role definition.

        Args:
            definition: Role definition to register
        """
        self._roles[definition.role] = definition
        logger.debug(f"Registered role: {definition.name}")

    def get(self, role: AgentRole) -> RoleDefinition:
        """Get a role definition.

        Args:
            role: Role to get

        Returns:
            Role definition

        Raises:
            KeyError: If role not found
        """
        if role not in self._roles:
            raise KeyError(f"Role not found: {role}")
        return self._roles[role]

    def get_all(self) -> List[RoleDefinition]:
        """Get all registered roles.

        Returns:
            List of all role definitions
        """
        return list(self._roles.values())

    def get_dependencies(self, role: AgentRole) -> List[AgentRole]:
        """Get the dependencies for a role.

        Args:
            role: Role to get dependencies for

        Returns:
            List of dependent roles
        """
        return self._roles[role].dependencies

    def get_execution_order(self) -> List[AgentRole]:
        """Get roles in execution order based on dependencies.

        Returns:
            List of roles in order they should execute
        """
        # Simple topological sort
        visited: Set[AgentRole] = set()
        order: List[AgentRole] = []

        def visit(role: AgentRole) -> None:
            if role in visited:
                return
            visited.add(role)
            for dep in self.get_dependencies(role):
                visit(dep)
            order.append(role)

        for role in self._roles:
            visit(role)

        return order
