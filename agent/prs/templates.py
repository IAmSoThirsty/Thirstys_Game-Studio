"""PR template generation for GitHub integration.

This module provides utilities for generating pull request templates
from feature proposals and agent-generated content.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional

from agent.core.interfaces import FeatureProposal

logger = logging.getLogger(__name__)


@dataclass
class DraftedPR:
    """A drafted GitHub pull request.

    Attributes:
        title: PR title
        body: PR body in markdown
        labels: Suggested labels
        reviewers: Suggested reviewers
        base_branch: Target branch
        head_branch: Source branch suggestion
        related_issues: Related issue numbers
        created_at: When the draft was created
    """

    title: str
    body: str
    labels: List[str] = field(default_factory=list)
    reviewers: List[str] = field(default_factory=list)
    base_branch: str = "main"
    head_branch: str = ""
    related_issues: List[int] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "title": self.title,
            "body": self.body,
            "labels": self.labels,
            "reviewers": self.reviewers,
            "base_branch": self.base_branch,
            "head_branch": self.head_branch,
            "related_issues": self.related_issues,
            "created_at": self.created_at.isoformat(),
        }

    def to_markdown(self) -> str:
        """Convert to markdown format for preview."""
        md = f"# {self.title}\n\n"
        md += f"**Base Branch:** {self.base_branch}\n"
        md += f"**Head Branch:** {self.head_branch}\n"
        md += f"**Labels:** {', '.join(self.labels) if self.labels else 'None'}\n"
        if self.related_issues:
            md += f"**Related Issues:** {', '.join(f'#{i}' for i in self.related_issues)}\n"
        md += "\n---\n\n"
        md += self.body
        return md


class PRTemplateGenerator:
    """Generator for GitHub PR templates from proposals.

    Creates well-formatted PR drafts that include all necessary
    information for review and merge.

    Attributes:
        default_labels: Default labels for generated PRs
        branch_prefix: Prefix for suggested branch names
    """

    def __init__(self, branch_prefix: str = "feature/"):
        """Initialize the PR template generator.

        Args:
            branch_prefix: Prefix for suggested branch names
        """
        self.default_labels = ["auto-generated", "needs-review"]
        self.branch_prefix = branch_prefix

        self.category_labels = {
            "customization": ["enhancement", "customization"],
            "cosmetics": ["enhancement", "cosmetics"],
            "social": ["enhancement", "social"],
            "events": ["enhancement", "events"],
            "progression": ["enhancement", "gameplay"],
            "performance": ["optimization", "performance"],
            "balance": ["balance", "gameplay"],
            "content": ["content", "enhancement"],
        }

    def generate_from_proposal(
        self,
        proposal: FeatureProposal,
        related_issues: Optional[List[int]] = None,
    ) -> DraftedPR:
        """Generate a PR draft from a feature proposal.

        Args:
            proposal: Feature proposal to convert
            related_issues: Related issue numbers

        Returns:
            Drafted pull request
        """
        # Generate branch name
        branch_name = self._generate_branch_name(proposal)

        # Build labels
        labels = self.default_labels.copy()
        labels.extend(
            self.category_labels.get(proposal.category, ["enhancement"])
        )
        if proposal.f2p_compliant:
            labels.append("f2p-approved")

        # Build PR body
        body = self._build_proposal_pr_body(proposal, related_issues)

        return DraftedPR(
            title=f"feat({proposal.category}): {proposal.title}",
            body=body,
            labels=labels,
            head_branch=branch_name,
            related_issues=related_issues or [],
        )

    def generate_agent_run_pr(
        self,
        run_summary: Dict[str, Any],
        proposals: List[FeatureProposal],
    ) -> DraftedPR:
        """Generate a PR for an agent run with proposals.

        Args:
            run_summary: Summary of the agent run
            proposals: List of proposals from the run

        Returns:
            Drafted pull request for the agent run
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        branch_name = f"{self.branch_prefix}agent-run-{timestamp}"

        body = self._build_agent_run_body(run_summary, proposals)

        labels = ["agent-generated", "needs-review"]
        if all(p.f2p_compliant for p in proposals):
            labels.append("f2p-approved")

        return DraftedPR(
            title=f"feat: Agent-generated proposals ({len(proposals)} features)",
            body=body,
            labels=labels,
            head_branch=branch_name,
        )

    def _generate_branch_name(self, proposal: FeatureProposal) -> str:
        """Generate a branch name from a proposal.

        Args:
            proposal: Feature proposal

        Returns:
            Suggested branch name
        """
        # Sanitize title for branch name
        safe_title = proposal.title.lower()
        safe_title = "".join(c if c.isalnum() or c == " " else "" for c in safe_title)
        safe_title = "-".join(safe_title.split())[:40]

        return f"{self.branch_prefix}{proposal.category}/{safe_title}"

    def _build_proposal_pr_body(
        self,
        proposal: FeatureProposal,
        related_issues: Optional[List[int]] = None,
    ) -> str:
        """Build PR body for a proposal.

        Args:
            proposal: Feature proposal
            related_issues: Related issue numbers

        Returns:
            Formatted markdown body
        """
        body = f"""## Description

{proposal.description}

## Feature Details

| Attribute | Value |
|-----------|-------|
| Category | {proposal.category} |
| Priority | {proposal.priority:.2f} |
| Monetization | {proposal.monetization_type} |
| F2P Compliant | {'✅ Yes' if proposal.f2p_compliant else '❌ Needs Review'} |

"""

        if related_issues:
            body += "## Related Issues\n\n"
            for issue in related_issues:
                body += f"- Closes #{issue}\n"
            body += "\n"

        if proposal.comparative_notes:
            body += "## Competitive Analysis Notes\n\n"
            for note in proposal.comparative_notes:
                body += f"- {note}\n"
            body += "\n"

        if proposal.guardrail_notes:
            body += "## ⚠️ Guardrail Warnings\n\n"
            for note in proposal.guardrail_notes:
                body += f"- {note}\n"
            body += "\n"

        body += """## Checklist

### Implementation
- [ ] Feature implemented as specified
- [ ] Unit tests added
- [ ] Integration tests added (if applicable)
- [ ] Documentation updated

### F2P Compliance
- [ ] No gameplay advantages for paid content
- [ ] Cosmetic-only monetization verified
- [ ] Fair progression maintained
- [ ] No predatory mechanics

### Review
- [ ] Code reviewed
- [ ] F2P guardrails validated
- [ ] UX reviewed
- [ ] Performance tested

---

*This PR was generated by the Thirsty's Game Studio Agent System.*
"""

        return body

    def _build_agent_run_body(
        self,
        run_summary: Dict[str, Any],
        proposals: List[FeatureProposal],
    ) -> str:
        """Build PR body for an agent run.

        Args:
            run_summary: Summary of the agent run
            proposals: List of proposals

        Returns:
            Formatted markdown body
        """
        body = """## Agent Run Summary

This PR contains feature proposals generated from community feedback analysis.

### Run Statistics

"""
        if run_summary:
            body += f"- **Total Insights Analyzed:** {run_summary.get('total_insights', 'N/A')}\n"
            body += f"- **Proposals Generated:** {len(proposals)}\n"

            if "summary" in run_summary:
                summary = run_summary["summary"]
                body += f"- **Average Sentiment:** {summary.get('avg_sentiment', 0):.2f}\n"
                body += f"- **Sources:** {', '.join(summary.get('sources', {}).keys())}\n"

        body += "\n### Proposals\n\n"

        for i, proposal in enumerate(proposals, 1):
            status = "✅" if proposal.f2p_compliant else "⚠️"
            body += f"{i}. {status} **{proposal.title}**\n"
            body += f"   - Category: {proposal.category}\n"
            body += f"   - Priority: {proposal.priority:.2f}\n"
            body += f"   - Monetization: {proposal.monetization_type}\n\n"

        compliant_count = sum(1 for p in proposals if p.f2p_compliant)
        body += f"""
### F2P Compliance

- **Compliant:** {compliant_count}/{len(proposals)}
- **Status:** {'✅ All proposals are F2P compliant' if compliant_count == len(proposals) else '⚠️ Some proposals need review'}

## Artifacts

This PR includes:
- `output/community_insights.json` - Raw community insights
- `output/proposals.json` - Generated feature proposals
- `output/agent_run_summary.json` - Full run summary

## Review Checklist

- [ ] All proposals reviewed for F2P compliance
- [ ] Community sentiment verified
- [ ] Proposals prioritized correctly
- [ ] No pay-to-win mechanics
- [ ] Artifacts validated

---

*This PR was auto-generated by the Thirsty's Game Studio Agent System.*
"""

        return body

    def batch_generate(
        self, proposals: List[FeatureProposal]
    ) -> List[DraftedPR]:
        """Generate PR drafts for multiple proposals.

        Args:
            proposals: List of feature proposals

        Returns:
            List of drafted PRs
        """
        return [self.generate_from_proposal(p) for p in proposals]
