#!/usr/bin/env python3
"""Main runner for the Thirsty's Game Studio agent system.

This script runs the complete agent team pipeline for community
insights analysis, feature proposal generation, and artifact creation.
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

from agent.orchestration.runner_team import TeamRunner


def main():
    """Main entry point for the agent runner."""
    parser = argparse.ArgumentParser(
        description="Thirsty's Game Studio Agent Runner"
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory for output artifacts (default: output)",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)",
    )
    parser.add_argument(
        "--json-output",
        action="store_true",
        help="Output results as JSON to stdout",
    )

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logger = logging.getLogger(__name__)
    logger.info("Thirsty's Game Studio Agent Runner")
    logger.info(f"Output directory: {args.output_dir}")

    try:
        # Run the agent team
        runner = TeamRunner(output_dir=args.output_dir)
        result = runner.run()

        # Print results
        if args.json_output:
            print(json.dumps(result, indent=2, default=str))
        else:
            print("\n" + "=" * 60)
            print("Agent Team Run Complete!")
            print("=" * 60)
            print(f"Successful tasks: {result['successful']}")
            print(f"Failed tasks: {result['failed']}")
            print(f"Total execution time: {result['total_execution_time']:.2f}s")
            print("\nGenerated artifacts:")
            for name, path in result.get("artifact_paths", {}).items():
                print(f"  - {name}: {path}")
            print("=" * 60)

        return 0 if result["failed"] == 0 else 1

    except Exception as e:
        logger.exception(f"Agent run failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
