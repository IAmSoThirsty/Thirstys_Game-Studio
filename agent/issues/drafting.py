"""Issue drafting utilities for turning proposals into GitHub issues.

This module provides utilities for converting feature proposals and
community insights into well-formatted GitHub issue drafts.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional

from agent.core.interfaces import FeatureProposal, CommunityInsight

logger = logging.getLogger(__name__)


@dataclass
class DraftedIssue:
    """A drafted GitHub issue.

    Attributes:
        title: Issue title
        body: Issue body in markdown
        labels: Suggested labels
        assignees: Suggested assignees
        milestone: Suggested milestone
        priority: Priority level
        created_at: When the draft was created
    """

    title: str
    body: str
    labels: List[str] = field(default_factory=list)
    assignees: List[str] = field(default_factory=list)
    milestone: Optional[str] = None
    priority: str = "medium"
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "title": self.title,
            "body": self.body,
            "labels": self.labels,
            "assignees": self.assignees,
            "milestone": self.milestone,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
        }

    def to_markdown(self) -> str:
        """Convert to markdown format for preview."""
        md = f"# {self.title}\n\n"
        md += f"**Priority:** {self.priority}\n"
        md += f"**Labels:** {', '.join(self.labels) if self.labels else 'None'}\n"
        if self.milestone:
            md += f"**Milestone:** {self.milestone}\n"
        md += "\n---\n\n"
        md += self.body
        return md


class IssueDrafter:
    """Utility for drafting GitHub issues from proposals.

    Converts feature proposals into well-formatted GitHub issue drafts
    with appropriate labels, descriptions, and metadata.

    Attributes:
        default_labels: Default labels to apply to issues
        category_labels: Mapping of categories to labels
    """

    def __init__(self):
        """Initialize the issue drafter."""
        self.default_labels = ["community-driven", "auto-generated"]

        self.category_labels = {
            "customization": ["enhancement", "customization"],
            "cosmetics": ["enhancement", "cosmetics"],
            "social": ["enhancement", "social-features"],
            "events": ["enhancement", "events"],
            "progression": ["enhancement", "progression"],
            "performance": ["bug", "performance"],
            "balance": ["enhancement", "balance"],
            "content": ["enhancement", "content"],
            "general": ["enhancement"],
        }

        self.priority_thresholds = {
            "critical": 0.9,
            "high": 0.7,
            "medium": 0.4,
            "low": 0.0,
        }

    def draft_from_proposal(
        self, proposal: FeatureProposal
    ) -> DraftedIssue:
        """Create a drafted issue from a feature proposal.

        Args:
            proposal: Feature proposal to convert

        Returns:
            Drafted GitHub issue
        """
        # Determine priority
        priority = self._determine_priority(proposal.priority)

        # Build labels
        labels = self.default_labels.copy()
        labels.extend(self.category_labels.get(proposal.category, ["enhancement"]))
        if proposal.f2p_compliant:
            labels.append("f2p-approved")
        else:
            labels.append("needs-review")

        # Build issue body
        body = self._build_proposal_body(proposal)

        return DraftedIssue(
            title=f"[Feature] {proposal.title}",
            body=body,
            labels=labels,
            priority=priority,
            milestone=self._suggest_milestone(proposal),
        )

    def draft_from_insight(
        self, insight: CommunityInsight
    ) -> DraftedIssue:
        """Create a drafted issue from a community insight.

        Args:
            insight: Community insight to convert

        Returns:
            Drafted GitHub issue
        """
        priority = self._determine_priority(insight.priority)

        labels = self.default_labels.copy()
        labels.append(f"source:{insight.source}")

        if insight.category == "bug_report":
            labels.append("bug")
            title_prefix = "[Bug]"
        elif insight.category == "feature_request":
            labels.append("enhancement")
            title_prefix = "[Feature Request]"
        else:
            labels.append("feedback")
            title_prefix = "[Community Feedback]"

        body = self._build_insight_body(insight)

        # Generate title from content
        title_content = insight.content[:80]
        if len(insight.content) > 80:
            title_content = title_content.rsplit(" ", 1)[0] + "..."

        return DraftedIssue(
            title=f"{title_prefix} {title_content}",
            body=body,
            labels=labels,
            priority=priority,
        )

    def _determine_priority(self, score: float) -> str:
        """Determine priority level from score.

        Args:
            score: Priority score (0.0 to 1.0)

        Returns:
            Priority string
        """
        for priority, threshold in self.priority_thresholds.items():
            if score >= threshold:
                return priority
        return "low"

    def _suggest_milestone(self, proposal: FeatureProposal) -> Optional[str]:
        """Suggest a milestone for the proposal.

        Args:
            proposal: Feature proposal

        Returns:
            Suggested milestone name or None
        """
        if proposal.priority >= 0.8:
            return "Next Release"
        elif proposal.priority >= 0.5:
            return "Backlog - High Priority"
        else:
            return "Backlog"

    def _build_proposal_body(self, proposal: FeatureProposal) -> str:
        """Build the issue body for a proposal.

        Args:
            proposal: Feature proposal

        Returns:
            Formatted markdown body
        """
        body = f"""## Summary

