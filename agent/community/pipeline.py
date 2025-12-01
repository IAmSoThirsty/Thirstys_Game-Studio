"""Community insights pipeline for aggregating and processing community data.

This module provides the main pipeline for ingesting, normalizing, analyzing,
and aggregating community insights from multiple sources.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from agent.core.interfaces import CommunityInsight, FeatureProposal
from agent.community.sources import RedditSource, DiscordSource, SteamSource
from agent.community.analyzers.nlp import NLPAnalyzer

logger = logging.getLogger(__name__)


class CommunityPipeline:
    """Pipeline for processing community insights from multiple sources.

    Coordinates fetching from multiple community sources, analyzing insights,
    aggregating results, and generating feature proposals.

    Attributes:
        sources: List of community sources to fetch from
        analyzer: NLP analyzer for processing insights
        insights: Collected and processed insights
    """

    def __init__(
        self,
        enable_reddit: bool = True,
        enable_discord: bool = True,
        enable_steam: bool = True,
    ):
        """Initialize the community pipeline.

        Args:
            enable_reddit: Whether to include Reddit source
            enable_discord: Whether to include Discord source
            enable_steam: Whether to include Steam source
        """
        self.sources = []
        if enable_reddit:
            self.sources.append(RedditSource())
        if enable_discord:
            self.sources.append(DiscordSource())
        if enable_steam:
            self.sources.append(SteamSource())

        self.analyzer = NLPAnalyzer()
        self.insights: List[CommunityInsight] = []

    def run(
        self, limit_per_source: int = 50, since: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Run the full community insights pipeline.

        Args:
            limit_per_source: Maximum insights to fetch per source
            since: Only fetch insights after this timestamp

        Returns:
            Dictionary with pipeline results including insights and summary
        """
        logger.info("Starting community pipeline run")

        # Fetch from all sources
        all_insights: List[CommunityInsight] = []
        for source in self.sources:
            try:
                source_insights = source.fetch_insights(
                    limit=limit_per_source, since=since
                )
                logger.info(
                    f"Fetched {len(source_insights)} insights from {source.get_source_name()}"
                )
                all_insights.extend(source_insights)
            except Exception as e:
                logger.error(f"Error fetching from {source.get_source_name()}: {e}")

        # Analyze all insights
        self.insights = self.analyzer.batch_analyze(all_insights)
        logger.info(f"Analyzed {len(self.insights)} total insights")

        # Generate summary
        summary = self.analyzer.summarize_insights(self.insights)

        # Extract and prioritize feature requests
        feature_requests = self._extract_feature_requests()

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "total_insights": len(self.insights),
            "summary": summary,
            "feature_requests": [fr.to_dict() for fr in feature_requests],
            "insights": [i.to_dict() for i in self.insights],
        }

    def _extract_feature_requests(self) -> List[CommunityInsight]:
        """Extract and prioritize feature request insights.

        Returns:
            List of feature request insights sorted by priority
        """
        feature_requests = [
            i for i in self.insights if i.category == "feature_request"
        ]
        return sorted(feature_requests, key=lambda x: x.priority, reverse=True)

    def generate_proposals(self) -> List[FeatureProposal]:
        """Generate feature proposals from analyzed insights.

        Returns:
            List of feature proposals derived from community insights
        """
        feature_requests = self._extract_feature_requests()
        proposals: List[FeatureProposal] = []

        # Group similar feature requests by topic
        topic_groups: Dict[str, List[CommunityInsight]] = {}
        for fr in feature_requests:
            primary_topic = fr.topics[0] if fr.topics else "general"
            if primary_topic not in topic_groups:
                topic_groups[primary_topic] = []
            topic_groups[primary_topic].append(fr)

        # Generate proposals for each topic group
        for topic, requests in topic_groups.items():
            if len(requests) >= 1:  # At least 1 request
                proposal = self._create_proposal_from_requests(topic, requests)
                proposals.append(proposal)

        return sorted(proposals, key=lambda x: x.priority, reverse=True)

    def _create_proposal_from_requests(
        self, topic: str, requests: List[CommunityInsight]
    ) -> FeatureProposal:
        """Create a feature proposal from grouped requests.

        Args:
            topic: Primary topic for the proposal
            requests: List of related community insights

        Returns:
            FeatureProposal synthesized from the requests
        """
        # Calculate aggregate priority
        avg_priority = sum(r.priority for r in requests) / len(requests)
        avg_sentiment = sum(r.sentiment for r in requests) / len(requests)

        # Determine monetization type based on topic
        monetization_type = self._determine_monetization_type(topic)

        # Create descriptive title and description
        title = f"Community-Requested: Enhanced {topic.replace('_', ' ').title()}"
        description = self._synthesize_description(requests)

        return FeatureProposal(
            title=title,
            description=description,
            source_insights=[str(hash(r.content)) for r in requests],
            category=topic,
            monetization_type=monetization_type,
            priority=avg_priority * (1 + avg_sentiment * 0.2),  # Boost by sentiment
            f2p_compliant=True,  # Will be validated by guardrails
        )

    def _determine_monetization_type(self, topic: str) -> str:
        """Determine appropriate monetization type for a topic.

        Args:
            topic: Feature topic

        Returns:
            Monetization type string
        """
        cosmetic_topics = {"customization", "cosmetics", "social", "events"}
        free_topics = {"gameplay", "performance", "balance", "content"}

        if topic in cosmetic_topics:
            return "cosmetic"
        elif topic in free_topics:
            return "free"
        else:
            return "qol"  # Quality of life

    def _synthesize_description(self, requests: List[CommunityInsight]) -> str:
        """Synthesize a description from multiple requests.

        Args:
            requests: List of related community insights

        Returns:
            Synthesized description
        """
        # Take key points from top requests
        top_requests = sorted(requests, key=lambda x: x.priority, reverse=True)[:3]

        points = []
        for req in top_requests:
            # Extract first sentence or truncate
            content = req.content
            if "." in content:
                content = content.split(".")[0] + "."
            if len(content) > 200:
                content = content[:197] + "..."
            points.append(f"- {content}")

        community_input = "\n".join(points)

        return f"""Based on community feedback from {len(requests)} users:

{community_input}

This feature would enhance the player experience while maintaining our F2P-friendly approach.
Engagement metrics suggest high community interest in this area."""

    def save_results(self, output_path: str = "output/community_insights.json") -> str:
        """Save pipeline results to a JSON file.

        Args:
            output_path: Path to save the output file

        Returns:
            Path to the saved file
        """
        # Ensure output directory exists
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Run pipeline if not already run
        if not self.insights:
            results = self.run()
        else:
            results = {
                "timestamp": datetime.utcnow().isoformat(),
                "total_insights": len(self.insights),
                "summary": self.analyzer.summarize_insights(self.insights),
                "insights": [i.to_dict() for i in self.insights],
            }

        # Add proposals to results
        proposals = self.generate_proposals()
        results["proposals"] = [p.to_dict() for p in proposals]

        # Save to file
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2, default=str)

        logger.info(f"Saved pipeline results to {output_file}")
        return str(output_file)


def run_pipeline() -> Dict[str, Any]:
    """Convenience function to run the community pipeline.

    Returns:
        Pipeline results dictionary
    """
    pipeline = CommunityPipeline()
    return pipeline.run()
