# Thirsty's Game Studio

A community-driven game development platform featuring multi-agent orchestration for community insights, feature proposal generation, and a deployable Android application.

## 🎮 Features

- **Multi-Agent Platform**: Python-based orchestration system for processing community feedback
- **Community Insights**: Aggregates data from Reddit, Discord, and Steam
- **Feature Proposals**: AI-generated feature suggestions based on community sentiment
- **F2P Guardrails**: Enforces ethical monetization (no pay-to-win)
- **Android App**: Ready-to-deploy mobile app with Jetpack Compose UI
- **CI/CD Automation**: GitHub Actions for daily agent runs and Android builds

## 📁 Project Structure

```
├── agent/                    # Python multi-agent platform
│   ├── core/                 # Core interfaces and abstractions
│   ├── community/            # Community data sources and analyzers
│   ├── monetization/         # F2P guardrail enforcement
│   ├── comparative/          # Competitive analysis utilities
│   ├── orchestration/        # Task and worker management
│   ├── issues/               # GitHub issue drafting
│   └── prs/                  # PR template generation
├── android/ThirstysGame/     # Android Kotlin/Compose app
├── dotnet/AgentPlugin/       # C# interface for Unity integration
├── cpp/include/              # C++ interface for Unreal/custom engines
├── web/plugin/               # TypeScript interface for web games
├── docs/                     # Documentation
└── .github/workflows/        # CI/CD workflows
```

## 🚀 Quick Start

### Run the Agent Pipeline

```bash
# Run the full agent team cycle
python -m agent.runner --output-dir output

# Results will be in output/
```

### Build Android App

```bash
cd android/ThirstysGame
./gradlew assembleDebug
```

## 📱 Android App

The Android app displays community insights, feature proposals, and a cosmetic storefront. See [android/ThirstysGame/README.md](android/ThirstysGame/README.md) for build and deployment instructions.

## 🤖 Agent System

The multi-agent system processes community feedback through these stages:

1. **Community Analysis** - Fetch from Reddit, Discord, Steam
2. **NLP Processing** - Sentiment analysis and topic extraction
3. **Proposal Generation** - Create feature proposals
4. **Monetization Review** - F2P compliance validation
5. **Competitive Analysis** - Compare with Age of Origins, etc.
6. **Artifact Generation** - Create GitHub issues and PR templates

See [docs/TEAM_AGENT_DESIGN.md](docs/TEAM_AGENT_DESIGN.md) for architecture details.

## 🛡️ F2P Philosophy

We're committed to ethical free-to-play:

- ✅ Cosmetic-only purchases
- ✅ Fair progression for all
- ✅ Transparent odds
- ❌ No pay-to-win
- ❌ No loot boxes
- ❌ No FOMO tactics

## 🔧 CI/CD

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `agent_team.yml` | Daily/Manual | Run agent pipeline |
| `android_build.yml` | Push/Release | Build Android APK/AAB |

## 📖 Documentation

- [Team Agent Design](docs/TEAM_AGENT_DESIGN.md) - Architecture and flow
- [Android README](android/ThirstysGame/README.md) - Build and deployment

## 🔐 Configuration

API keys should be set as GitHub Secrets:
- `REDDIT_CLIENT_ID` / `REDDIT_CLIENT_SECRET`
- `DISCORD_BOT_TOKEN` / `DISCORD_GUILD_ID`
- `STEAM_API_KEY` / `STEAM_APP_ID`
- `KEYSTORE_*` (for Android signing)

## License

Copyright © 2024 Thirsty's Game Studio