{proposal.description}

## Details

- **Category:** {proposal.category}
- **Priority Score:** {proposal.priority:.2f}
- **Monetization Type:** {proposal.monetization_type}
- **F2P Compliant:** {'✅ Yes' if proposal.f2p_compliant else '❌ No - Needs Review'}

## Source

This feature was generated from community feedback analysis.
- **Source Insights:** {len(proposal.source_insights)} community inputs

"""

        if proposal.guardrail_notes:
            body += "## Guardrail Notes\n\n"
            for note in proposal.guardrail_notes:
                body += f"- ⚠️ {note}\n"
            body += "\n"

        if proposal.comparative_notes:
            body += "## Competitive Analysis\n\n"
            for note in proposal.comparative_notes:
                body += f"- {note}\n"
            body += "\n"

        body += """## Acceptance Criteria

- [ ] Feature implemented as described
- [ ] F2P guardrails validated
- [ ] No gameplay advantages for paid content
- [ ] Unit tests added
- [ ] Documentation updated

---

*This issue was auto-generated by the Thirsty's Game Studio Agent System.*
"""

        return body

    def _build_insight_body(self, insight: CommunityInsight) -> str:
        """Build the issue body for a community insight.

        Args:
            insight: Community insight

        Returns:
            Formatted markdown body
        """
        body = f"""## Community Feedback

> {insight.content}

## Details

- **Source:** {insight.source}
- **Category:** {insight.category}
- **Sentiment:** {self._sentiment_emoji(insight.sentiment)} ({insight.sentiment:.2f})
- **Priority Score:** {insight.priority:.2f}
- **Topics:** {', '.join(insight.topics) if insight.topics else 'None identified'}

## Engagement Metrics

"""
        for metric, value in insight.engagement.items():
            body += f"- **{metric.title()}:** {value}\n"

        body += """

## Next Steps

- [ ] Review feedback validity
- [ ] Determine if actionable
- [ ] Create feature proposal if applicable
- [ ] Respond to community if appropriate

---

*This issue was auto-generated from community feedback by the Thirsty's Game Studio Agent System.*
"""

        return body

    def _sentiment_emoji(self, sentiment: float) -> str:
        """Get emoji for sentiment score.

        Args:
            sentiment: Sentiment score (-1.0 to 1.0)

        Returns:
            Emoji string
        """
        if sentiment >= 0.5:
            return "😊 Positive"
        elif sentiment >= 0.0:
            return "😐 Neutral"
        elif sentiment >= -0.5:
            return "😕 Slightly Negative"
        else:
            return "😠 Negative"

    def batch_draft(
        self, proposals: List[FeatureProposal]
    ) -> List[DraftedIssue]:
        """Draft issues for multiple proposals.

        Args:
            proposals: List of feature proposals

        Returns:
            List of drafted issues
        """
        return [self.draft_from_proposal(p) for p in proposals]

    def generate_issue_report(
        self, issues: List[DraftedIssue]
    ) -> Dict[str, Any]:
        """Generate a report of drafted issues.

        Args:
            issues: List of drafted issues

        Returns:
            Report dictionary
        """
        priority_counts: Dict[str, int] = {}
        for issue in issues:
            priority_counts[issue.priority] = (
                priority_counts.get(issue.priority, 0) + 1
            )

        return {
            "total_issues": len(issues),
            "by_priority": priority_counts,
            "issues": [i.to_dict() for i in issues],
        }
