"""Core interfaces for the multi-agent gaming platform.

This module defines the foundational abstractions used throughout the agent system
for community insights processing, feature proposal generation, and monetization
guardrails enforcement.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class AgentRole(Enum):
    """Roles that agents can assume in the orchestration system."""

    MANAGER = "manager"
    COMMUNITY_ANALYST = "community_analyst"
    FEATURE_DESIGNER = "feature_designer"
    MONETIZATION_REVIEWER = "monetization_reviewer"
    COMPARATIVE_ANALYST = "comparative_analyst"
    ISSUE_DRAFTER = "issue_drafter"
    PR_CREATOR = "pr_creator"


class TaskStatus(Enum):
    """Status of a task in the pipeline."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class CommunityInsight:
    """Represents a normalized insight from community sources.

    Attributes:
        source: Origin platform (reddit, discord, steam, etc.)
        content: Raw content of the insight
        sentiment: Sentiment score (-1.0 to 1.0)
        topics: Extracted topics/keywords
        author: Anonymous author identifier
        timestamp: When the insight was captured
        engagement: Engagement metrics (upvotes, reactions, etc.)
        category: Categorization (feature_request, bug_report, praise, etc.)
        priority: Calculated priority score (0.0 to 1.0)
    """

    source: str
    content: str
    sentiment: float = 0.0
    topics: List[str] = field(default_factory=list)
    author: str = "anonymous"
    timestamp: datetime = field(default_factory=datetime.utcnow)
    engagement: Dict[str, int] = field(default_factory=dict)
    category: str = "general"
    priority: float = 0.5

    def to_dict(self) -> Dict[str, Any]:
        """Convert insight to dictionary for serialization."""
        return {
            "source": self.source,
            "content": self.content,
            "sentiment": self.sentiment,
            "topics": self.topics,
            "author": self.author,
            "timestamp": self.timestamp.isoformat(),
            "engagement": self.engagement,
            "category": self.category,
            "priority": self.priority,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CommunityInsight":
        """Create insight from dictionary."""
        data = data.copy()
        if isinstance(data.get("timestamp"), str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)


@dataclass
class FeatureProposal:
    """A feature proposal derived from community insights.

    Attributes:
        title: Brief title of the proposal
        description: Detailed description
        source_insights: IDs of insights that inspired this proposal
        category: Type (cosmetic, qol, gameplay, etc.)
        monetization_type: How it could be monetized (free, cosmetic, etc.)
        priority: Priority score
        f2p_compliant: Whether it passes F2P guardrails
        guardrail_notes: Notes from monetization review
        comparative_notes: Notes from competitive analysis
    """

    title: str
    description: str
    source_insights: List[str] = field(default_factory=list)
    category: str = "general"
    monetization_type: str = "free"
    priority: float = 0.5
    f2p_compliant: bool = True
    guardrail_notes: List[str] = field(default_factory=list)
    comparative_notes: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert proposal to dictionary for serialization."""
        return {
            "title": self.title,
            "description": self.description,
            "source_insights": self.source_insights,
            "category": self.category,
            "monetization_type": self.monetization_type,
            "priority": self.priority,
            "f2p_compliant": self.f2p_compliant,
            "guardrail_notes": self.guardrail_notes,
            "comparative_notes": self.comparative_notes,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FeatureProposal":
        """Create proposal from dictionary."""
        data = data.copy()
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)


class MonetizationGuardrail(Enum):
    """Monetization guardrails to prevent pay-to-win mechanics."""

    NO_PAY_TO_WIN = "no_pay_to_win"
    COSMETIC_ONLY = "cosmetic_only"
    NO_GAMEPLAY_ADVANTAGE = "no_gameplay_advantage"
    FAIR_PROGRESSION = "fair_progression"
    TRANSPARENT_ODDS = "transparent_odds"
    NO_LOOT_BOXES = "no_loot_boxes"
    ACCESSIBLE_CONTENT = "accessible_content"


@dataclass
class Task:
    """A task to be executed by workers.

    Attributes:
        id: Unique task identifier
        name: Human-readable task name
        description: Task description
        role: Required agent role
        input_data: Input data for the task
        dependencies: Task IDs that must complete first
        status: Current task status
        result: Task result after completion
    """

    id: str
    name: str
    description: str
    role: AgentRole
    input_data: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    result: Optional["TaskResult"] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "role": self.role.value,
            "input_data": self.input_data,
            "dependencies": self.dependencies,
            "status": self.status.value,
            "result": self.result.to_dict() if self.result else None,
        }


@dataclass
class TaskResult:
    """Result of a completed task.

    Attributes:
        task_id: ID of the completed task
        success: Whether the task succeeded
        output_data: Output data from the task
        error: Error message if failed
        execution_time: Time taken to execute (seconds)
    """

    task_id: str
    success: bool
    output_data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    execution_time: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for serialization."""
        return {
            "task_id": self.task_id,
            "success": self.success,
            "output_data": self.output_data,
            "error": self.error,
            "execution_time": self.execution_time,
        }


class Worker(ABC):
    """Abstract base class for task workers.

    Workers are responsible for executing tasks of specific types
    based on their assigned roles.
    """

    def __init__(self, role: AgentRole):
        """Initialize worker with assigned role."""
        self.role = role

    @abstractmethod
    def execute(self, task: Task) -> TaskResult:
        """Execute the given task and return result.

        Args:
            task: The task to execute

        Returns:
            TaskResult with outcome of execution
        """
        pass

    @abstractmethod
    def can_handle(self, task: Task) -> bool:
        """Check if this worker can handle the given task.

        Args:
            task: The task to check

        Returns:
            True if worker can handle the task
        """
        pass


class CommunitySource(ABC):
    """Abstract base class for community data sources.

    Implementations fetch and normalize data from various community platforms.
    """

    @abstractmethod
    def fetch_insights(
        self, limit: int = 100, since: Optional[datetime] = None
    ) -> List[CommunityInsight]:
        """Fetch insights from the community source.

        Args:
            limit: Maximum number of insights to fetch
            since: Only fetch insights after this timestamp

        Returns:
            List of normalized community insights
        """
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        """Get the name of this source."""
        pass


class Analyzer(ABC):
    """Abstract base class for insight analyzers."""

    @abstractmethod
    def analyze(self, insight: CommunityInsight) -> CommunityInsight:
        """Analyze and enrich a community insight.

        Args:
            insight: Raw insight to analyze

        Returns:
            Enriched insight with analysis results
        """
        pass
