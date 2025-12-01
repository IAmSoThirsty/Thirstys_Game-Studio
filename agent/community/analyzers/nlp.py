"""NLP-based analyzer for community insights.

This module provides natural language processing capabilities for analyzing
community insights, including sentiment analysis, topic extraction, and
categorization.
"""

import re
import logging
from typing import List, Dict, Tuple

from agent.core.interfaces import Analyzer, CommunityInsight

logger = logging.getLogger(__name__)


class NLPAnalyzer(Analyzer):
    """NLP-based community insight analyzer.

    Provides sentiment analysis, topic extraction, and categorization
    for community insights using simple rule-based NLP.

    For production use, this could be enhanced with:
    - spaCy for advanced NLP
    - TextBlob for sentiment analysis
    - Transformers for topic modeling

    Attributes:
        positive_words: Set of positive sentiment words
        negative_words: Set of negative sentiment words
        topic_keywords: Mapping of topics to their keywords
    """

    def __init__(self):
        """Initialize NLP analyzer with sentiment lexicons and topic mappings."""
        self.positive_words = {
            "love",
            "great",
            "amazing",
            "excellent",
            "awesome",
            "fantastic",
            "perfect",
            "best",
            "fun",
            "enjoy",
            "wonderful",
            "brilliant",
            "superb",
            "outstanding",
            "incredible",
            "thanks",
            "thank",
            "appreciate",
            "helpful",
            "beautiful",
            "cool",
            "nice",
            "good",
        }

        self.negative_words = {
            "hate",
            "bad",
            "terrible",
            "awful",
            "horrible",
            "worst",
            "boring",
            "frustrating",
            "annoying",
            "broken",
            "buggy",
            "crash",
            "laggy",
            "unfair",
            "expensive",
            "scam",
            "p2w",
            "pay-to-win",
            "greedy",
            "garbage",
            "trash",
            "disappointed",
        }

        self.topic_keywords: Dict[str, List[str]] = {
            "customization": [
                "customization",
                "customize",
                "custom",
                "personalize",
                "skins",
                "outfits",
            ],
            "cosmetics": [
                "cosmetic",
                "cosmetics",
                "skin",
                "outfit",
                "appearance",
                "visual",
            ],
            "gameplay": [
                "gameplay",
                "mechanics",
                "combat",
                "movement",
                "controls",
            ],
            "social": ["guild", "clan", "friends", "chat", "party", "team", "social"],
            "monetization": [
                "shop",
                "store",
                "buy",
                "purchase",
                "price",
                "cost",
                "f2p",
                "free",
            ],
            "progression": [
                "level",
                "xp",
                "unlock",
                "progression",
                "grind",
                "earn",
                "reward",
            ],
            "events": ["event", "season", "seasonal", "battle pass", "limited"],
            "performance": ["lag", "fps", "performance", "crash", "bug", "optimization"],
            "balance": ["balance", "nerf", "buff", "overpowered", "underpowered", "op"],
            "content": ["content", "update", "new", "feature", "addition", "map", "mode"],
        }

        self.category_patterns = {
            "feature_request": [
                r"\bwould love\b",
                r"\bshould add\b",
                r"\bcan we get\b",
                r"\bsuggestion\b",
                r"\bidea\b",
                r"\brequest\b",
                r"\bwish\b",
                r"\bplease add\b",
            ],
            "bug_report": [
                r"\bbug\b",
                r"\bcrash\b",
                r"\bbroken\b",
                r"\bissue\b",
                r"\bglitch\b",
                r"\berror\b",
                r"\bnot working\b",
            ],
            "praise": [
                r"\blove this\b",
                r"\bamazing\b",
                r"\bgreat job\b",
                r"\bthank you\b",
                r"\bawesome\b",
                r"\bbest game\b",
            ],
            "complaint": [
                r"\bhate\b",
                r"\bterrible\b",
                r"\bworst\b",
                r"\bunfair\b",
                r"\brunfun\b",
            ],
        }

    def analyze(self, insight: CommunityInsight) -> CommunityInsight:
        """Analyze and enrich a community insight.

        Args:
            insight: Raw insight to analyze

        Returns:
            Enriched insight with sentiment, topics, and category
        """
        # Calculate sentiment if not already set or seems default
        if insight.sentiment == 0.0:
            insight.sentiment = self._analyze_sentiment(insight.content)

        # Extract topics if not already set
        if not insight.topics:
            insight.topics = self._extract_topics(insight.content)

        # Categorize if not already set or seems default
        if insight.category == "general":
            insight.category = self._categorize(insight.content)

        # Calculate priority based on engagement and sentiment
        insight.priority = self._calculate_priority(insight)

        return insight

    def _analyze_sentiment(self, text: str) -> float:
        """Analyze sentiment of text.

        Args:
            text: Text to analyze

        Returns:
            Sentiment score from -1.0 (negative) to 1.0 (positive)
        """
        words = text.lower().split()
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)

        total = positive_count + negative_count
        if total == 0:
            return 0.0

        # Calculate normalized sentiment score
        score = (positive_count - negative_count) / total
        return max(-1.0, min(1.0, score))

    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics from text.

        Args:
            text: Text to analyze

        Returns:
            List of extracted topics
        """
        text_lower = text.lower()
        found_topics = []

        for topic, keywords in self.topic_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    found_topics.append(topic)
                    break

        return found_topics if found_topics else ["general"]

    def _categorize(self, text: str) -> str:
        """Categorize text based on patterns.

        Args:
            text: Text to categorize

        Returns:
            Category string
        """
        text_lower = text.lower()

        for category, patterns in self.category_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return category

        return "discussion"

    def _calculate_priority(self, insight: CommunityInsight) -> float:
        """Calculate priority score for an insight.

        Args:
            insight: Insight to score

        Returns:
            Priority score from 0.0 to 1.0
        """
        # Base priority from engagement
        total_engagement = sum(insight.engagement.values())
        engagement_score = min(1.0, total_engagement / 500)

        # Boost for feature requests
        category_multiplier = 1.2 if insight.category == "feature_request" else 1.0

        # Boost for positive sentiment (people want more of good things)
        sentiment_boost = 0.1 if insight.sentiment > 0.5 else 0

        priority = (engagement_score * category_multiplier + sentiment_boost) / 1.3
        return min(1.0, max(0.0, priority))

    def batch_analyze(
        self, insights: List[CommunityInsight]
    ) -> List[CommunityInsight]:
        """Analyze multiple insights.

        Args:
            insights: List of insights to analyze

        Returns:
            List of analyzed insights
        """
        return [self.analyze(insight) for insight in insights]

    def summarize_insights(
        self, insights: List[CommunityInsight]
    ) -> Dict[str, any]:
        """Generate a summary of analyzed insights.

        Args:
            insights: List of analyzed insights

        Returns:
            Summary dictionary with aggregated metrics
        """
        if not insights:
            return {"count": 0}

        categories: Dict[str, int] = {}
        topics: Dict[str, int] = {}
        sentiments: List[float] = []
        sources: Dict[str, int] = {}

        for insight in insights:
            categories[insight.category] = categories.get(insight.category, 0) + 1
            sources[insight.source] = sources.get(insight.source, 0) + 1
            sentiments.append(insight.sentiment)

            for topic in insight.topics:
                topics[topic] = topics.get(topic, 0) + 1

        return {
            "count": len(insights),
            "avg_sentiment": sum(sentiments) / len(sentiments),
            "categories": categories,
            "top_topics": sorted(topics.items(), key=lambda x: x[1], reverse=True)[:10],
            "sources": sources,
            "feature_requests": [
                i for i in insights if i.category == "feature_request"
            ],
        }
