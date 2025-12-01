"""Monetization guardrails for ensuring F2P-friendly feature proposals.

This module provides guardrail checks to ensure all feature proposals
comply with ethical F2P monetization principles, specifically:
- No pay-to-win mechanics
- Cosmetic-only premium content
- Fair progression for all players
- Transparent pricing and odds
"""

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any

from agent.core.interfaces import FeatureProposal, MonetizationGuardrail

logger = logging.getLogger(__name__)


# F2P Policy statement for display in app
F2P_POLICY = """
# Thirsty's Game Studio F2P Policy

We believe games should be fun for everyone, regardless of how much they spend.
Our monetization philosophy is built on these core principles:

## ✅ What We DO Offer

### Cosmetic Items
- Character skins and outfits
- Weapon skins and visual effects
- Emotes and animations
- Profile customization (banners, borders, titles)
- Visual-only pets and companions

### Quality of Life Features
- Additional cosmetic loadout slots
- Extended profile customization options
- Social features and emotes

### Battle Pass (Seasonal)
- Purely cosmetic rewards
- All gameplay-relevant content available for free
- Reasonable progression achievable through normal play

## ❌ What We NEVER Do

### No Pay-to-Win
- No stat boosts or gameplay advantages for purchase
- No exclusive weapons or abilities behind paywalls
- No faster progression through purchases

### No Predatory Mechanics
- No loot boxes with random valuable items
- No hidden odds or manipulative pricing
- No artificial time-gates that can be skipped with money

### No FOMO Tactics
- No countdown timers on purchase decisions
- Seasonal items return in future seasons
- No pressure sales or manipulation

## Our Commitment

Every player, free or paying, has the same gameplay experience.
Paying supports development and gets you cool cosmetics - nothing more.
"""


@dataclass
class GuardrailResult:
    """Result of a guardrail check.

    Attributes:
        passed: Whether the proposal passed the check
        guardrail: The guardrail that was checked
        message: Detailed message about the result
        suggestions: Suggestions for making the proposal compliant
    """

    passed: bool
    guardrail: MonetizationGuardrail
    message: str
    suggestions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "passed": self.passed,
            "guardrail": self.guardrail.value,
            "message": self.message,
            "suggestions": self.suggestions,
        }


