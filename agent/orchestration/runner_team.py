"""Team runner for executing the full agent pipeline.

This module provides the high-level interface for running the
complete agent team cycle, producing outputs for consumption
by the mobile app and CI/CD systems.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from agent.orchestration.manager import AgentManager
from agent.monetization.guardrails import F2P_POLICY
from agent.prs.templates import PRTemplateGenerator

logger = logging.getLogger(__name__)


class TeamRunner:
    """High-level runner for the agent team.

    Executes the full agent pipeline and produces output artifacts
    for consumption by the mobile app and CI systems.

    Attributes:
        manager: Agent manager instance
        output_dir: Directory for output artifacts
    """

    def __init__(self, output_dir: str = "output"):
        """Initialize the team runner.

        Args:
            output_dir: Directory to write output artifacts
        """
        self.manager = AgentManager()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run(self) -> Dict[str, Any]:
        """Run the full agent team pipeline.

        Returns:
            Run summary with paths to generated artifacts
        """
        logger.info("=" * 60)
        logger.info("Starting Thirsty's Game Studio Agent Team Run")
        logger.info("=" * 60)

        # Initialize workers
        self.manager.initialize_workers()

        # Create and run the full pipeline
        self.manager.create_full_pipeline()
        run_summary = self.manager.run_all()

        # Save artifacts
        artifact_paths = self._save_artifacts(run_summary)

        # Generate PR template if successful
        if run_summary.get("failed", 0) == 0:
            pr_path = self._generate_pr_template(run_summary)
            artifact_paths["pr_template"] = pr_path

        run_summary["artifact_paths"] = artifact_paths

        logger.info("=" * 60)
        logger.info("Agent Team Run Complete")
        logger.info(
            f"Results: {run_summary['successful']} successful, "
            f"{run_summary['failed']} failed"
        )
        logger.info("=" * 60)

        return run_summary

    def _save_artifacts(self, run_summary: Dict[str, Any]) -> Dict[str, str]:
        """Save output artifacts to files.

        Args:
            run_summary: Summary from the run

        Returns:
            Dictionary of artifact type to file path
        """
        paths = {}
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        # Save run summary
        summary_path = self.output_dir / f"run_summary_{timestamp}.json"
        with open(summary_path, "w") as f:
            # Remove non-serializable items
            safe_summary = self._make_json_safe(run_summary)
            json.dump(safe_summary, f, indent=2, default=str)
        paths["run_summary"] = str(summary_path)

        # Also save as latest for app consumption
        latest_summary = self.output_dir / "latest_run_summary.json"
        with open(latest_summary, "w") as f:
            json.dump(safe_summary, f, indent=2, default=str)
        paths["latest_summary"] = str(latest_summary)

        # Save proposals if available
        output_data = run_summary.get("output_data", {})
        if "proposals" in output_data:
            proposals_path = self.output_dir / "proposals.json"
            with open(proposals_path, "w") as f:
                json.dump(output_data["proposals"], f, indent=2)
            paths["proposals"] = str(proposals_path)

        # Save insights if available
        if "insights" in output_data:
            insights_path = self.output_dir / "community_insights.json"
            with open(insights_path, "w") as f:
                json.dump(output_data["insights"], f, indent=2)
            paths["insights"] = str(insights_path)

        # Save issues if available
        if "issues" in output_data:
            issues_path = self.output_dir / "drafted_issues.json"
            with open(issues_path, "w") as f:
                json.dump(output_data["issues"], f, indent=2)
            paths["issues"] = str(issues_path)

        # Save F2P policy for app
        policy_path = self.output_dir / "f2p_policy.md"
        with open(policy_path, "w") as f:
            f.write(F2P_POLICY)
        paths["f2p_policy"] = str(policy_path)

        # Create app data bundle
        app_data = self._create_app_data_bundle(run_summary)
        app_data_path = self.output_dir / "app_data.json"
        with open(app_data_path, "w") as f:
            json.dump(app_data, f, indent=2)
        paths["app_data"] = str(app_data_path)

        logger.info(f"Saved {len(paths)} artifacts to {self.output_dir}")
        return paths

    def _create_app_data_bundle(self, run_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Create a data bundle for the mobile app.

        Args:
            run_summary: Summary from the run

        Returns:
            App-friendly data bundle
        """
        output_data = run_summary.get("output_data", {})

        # Extract top proposals
        proposals = output_data.get("proposals", [])
        top_proposals = proposals[:10] if proposals else []

        # Extract insights summary
        summary = output_data.get("summary", {})

        return {
            "version": "1.0.0",
            "generated_at": datetime.utcnow().isoformat(),
            "insights_summary": {
                "total_count": summary.get("count", 0),
                "avg_sentiment": summary.get("avg_sentiment", 0),
                "top_topics": summary.get("top_topics", []),
                "sources": list(summary.get("sources", {}).keys()),
            },
            "proposals": [
                {
                    "title": p.get("title", ""),
                    "description": p.get("description", ""),
                    "category": p.get("category", ""),
                    "priority": p.get("priority", 0),
                    "f2p_compliant": p.get("f2p_compliant", True),
                }
                for p in top_proposals
            ],
            "f2p_policy_summary": {
                "core_principles": [
                    "No pay-to-win mechanics",
                    "Cosmetic-only purchases",
                    "Fair progression for all",
                    "No predatory mechanics",
                ],
                "what_we_offer": [
                    "Cosmetic items (skins, outfits, effects)",
                    "Quality of life features",
                    "Battle pass with cosmetic rewards",
                ],
                "what_we_never_do": [
                    "Sell gameplay advantages",
                    "Use loot boxes with valuable items",
                    "Create artificial time pressure",
                ],
            },
            "storefront_items": [
                {
                    "id": "skin_001",
                    "name": "Golden Knight Armor",
                    "type": "cosmetic",
                    "price": 500,
                    "currency": "gems",
                    "description": "A dazzling golden armor set. Purely cosmetic.",
                },
                {
                    "id": "emote_001",
                    "name": "Victory Dance",
                    "type": "emote",
                    "price": 200,
                    "currency": "gems",
                    "description": "Celebrate your wins in style!",
                },
                {
                    "id": "bundle_001",
                    "name": "Starter Cosmetic Bundle",
                    "type": "bundle",
                    "price": 1000,
                    "currency": "gems",
                    "description": "3 skins + 2 emotes. Great value!",
                },
            ],
        }

    def _generate_pr_template(self, run_summary: Dict[str, Any]) -> str:
        """Generate a PR template from the run results.

        Args:
            run_summary: Summary from the run

        Returns:
            Path to generated PR template
        """
        from agent.core.interfaces import FeatureProposal

        output_data = run_summary.get("output_data", {})
        proposals_data = output_data.get("proposals", [])

        proposals = []
        for p_data in proposals_data:
            try:
                proposals.append(FeatureProposal.from_dict(p_data))
            except Exception:
                logger.exception(f"Failed to create FeatureProposal from data: {p_data}")

        generator = PRTemplateGenerator()
        pr = generator.generate_agent_run_pr(run_summary, proposals)

        pr_path = self.output_dir / "pr_template.md"
        with open(pr_path, "w") as f:
            f.write(pr.to_markdown())

        return str(pr_path)

    def _make_json_safe(self, obj: Any) -> Any:
        """Make an object JSON-serializable.

        Args:
            obj: Object to convert

        Returns:
            JSON-safe version of the object
        """
        if isinstance(obj, dict):
            return {k: self._make_json_safe(v) for k, v in obj.items() if not k.startswith("raw_")}
        elif isinstance(obj, list):
            return [self._make_json_safe(v) for v in obj]
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, "to_dict"):
            return obj.to_dict()
        else:
            return obj


def run_team() -> Dict[str, Any]:
    """Convenience function to run the agent team.

    Returns:
        Run summary
    """
    runner = TeamRunner()
    return runner.run()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    result = run_team()
    print(f"Run completed with {result['successful']} successful tasks")
