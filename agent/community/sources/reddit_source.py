"""Reddit community source for insights ingestion.

This module provides integration with Reddit for fetching community feedback,
feature requests, bug reports, and general discussion from game-related subreddits.

Note: Requires REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT
environment variables or configuration for full functionality.
"""

import os
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any

from agent.core.interfaces import CommunitySource, CommunityInsight

logger = logging.getLogger(__name__)


class RedditSource(CommunitySource):
    """Reddit community source implementation.

    Fetches posts and comments from specified subreddits and normalizes
    them into CommunityInsight objects.

    Attributes:
        subreddits: List of subreddits to monitor
        client_id: Reddit API client ID (from env or config)
        client_secret: Reddit API client secret (from env or config)
        user_agent: Reddit API user agent
    """

    def __init__(
        self,
        subreddits: Optional[List[str]] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        user_agent: Optional[str] = None,
    ):
        """Initialize Reddit source.

        Args:
            subreddits: List of subreddit names to fetch from
            client_id: Reddit API client ID (defaults to env var)
            client_secret: Reddit API client secret (defaults to env var)
            user_agent: Reddit API user agent (defaults to env var)
        """
        self.subreddits = subreddits or ["gamedev", "gaming", "indiegaming"]
        self.client_id = client_id or os.getenv("REDDIT_CLIENT_ID", "")
        self.client_secret = client_secret or os.getenv("REDDIT_CLIENT_SECRET", "")
        self.user_agent = user_agent or os.getenv(
            "REDDIT_USER_AGENT", "ThirstysGameStudio/1.0"
        )
        self._configured = bool(self.client_id and self.client_secret)

    def get_source_name(self) -> str:
        """Get the name of this source."""
        return "reddit"

    def is_configured(self) -> bool:
        """Check if the source is properly configured."""
        return self._configured

    def fetch_insights(
        self, limit: int = 100, since: Optional[datetime] = None
    ) -> List[CommunityInsight]:
        """Fetch insights from Reddit.

        Args:
            limit: Maximum number of insights to fetch
            since: Only fetch insights after this timestamp

        Returns:
            List of normalized community insights

        Note:
            Returns placeholder data if API credentials are not configured.
            In production, this would use the PRAW library to fetch real data.
        """
        if not self._configured:
            logger.warning(
                "Reddit API not configured. Returning placeholder insights. "
                "Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET env vars."
            )
            return self._get_placeholder_insights(limit)

        # Production implementation would use PRAW:
        # import praw
        # reddit = praw.Reddit(
        #     client_id=self.client_id,
        #     client_secret=self.client_secret,
        #     user_agent=self.user_agent
        # )
        # for subreddit_name in self.subreddits:
        #     subreddit = reddit.subreddit(subreddit_name)
        #     for submission in subreddit.hot(limit=limit):
        #         insights.append(self._normalize_submission(submission))

        return self._get_placeholder_insights(limit)

    def _get_placeholder_insights(self, limit: int) -> List[CommunityInsight]:
        """Generate placeholder insights for testing/demo purposes."""
        placeholders = [
            CommunityInsight(
                source="reddit",
                content="Would love to see more character customization options! "
                "Maybe different armor styles that don't affect stats?",
                sentiment=0.7,
                topics=["customization", "cosmetics", "armor"],
                author="reddit_user_1",
                engagement={"upvotes": 145, "comments": 23},
                category="feature_request",
                priority=0.8,
            ),
            CommunityInsight(
                source="reddit",
                content="The new update is amazing! Really appreciate the F2P model.",
                sentiment=0.9,
                topics=["update", "f2p", "appreciation"],
                author="reddit_user_2",
                engagement={"upvotes": 312, "comments": 45},
                category="praise",
                priority=0.6,
            ),
            CommunityInsight(
                source="reddit",
                content="Can we get a guild/clan system? Would make the game "
                "more social without any pay-to-win elements.",
                sentiment=0.5,
                topics=["social", "guild", "clan", "multiplayer"],
                author="reddit_user_3",
                engagement={"upvotes": 256, "comments": 67},
                category="feature_request",
                priority=0.85,
            ),
            CommunityInsight(
                source="reddit",
                content="The battle pass is fair and purely cosmetic. "
                "This is how F2P should be done!",
                sentiment=0.8,
                topics=["battle_pass", "cosmetics", "f2p"],
                author="reddit_user_4",
                engagement={"upvotes": 189, "comments": 12},
                category="praise",
                priority=0.5,
            ),
            CommunityInsight(
                source="reddit",
                content="Suggestion: Add daily challenges for earning cosmetic currency.",
                sentiment=0.6,
                topics=["daily_challenges", "currency", "cosmetics"],
                author="reddit_user_5",
                engagement={"upvotes": 98, "comments": 15},
                category="feature_request",
                priority=0.7,
            ),
        ]
        return placeholders[:limit]

    def _normalize_submission(self, submission: Any) -> CommunityInsight:
        """Normalize a Reddit submission to CommunityInsight.

        Args:
            submission: PRAW submission object

        Returns:
            Normalized CommunityInsight
        """
        # This would be used in production with real PRAW objects
        return CommunityInsight(
            source="reddit",
            content=f"{submission.title}\n\n{submission.selftext}",
            author=str(submission.author) if submission.author else "deleted",
            timestamp=datetime.utcfromtimestamp(submission.created_utc),
            engagement={
                "upvotes": submission.score,
                "comments": submission.num_comments,
            },
            category=self._categorize_submission(submission),
        )

    def _categorize_submission(self, submission: Any) -> str:
        """Categorize a submission based on flair and content."""
        title_lower = submission.title.lower()
        if any(word in title_lower for word in ["bug", "issue", "broken"]):
            return "bug_report"
        if any(word in title_lower for word in ["suggestion", "idea", "request"]):
            return "feature_request"
        if any(word in title_lower for word in ["thank", "love", "amazing"]):
            return "praise"
        return "discussion"
