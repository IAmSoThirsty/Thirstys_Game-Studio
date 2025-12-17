"""GitHub Actions workflow generator.

This module provides utilities for generating GitHub Actions
workflow files for the agent team automation.
"""

from pathlib import Path
from typing import Optional


class WorkflowGenerator:
    """Generator for GitHub Actions workflow files.

    Creates workflow YAML files for automating the agent team
    pipeline in GitHub Actions.
    """

    def __init__(self, output_dir: str = ".github/workflows"):
        """Initialize the workflow generator.

        Args:
            output_dir: Directory to write workflow files
        """
        self.output_dir = Path(output_dir)

    def generate_agent_team_workflow(self, output_path: Optional[str] = None) -> str:
        """Generate the agent team workflow YAML.

        Args:
            output_path: Optional path to write the workflow

        Returns:
            The workflow YAML content
        """
        workflow = '''name: Agent Team Cycle

on:
  schedule:
    # Run daily at 6 AM UTC
    - cron: '0 6 * * *'
  workflow_dispatch:
    inputs:
      output_dir:
        description: 'Output directory for artifacts'
        required: false
        default: 'output'

jobs:
  run-agent-team:
    runs-on: ubuntu-latest
    
    permissions:
      contents: write
      issues: write
      pull-requests: write
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt || true
      
      - name: Run Agent Team
        env:
          # Community API credentials (set these as repository secrets)
          REDDIT_CLIENT_ID: ${{ secrets.REDDIT_CLIENT_ID }}
          REDDIT_CLIENT_SECRET: ${{ secrets.REDDIT_CLIENT_SECRET }}
          REDDIT_USER_AGENT: 'ThirstysGameStudio/1.0'
          DISCORD_BOT_TOKEN: ${{ secrets.DISCORD_BOT_TOKEN }}
          DISCORD_GUILD_ID: ${{ secrets.DISCORD_GUILD_ID }}
          STEAM_API_KEY: ${{ secrets.STEAM_API_KEY }}
          STEAM_APP_ID: ${{ secrets.STEAM_APP_ID }}
        run: |
          python -m agent.runner --output-dir ${{ github.event.inputs.output_dir || 'output' }}
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: agent-outputs-${{ github.run_number }}
          path: output/
          retention-days: 30
      
      - name: Commit outputs (if any changes)
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add output/
          git diff --staged --quiet || git commit -m "chore: update agent outputs [skip ci]"
          git push || true

'''
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w") as f:
                f.write(workflow)

        return workflow

    def generate_android_build_workflow(self, output_path: Optional[str] = None) -> str:
        """Generate the Android build workflow YAML.

        Args:
            output_path: Optional path to write the workflow

        Returns:
            The workflow YAML content
        """
        workflow = '''name: Android Build

on:
  push:
    branches: [ main, develop ]
    paths:
      - 'android/**'
      - '.github/workflows/android_build.yml'
  pull_request:
    branches: [ main ]
    paths:
      - 'android/**'
  release:
    types: [ created ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
          cache: 'gradle'
      
      - name: Grant execute permission for gradlew
        run: chmod +x android/ThirstysGame/gradlew
      
      - name: Run unit tests
        working-directory: android/ThirstysGame
        run: ./gradlew test
      
      - name: Build Debug APK
        working-directory: android/ThirstysGame
        run: ./gradlew assembleDebug
      
      - name: Upload Debug APK
        uses: actions/upload-artifact@v4
        with:
          name: debug-apk-${{ github.run_number }}
          path: android/ThirstysGame/app/build/outputs/apk/debug/*.apk
          retention-days: 14
      
      - name: Build Release Bundle (on release or main)
        if: github.event_name == 'release' || github.ref == 'refs/heads/main'
        working-directory: android/ThirstysGame
        run: ./gradlew bundleRelease
        env:
          # Keystore credentials for signing (set as repository secrets)
          KEYSTORE_BASE64: ${{ secrets.KEYSTORE_BASE64 }}
          KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
          KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
          KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
      
      - name: Upload Release AAB
        if: github.event_name == 'release' || github.ref == 'refs/heads/main'
        uses: actions/upload-artifact@v4
        with:
          name: release-aab-${{ github.run_number }}
          path: android/ThirstysGame/app/build/outputs/bundle/release/*.aab
          retention-days: 30
  
  release:
    needs: build
    runs-on: ubuntu-latest
    if: github.event_name == 'release'
    
    steps:
      - name: Download Release AAB
        uses: actions/download-artifact@v4
        with:
          name: release-aab-${{ github.run_number }}
          path: ./release
      
      - name: Upload to GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: ./release/*.aab
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

'''
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w") as f:
                f.write(workflow)

        return workflow

    def generate_all(self) -> None:
        """Generate all workflow files."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.generate_agent_team_workflow(
            str(self.output_dir / "agent_team.yml")
        )
        self.generate_android_build_workflow(
            str(self.output_dir / "android_build.yml")
        )


if __name__ == "__main__":
    generator = WorkflowGenerator()
    generator.generate_all()
    print("Workflow files generated successfully!")