class MonetizationGuardrailChecker:
    """Checker for monetization guardrails on feature proposals.

    Validates that feature proposals comply with F2P-friendly monetization
    principles and provides feedback for non-compliant proposals.

    Attributes:
        pay_to_win_keywords: Keywords indicating pay-to-win mechanics
        allowed_monetization_types: Monetization types that are acceptable
    """

    def __init__(self):
        """Initialize the guardrail checker."""
        self.pay_to_win_keywords = {
            "stat boost",
            "power boost",
            "damage increase",
            "health increase",
            "speed boost",
            "advantage",
            "stronger",
            "faster",
            "more powerful",
            "exclusive weapon",
            "exclusive ability",
            "pay for power",
            "buy advantage",
            "premium stats",
            "vip bonus",
            "skip grind",
            "instant unlock",
            "pay to skip",
        }

        self.predatory_keywords = {
            "loot box",
            "gacha",
            "random chance",
            "mystery box",
            "limited time only",
            "last chance",
            "countdown",
            "expires soon",
            "fomo",
            "exclusive forever",
        }

        self.allowed_monetization_types = {
            "free",
            "cosmetic",
            "qol",
            "battle_pass",
        }

    def check_proposal(self, proposal: FeatureProposal) -> List[GuardrailResult]:
        """Check a proposal against all guardrails.

        Args:
            proposal: The feature proposal to check

        Returns:
            List of guardrail check results
        """
        results = [
            self._check_pay_to_win(proposal),
            self._check_cosmetic_only(proposal),
            self._check_no_gameplay_advantage(proposal),
            self._check_fair_progression(proposal),
            self._check_transparent_odds(proposal),
            self._check_no_loot_boxes(proposal),
            self._check_accessible_content(proposal),
        ]

        # Update proposal based on results
        proposal.f2p_compliant = all(r.passed for r in results)
        proposal.guardrail_notes = [r.message for r in results if not r.passed]

        return results

    def _check_pay_to_win(self, proposal: FeatureProposal) -> GuardrailResult:
        """Check for pay-to-win mechanics."""
        content = f"{proposal.title} {proposal.description}".lower()

        found_keywords = [kw for kw in self.pay_to_win_keywords if kw in content]

        if found_keywords:
            return GuardrailResult(
                passed=False,
                guardrail=MonetizationGuardrail.NO_PAY_TO_WIN,
                message=f"Pay-to-win indicators found: {', '.join(found_keywords)}",
                suggestions=[
                    "Remove any gameplay advantages from paid content",
                    "Make all gameplay-affecting content available for free",
                    "Convert to cosmetic-only if visual aspect is involved",
                ],
            )

        return GuardrailResult(
            passed=True,
            guardrail=MonetizationGuardrail.NO_PAY_TO_WIN,
            message="No pay-to-win mechanics detected",
        )

    def _check_cosmetic_only(self, proposal: FeatureProposal) -> GuardrailResult:
        """Check if monetized content is cosmetic only."""
        if proposal.monetization_type not in self.allowed_monetization_types:
            return GuardrailResult(
                passed=False,
                guardrail=MonetizationGuardrail.COSMETIC_ONLY,
                message=f"Invalid monetization type: {proposal.monetization_type}",
                suggestions=[
                    "Use 'free', 'cosmetic', 'qol', or 'battle_pass' as monetization type",
                    "Ensure any paid content is purely visual or quality-of-life",
                ],
            )

        return GuardrailResult(
            passed=True,
            guardrail=MonetizationGuardrail.COSMETIC_ONLY,
            message="Monetization type is acceptable",
        )

    def _check_no_gameplay_advantage(self, proposal: FeatureProposal) -> GuardrailResult:
        """Check for gameplay advantages in paid content."""
        if proposal.monetization_type == "free":
            return GuardrailResult(
                passed=True,
                guardrail=MonetizationGuardrail.NO_GAMEPLAY_ADVANTAGE,
                message="Free content - no gameplay advantage concerns",
            )

        # Check for gameplay-affecting categories
        gameplay_categories = {"gameplay", "balance", "combat", "abilities", "weapons"}
        if proposal.category in gameplay_categories:
            return GuardrailResult(
                passed=False,
                guardrail=MonetizationGuardrail.NO_GAMEPLAY_ADVANTAGE,
                message=f"Gameplay-affecting category '{proposal.category}' with paid monetization",
                suggestions=[
                    "Make gameplay-affecting features free for all players",
                    "Separate visual aspects (can be paid) from functional aspects (must be free)",
                ],
            )

        return GuardrailResult(
            passed=True,
            guardrail=MonetizationGuardrail.NO_GAMEPLAY_ADVANTAGE,
            message="No gameplay advantage in paid content",
        )

    def _check_fair_progression(self, proposal: FeatureProposal) -> GuardrailResult:
        """Check for fair progression mechanics."""
        content = f"{proposal.title} {proposal.description}".lower()

        unfair_keywords = ["skip grind", "instant unlock", "pay to skip", "faster xp"]
        found_keywords = [kw for kw in unfair_keywords if kw in content]

        if found_keywords:
            return GuardrailResult(
                passed=False,
                guardrail=MonetizationGuardrail.FAIR_PROGRESSION,
                message=f"Unfair progression indicators: {', '.join(found_keywords)}",
                suggestions=[
                    "Remove pay-to-skip mechanics",
                    "Ensure all players progress at the same rate",
                    "Consider cosmetic rewards instead of progression shortcuts",
                ],
            )

        return GuardrailResult(
            passed=True,
            guardrail=MonetizationGuardrail.FAIR_PROGRESSION,
            message="Progression appears fair for all players",
        )

    def _check_transparent_odds(self, proposal: FeatureProposal) -> GuardrailResult:
        """Check for transparent odds in any random elements."""
        content = f"{proposal.title} {proposal.description}".lower()

        if "random" in content or "chance" in content:
            if "odds" not in content and "probability" not in content:
                return GuardrailResult(
                    passed=False,
                    guardrail=MonetizationGuardrail.TRANSPARENT_ODDS,
                    message="Random elements detected but no mention of transparent odds",
                    suggestions=[
                        "Add clear odds disclosure for any random elements",
                        "Consider removing random elements entirely",
                        "Display exact probabilities to players",
                    ],
                )

        return GuardrailResult(
            passed=True,
            guardrail=MonetizationGuardrail.TRANSPARENT_ODDS,
            message="No undisclosed random elements",
        )

    def _check_no_loot_boxes(self, proposal: FeatureProposal) -> GuardrailResult:
        """Check for loot box or gacha mechanics."""
        content = f"{proposal.title} {proposal.description}".lower()

        lootbox_keywords = ["loot box", "gacha", "mystery box", "random reward box"]
        found_keywords = [kw for kw in lootbox_keywords if kw in content]

        if found_keywords:
            return GuardrailResult(
                passed=False,
                guardrail=MonetizationGuardrail.NO_LOOT_BOXES,
                message=f"Loot box mechanics detected: {', '.join(found_keywords)}",
                suggestions=[
                    "Replace random rewards with direct purchase options",
                    "If randomness is desired, make it free/earnable only",
                    "Consider battle pass with guaranteed rewards instead",
                ],
            )

        return GuardrailResult(
            passed=True,
            guardrail=MonetizationGuardrail.NO_LOOT_BOXES,
            message="No loot box mechanics detected",
        )

    def _check_accessible_content(self, proposal: FeatureProposal) -> GuardrailResult:
        """Check that core content is accessible to all players."""
        content = f"{proposal.title} {proposal.description}".lower()

        exclusive_keywords = ["exclusive", "vip only", "premium only", "paid players only"]
        found_keywords = [kw for kw in exclusive_keywords if kw in content]

        # Check if exclusivity is for cosmetics (allowed) or gameplay (not allowed)
        if found_keywords:
            if proposal.monetization_type == "cosmetic":
                return GuardrailResult(
                    passed=True,
                    guardrail=MonetizationGuardrail.ACCESSIBLE_CONTENT,
                    message="Exclusive content is cosmetic-only - acceptable",
                )
            else:
                return GuardrailResult(
                    passed=False,
                    guardrail=MonetizationGuardrail.ACCESSIBLE_CONTENT,
                    message=f"Non-cosmetic exclusive content detected: {', '.join(found_keywords)}",
                    suggestions=[
                        "Make gameplay content available to all players",
                        "Limit exclusivity to cosmetic items only",
                    ],
                )

        return GuardrailResult(
            passed=True,
            guardrail=MonetizationGuardrail.ACCESSIBLE_CONTENT,
            message="Core content appears accessible to all players",
        )

    def validate_proposals(
        self, proposals: List[FeatureProposal]
    ) -> Dict[str, Any]:
        """Validate multiple proposals and return summary.

        Args:
            proposals: List of proposals to validate

        Returns:
            Validation summary with results for each proposal
        """
        results = []
        compliant_count = 0

        for proposal in proposals:
            checks = self.check_proposal(proposal)
            all_passed = all(c.passed for c in checks)
            if all_passed:
                compliant_count += 1

            results.append({
                "proposal_title": proposal.title,
                "f2p_compliant": all_passed,
                "checks": [c.to_dict() for c in checks],
            })

        return {
            "total_proposals": len(proposals),
            "compliant_proposals": compliant_count,
            "compliance_rate": compliant_count / len(proposals) if proposals else 1.0,
            "results": results,
        }
