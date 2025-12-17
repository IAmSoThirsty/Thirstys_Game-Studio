# Thirsty's Game Studio - Team Agent Design Document

## Overview

The Thirsty's Game Studio Agent System is a multi-agent orchestration platform designed to automate community-driven game development workflows. The system ingests community feedback from multiple sources, analyzes sentiment and topics, generates feature proposals, validates them against F2P (Free-to-Play) monetization guardrails, and produces artifacts for both development workflows and mobile app consumption.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Team Runner                               │
│  Orchestrates the full pipeline and produces output artifacts    │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                        Agent Manager                             │
│  Manages task queues, worker assignment, and result aggregation  │
└───────────────────────────────┬─────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐   ┌───────────────────┐   ┌───────────────────┐
│  Task Queue   │   │   Role Registry   │   │     Workers       │
│  (Priority)   │   │  (Definitions)    │   │  (Execution)      │
└───────────────┘   └───────────────────┘   └───────────────────┘
```

## Agent Roles

### 1. Community Analyst
- **Purpose**: Fetch and analyze community feedback from various sources
- **Inputs**: Community source configurations
- **Outputs**: Normalized insights with sentiment, topics, and priority
- **Sources**: Reddit, Discord, Steam (placeholder implementations)

### 2. Feature Designer
- **Purpose**: Generate feature proposals from analyzed insights
- **Inputs**: Community insights from analyst
- **Outputs**: Feature proposals with categories and monetization types
- **Dependencies**: Community Analyst

### 3. Monetization Reviewer
- **Purpose**: Validate proposals against F2P guardrails
- **Inputs**: Feature proposals
- **Outputs**: Validated proposals with compliance status
- **Dependencies**: Feature Designer
- **Guardrails**:
  - No pay-to-win mechanics
  - Cosmetic-only premium content
  - Fair progression for all players
  - Transparent odds disclosure
  - No loot boxes with valuable items
  - Accessible core content

### 4. Comparative Analyst
- **Purpose**: Enrich proposals with competitive insights
- **Inputs**: Validated proposals
- **Outputs**: Enriched proposals with competitive notes
- **Dependencies**: Monetization Reviewer
- **Focus**: Age of Origins and similar games

### 5. Issue Drafter
- **Purpose**: Create GitHub issue drafts from proposals
- **Inputs**: Enriched proposals
- **Outputs**: Formatted issue drafts
- **Dependencies**: Comparative Analyst

### 6. PR Creator
- **Purpose**: Create PR templates from proposals
- **Inputs**: Enriched proposals
- **Outputs**: Formatted PR templates
- **Dependencies**: Comparative Analyst

## Pipeline Execution Flow

```
1. Community Analysis
   ├── Fetch from Reddit (or placeholder)
   ├── Fetch from Discord (or placeholder)
   ├── Fetch from Steam (or placeholder)
   └── Normalize and analyze with NLP

2. Feature Design
   ├── Extract feature requests
   ├── Group by topic
   └── Generate proposals

3. Monetization Review
   ├── Check all guardrails
   ├── Mark non-compliant proposals
   └── Provide improvement suggestions

4. Comparative Analysis
   ├── Match with competitor features
   ├── Extract best practices
   └── Enrich proposals

5. Issue/PR Drafting
   ├── Format as GitHub issues
   ├── Add labels and milestones
   └── Generate PR templates

6. Output Generation
   ├── Save JSON artifacts
   ├── Generate app data bundle
   └── Create F2P policy file
```

## Monetization Philosophy

### Core Principles
1. **No Pay-to-Win**: Players cannot purchase gameplay advantages
2. **Cosmetic Focus**: Premium content is purely visual
3. **Fair Progression**: All players progress at the same rate
4. **Transparency**: All odds and mechanics are disclosed
5. **Anti-FOMO**: No manipulative time pressure

### Allowed Monetization
- Character skins and outfits
- Weapon visual effects
- Emotes and animations
- Profile customization
- Battle passes (cosmetic rewards only)

### Prohibited Mechanics
- Stat boosts for purchase
- Pay-to-skip progression
- Loot boxes with gameplay items
- VIP systems with advantages
- Time-limited exclusive gameplay content

## Output Artifacts

### For Mobile App
- `app_data.json`: Bundled data for app consumption
- `proposals.json`: Feature proposals list
- `f2p_policy.md`: Policy document

### For Development
- `community_insights.json`: Raw analyzed insights
- `drafted_issues.json`: GitHub issue drafts
- `pr_template.md`: Pull request template
- `run_summary.json`: Pipeline execution report

## CI/CD Integration

### Daily Run Workflow (`agent_team.yml`)
- Scheduled at 6 AM UTC daily
- Manual dispatch available
- Uploads artifacts to GitHub
- Commits outputs to repository

### Android Build Workflow (`android_build.yml`)
- Triggered on push to main/develop
- Runs unit tests
- Builds debug APK
- Builds release AAB on releases
- Uploads build artifacts

## Cross-Language Interfaces

### .NET/C# (`IGamingAgentPlugin.cs`)
- For Unity and other C# game engines
- Async/await pattern support
- Full type safety

### C++ (`IGamingAgentPlugin.h`)
- For Unreal Engine and custom engines
- Both sync and async APIs
- RAII resource management

### TypeScript (`IGamingAgentPlugin.ts`)
- For web games and React Native
- Full TypeScript types
- Event-based architecture

## Configuration

### Required Environment Variables
```
REDDIT_CLIENT_ID          # Reddit API client ID
REDDIT_CLIENT_SECRET      # Reddit API client secret
REDDIT_USER_AGENT         # Reddit API user agent
DISCORD_BOT_TOKEN         # Discord bot token
DISCORD_GUILD_ID          # Discord server ID
STEAM_API_KEY             # Steam Web API key
STEAM_APP_ID              # Steam application ID
```

### Optional Configuration
```
OUTPUT_DIR                # Output directory (default: output)
LOG_LEVEL                 # Logging level (default: INFO)
```

## Running the Agent

### Command Line
```bash
python -m agent.runner --output-dir output --log-level INFO
```

### Programmatic
```python
from agent.orchestration.runner_team import TeamRunner

runner = TeamRunner(output_dir="output")
result = runner.run()
print(f"Generated {len(result['output_data']['proposals'])} proposals")
```

## Future Enhancements

1. **Real API Integration**: Replace placeholders with actual API calls
2. **Machine Learning**: Improve NLP with trained models
3. **Interactive Dashboard**: Web UI for reviewing proposals
4. **Automated Issue Creation**: Direct GitHub integration
5. **A/B Testing**: Track proposal success rates
6. **Multi-Language Support**: Analyze non-English feedback

## Security Considerations

1. API credentials stored as GitHub Secrets
2. No sensitive data in output artifacts
3. Rate limiting on API calls
4. Input sanitization for all user content
5. No executable code in outputs
