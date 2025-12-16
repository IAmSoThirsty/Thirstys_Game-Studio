"""Age of Origins competitive analysis module.

This module provides analysis utilities for studying Age of Origins
and similar games to extract best practices and feature inspiration
while ensuring our approach remains F2P-friendly.
"""

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any

from agent.core.interfaces import FeatureProposal

logger = logging.getLogger(__name__)


@dataclass
class CompetitorInsight:
    """Insight derived from competitor analysis.

    Attributes:
        source_game: Name of the competitor game
        feature_category: Category of the feature
        description: Description of the feature
        pros: Positive aspects to potentially adopt
        cons: Negative aspects to avoid
        f2p_adaptable: Whether this can be adapted in F2P-friendly way
        adaptation_notes: Notes on how to adapt for our game
    """

    source_game: str
    feature_category: str
    description: str
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)
    f2p_adaptable: bool = True
    adaptation_notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "source_game": self.source_game,
            "feature_category": self.feature_category,
            "description": self.description,
            "pros": self.pros,
            "cons": self.cons,
            "f2p_adaptable": self.f2p_adaptable,
            "adaptation_notes": self.adaptation_notes,
        }


class AgeOfOriginsAnalyzer:
    """Analyzer for Age of Origins and similar strategy games.

    Provides competitive analysis to inspire features while ensuring
    ethical F2P adaptation.

    Attributes:
        competitor_features: Database of analyzed competitor features
    """

    def __init__(self):
        """Initialize the analyzer with competitor feature database."""
        self.competitor_features = self._load_feature_database()

    def _load_feature_database(self) -> List[CompetitorInsight]:
        """Load the competitor feature database.

        Returns:
            List of competitor insights
        """
        # In production, this would load from a data file or API
        # For now, using curated examples based on public knowledge
        return [
            CompetitorInsight(
                source_game="Age of Origins",
                feature_category="social",
                description="Alliance/Guild System with territory control",
                pros=[
                    "Strong social engagement",
                    "Cooperative gameplay",
                    "Long-term retention",
                ],
                cons=[
                    "Can create power imbalances",
                    "VIP systems give unfair advantages",
                ],
                f2p_adaptable=True,
                adaptation_notes="Implement guild system without pay-to-win "
                "territory bonuses. Focus on cosmetic guild customization.",
            ),
            CompetitorInsight(
                source_game="Age of Origins",
                feature_category="customization",
                description="Commander/Hero customization and skins",
                pros=[
                    "High player attachment",
                    "Good monetization potential",
                    "Visual differentiation",
                ],
                cons=["Often tied to stat bonuses"],
                f2p_adaptable=True,
                adaptation_notes="Offer cosmetic-only commander skins. "
                "Any stat-affecting commanders should be earnable by all.",
            ),
            CompetitorInsight(
                source_game="Age of Origins",
                feature_category="events",
                description="Regular seasonal events with exclusive rewards",
                pros=[
                    "Keeps game fresh",
                    "Engagement spikes",
                    "Community participation",
                ],
                cons=[
                    "FOMO tactics in limited exclusives",
                    "Event passes can be expensive",
                ],
                f2p_adaptable=True,
                adaptation_notes="Run events with cosmetic rewards. "
                "Bring back seasonal items in future. No FOMO pressure.",
            ),
            CompetitorInsight(
                source_game="Age of Origins",
                feature_category="progression",
                description="Multiple progression systems (base, heroes, tech)",
                pros=[
                    "Deep gameplay systems",
                    "Long-term goals",
                    "Varied gameplay",
                ],
                cons=["Can be pay-to-progress faster", "Overwhelming complexity"],
                f2p_adaptable=True,
                adaptation_notes="Multiple progression paths but equal time "
                "investment for all players. No paid speedups.",
            ),
            CompetitorInsight(
                source_game="Age of Origins",
                feature_category="monetization",
                description="VIP system with subscription benefits",
                pros=["Predictable revenue", "Player commitment"],
                cons=[
                    "Creates class divide",
                    "Often includes gameplay advantages",
                ],
                f2p_adaptable=False,
                adaptation_notes="Avoid VIP systems entirely. Use battle pass "
                "with purely cosmetic rewards instead.",
            ),
            CompetitorInsight(
                source_game="Age of Origins",
                feature_category="content",
                description="Regular content updates with new zones/modes",
                pros=[
                    "Keeps game fresh",
                    "New challenges",
                    "Returning players",
                ],
                cons=["New content can invalidate old progression"],
                f2p_adaptable=True,
                adaptation_notes="Regular free content updates. New content "
                "should complement, not replace existing progression.",
            ),
        ]

    def get_insights_for_category(
        self, category: str
    ) -> List[CompetitorInsight]:
        """Get competitor insights for a specific category.

        Args:
            category: Feature category to search for

        Returns:
            List of relevant competitor insights
        """
        return [
            insight
            for insight in self.competitor_features
            if insight.feature_category == category
            or category.lower() in insight.description.lower()
        ]

    def get_f2p_adaptable_insights(self) -> List[CompetitorInsight]:
        """Get all F2P-adaptable competitor insights.

        Returns:
            List of F2P-adaptable insights
        """
        return [i for i in self.competitor_features if i.f2p_adaptable]

    def enrich_proposal(
        self, proposal: FeatureProposal
    ) -> FeatureProposal:
        """Enrich a proposal with competitive analysis.

        Args:
            proposal: Feature proposal to enrich

        Returns:
            Proposal enriched with comparative notes
        """
        # Find relevant competitor insights
        relevant_insights = self.get_insights_for_category(proposal.category)

        if not relevant_insights:
            # Try matching on title/description keywords
            for insight in self.competitor_features:
                if any(
                    word in proposal.description.lower()
                    for word in insight.description.lower().split()
                ):
                    relevant_insights.append(insight)

        # Add comparative notes
        notes = []
        for insight in relevant_insights[:3]:  # Limit to top 3
            if insight.f2p_adaptable:
                notes.append(
                    f"[{insight.source_game}] {insight.feature_category}: "
                    f"{insight.adaptation_notes}"
                )
            else:
                notes.append(
                    f"[{insight.source_game}] AVOID: {insight.description} "
                    f"- not F2P adaptable"
                )

        proposal.comparative_notes.extend(notes)
        return proposal

    def enrich_proposals(
        self, proposals: List[FeatureProposal]
    ) -> List[FeatureProposal]:
        """Enrich multiple proposals with competitive analysis.

        Args:
            proposals: List of proposals to enrich

        Returns:
            List of enriched proposals
        """
        return [self.enrich_proposal(p) for p in proposals]

    def generate_report(self) -> Dict[str, Any]:
        """Generate a competitive analysis report.

        Returns:
            Report dictionary with analysis summary
        """
        adaptable = self.get_f2p_adaptable_insights()
        non_adaptable = [
            i for i in self.competitor_features if not i.f2p_adaptable
        ]

        categories: Dict[str, int] = {}
        for insight in self.competitor_features:
            cat = insight.feature_category
            categories[cat] = categories.get(cat, 0) + 1

        return {
            "total_insights": len(self.competitor_features),
            "f2p_adaptable": len(adaptable),
            "to_avoid": len(non_adaptable),
            "categories": categories,
            "insights": [i.to_dict() for i in self.competitor_features],
            "recommendations": [
                {
                    "category": i.feature_category,
                    "recommendation": i.adaptation_notes,
                }
                for i in adaptable
            ],
            "avoid_patterns": [
                {
                    "feature": i.description,
                    "reason": ", ".join(i.cons),
                }
                for i in non_adaptable
            ],
        }
