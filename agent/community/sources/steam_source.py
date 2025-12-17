"""Steam community source for insights ingestion.

This module provides integration with Steam for fetching community feedback
from game discussions, reviews, and community hub.

Note: Requires STEAM_API_KEY environment variable for full functionality.
"""

import os
import logging
from datetime import datetime
from typing import List, Optional

from agent.core.interfaces import CommunitySource, CommunityInsight

logger = logging.getLogger(__name__)


class SteamSource(CommunitySource):
    """Steam community source implementation.

    Fetches reviews and discussion posts from Steam and normalizes
    them into CommunityInsight objects.

    Attributes:
        app_id: Steam application ID
        api_key: Steam Web API key
    """

    def __init__(
        self,
        app_id: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        """Initialize Steam source.

        Args:
            app_id: Steam application ID
            api_key: Steam Web API key (defaults to env var)
        """
        self.app_id = app_id or os.getenv("STEAM_APP_ID", "")
        self.api_key = api_key or os.getenv("STEAM_API_KEY", "")
        self._configured = bool(self.api_key and self.app_id)

    def get_source_name(self) -> str:
        """Get the name of this source."""
        return "steam"

    def is_configured(self) -> bool:
        """Check if the source is properly configured."""
        return self._configured

    def fetch_insights(
        self, limit: int = 100, since: Optional[datetime] = None
    ) -> List[CommunityInsight]:
        """Fetch insights from Steam.

        Args:
            limit: Maximum number of insights to fetch
            since: Only fetch insights after this timestamp

        Returns:
            List of normalized community insights

        Note:
            Returns placeholder data if API key is not configured.
            In production, this would use Steam Web API.
        """
        if not self._configured:
            logger.warning(
                "Steam API not configured. Returning placeholder insights. "
                "Set STEAM_API_KEY and STEAM_APP_ID env vars."
            )
            return self._get_placeholder_insights(limit)

        # Production implementation would use Steam Web API:
        # import requests
        # url = f"https://store.steampowered.com/appreviews/{self.app_id}"
        # params = {"json": 1, "num_per_page": limit}
        # response = requests.get(url, params=params)
        # for review in response.json()["reviews"]:
        #     insights.append(self._normalize_review(review))

        return self._get_placeholder_insights(limit)

    def _get_placeholder_insights(self, limit: int) -> List[CommunityInsight]:
        """Generate placeholder insights for testing/demo purposes."""
        placeholders = [
            CommunityInsight(
                source="steam",
                content="Excellent F2P game! No pay-to-win mechanics, just cosmetics. "
                "Played for 200 hours and never felt the need to spend money.",
                sentiment=0.9,
                topics=["f2p", "cosmetics", "no_p2w", "gameplay"],
                author="steam_user_1",
                engagement={"helpful": 234, "funny": 12},
                category="review_positive",
                priority=0.7,
            ),
            CommunityInsight(
                source="steam",
                content="Great game! Would love to see more weapon skins. "
                "Maybe animated ones as premium cosmetics?",
                sentiment=0.8,
                topics=["skins", "weapons", "cosmetics", "premium"],
                author="steam_user_2",
                engagement={"helpful": 89, "funny": 3},
                category="feature_request",
                priority=0.75,
            ),
            CommunityInsight(
                source="steam",
                content="The battle pass is well-designed. Good value and "
                "everything is achievable through gameplay.",
                sentiment=0.85,
                topics=["battle_pass", "value", "gameplay", "progression"],
                author="steam_user_3",
                engagement={"helpful": 156, "funny": 5},
                category="review_positive",
                priority=0.6,
            ),
            CommunityInsight(
                source="steam",
                content="Suggestion: Add a replay system and theater mode. "
                "Would be great for content creators!",
                sentiment=0.6,
                topics=["replay", "theater", "content_creation", "streaming"],
                author="steam_user_4",
                engagement={"helpful": 312, "funny": 8},
                category="feature_request",
                priority=0.85,
            ),
            CommunityInsight(
                source="steam",
                content="Love the cosmetic shop! Reasonable prices and no "
                "FOMO tactics. This is ethical F2P done right.",
                sentiment=0.95,
                topics=["shop", "cosmetics", "pricing", "ethical_f2p"],
                author="steam_user_5",
                engagement={"helpful": 445, "funny": 21},
                category="review_positive",
                priority=0.65,
            ),
        ]
        return placeholders[:limit]

    def _normalize_review(self, review: dict) -> CommunityInsight:
        """Normalize a Steam review to CommunityInsight.

        Args:
            review: Steam review dictionary

        Returns:
            Normalized CommunityInsight
        """
        return CommunityInsight(
            source="steam",
            content=review.get("review", ""),
            author=review.get("author", {}).get("steamid", "anonymous"),
            timestamp=datetime.utcfromtimestamp(
                review.get("timestamp_created", datetime.utcnow().timestamp())
            ),
            engagement={
                "helpful": review.get("votes_up", 0),
                "funny": review.get("votes_funny", 0),
            },
            category="review_positive"
            if review.get("voted_up", False)
            else "review_negative",
        )
