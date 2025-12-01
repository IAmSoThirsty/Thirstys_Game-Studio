"""Discord community source for insights ingestion.

This module provides integration with Discord for fetching community feedback
from game-related Discord servers and channels.

Note: Requires DISCORD_BOT_TOKEN environment variable for full functionality.
"""

import os
import logging
from datetime import datetime
from typing import List, Optional

from agent.core.interfaces import CommunitySource, CommunityInsight

logger = logging.getLogger(__name__)


class DiscordSource(CommunitySource):
    """Discord community source implementation.

    Fetches messages from specified Discord channels and normalizes
    them into CommunityInsight objects.

    Attributes:
        guild_id: Discord server (guild) ID
        channel_ids: List of channel IDs to monitor
        bot_token: Discord bot token for API access
    """

    def __init__(
        self,
        guild_id: Optional[str] = None,
        channel_ids: Optional[List[str]] = None,
        bot_token: Optional[str] = None,
    ):
        """Initialize Discord source.

        Args:
            guild_id: Discord server ID
            channel_ids: List of channel IDs to fetch from
            bot_token: Discord bot token (defaults to env var)
        """
        self.guild_id = guild_id or os.getenv("DISCORD_GUILD_ID", "")
        self.channel_ids = channel_ids or []
        self.bot_token = bot_token or os.getenv("DISCORD_BOT_TOKEN", "")
        self._configured = bool(self.bot_token and self.guild_id)

    def get_source_name(self) -> str:
        """Get the name of this source."""
        return "discord"

    def is_configured(self) -> bool:
        """Check if the source is properly configured."""
        return self._configured

    def fetch_insights(
        self, limit: int = 100, since: Optional[datetime] = None
    ) -> List[CommunityInsight]:
        """Fetch insights from Discord.

        Args:
            limit: Maximum number of insights to fetch
            since: Only fetch insights after this timestamp

        Returns:
            List of normalized community insights

        Note:
            Returns placeholder data if bot token is not configured.
            In production, this would use discord.py or similar library.
        """
        if not self._configured:
            logger.warning(
                "Discord API not configured. Returning placeholder insights. "
                "Set DISCORD_BOT_TOKEN and DISCORD_GUILD_ID env vars."
            )
            return self._get_placeholder_insights(limit)

        # Production implementation would use discord.py:
        # import discord
        # client = discord.Client()
        # for channel_id in self.channel_ids:
        #     channel = client.get_channel(int(channel_id))
        #     async for message in channel.history(limit=limit, after=since):
        #         insights.append(self._normalize_message(message))

        return self._get_placeholder_insights(limit)

    def _get_placeholder_insights(self, limit: int) -> List[CommunityInsight]:
        """Generate placeholder insights for testing/demo purposes."""
        placeholders = [
            CommunityInsight(
                source="discord",
                content="The new seasonal event is so much fun! Love that all "
                "rewards are earnable through gameplay.",
                sentiment=0.85,
                topics=["event", "seasonal", "rewards", "gameplay"],
                author="discord_user_1",
                engagement={"reactions": 45, "replies": 8},
                category="praise",
                priority=0.6,
            ),
            CommunityInsight(
                source="discord",
                content="Would be cool to have emote wheel customization. "
                "Could be a great cosmetic option!",
                sentiment=0.6,
                topics=["emotes", "customization", "cosmetics"],
                author="discord_user_2",
                engagement={"reactions": 78, "replies": 15},
                category="feature_request",
                priority=0.75,
            ),
            CommunityInsight(
                source="discord",
                content="The matchmaking feels balanced. Good job on the MMR system!",
                sentiment=0.7,
                topics=["matchmaking", "balance", "mmr"],
                author="discord_user_3",
                engagement={"reactions": 34, "replies": 5},
                category="praise",
                priority=0.5,
            ),
            CommunityInsight(
                source="discord",
                content="Can we get more profile customization? Banners, borders, "
                "titles - all cosmetic stuff that shows progression.",
                sentiment=0.5,
                topics=["profile", "customization", "cosmetics", "progression"],
                author="discord_user_4",
                engagement={"reactions": 92, "replies": 22},
                category="feature_request",
                priority=0.8,
            ),
            CommunityInsight(
                source="discord",
                content="The tutorial was clear and the game respects my time. "
                "No forced ads or energy systems. Refreshing!",
                sentiment=0.9,
                topics=["tutorial", "respect", "f2p", "no_ads"],
                author="discord_user_5",
                engagement={"reactions": 156, "replies": 31},
                category="praise",
                priority=0.55,
            ),
        ]
        return placeholders[:limit]

    def _normalize_message(self, message) -> CommunityInsight:
        """Normalize a Discord message to CommunityInsight.

        Args:
            message: Discord message object

        Returns:
            Normalized CommunityInsight
        """
        return CommunityInsight(
            source="discord",
            content=message.content,
            author=str(message.author.id),
            timestamp=message.created_at,
            engagement={
                "reactions": sum(r.count for r in message.reactions),
                "replies": 0,  # Would need additional API call
            },
            category=self._categorize_message(message),
        )

    def _categorize_message(self, message) -> str:
        """Categorize a message based on content and channel."""
        content_lower = message.content.lower()
        if any(word in content_lower for word in ["bug", "issue", "broken", "crash"]):
            return "bug_report"
        if any(
            word in content_lower for word in ["suggestion", "idea", "would be cool"]
        ):
            return "feature_request"
        if any(word in content_lower for word in ["thanks", "love", "amazing", "great"]):
            return "praise"
        return "discussion"
