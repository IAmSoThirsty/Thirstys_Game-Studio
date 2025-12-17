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
# Thirsty's Game Studio 🎮

My Repository for game building and advancement.

[![Android CI](https://github.com/IAmSoThirsty/Thirstys_Game-Studio/actions/workflows/android-ci.yml/badge.svg)](https://github.com/IAmSoThirsty/Thirstys_Game-Studio/actions/workflows/android-ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This is an Android game development project built with Kotlin and Android Studio. The project serves as a foundation for creating mobile games and experimenting with game development concepts.

## Requirements

- Android Studio Arctic Fox or later
- JDK 17 or higher
- Android SDK 34 (minimum SDK 24)
- Gradle 8.0+

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/IAmSoThirsty/Thirstys_Game-Studio.git
cd Thirstys_Game-Studio
```

### Build the Project

Open the project in Android Studio and let it sync the Gradle files, or build from command line:

```bash
./gradlew build
```

### Run the App

```bash
./gradlew installDebug
```

Or use Android Studio's Run button to deploy to an emulator or connected device.

### Run Tests

```bash
./gradlew test          # Run unit tests
./gradlew connectedCheck # Run instrumented tests
```

## Project Structure

```
├── app/                    # Main Android application module
│   ├── src/
│   │   ├── main/          # Main source code and resources
│   │   ├── test/          # Unit tests
│   │   └── androidTest/   # Instrumented tests
│   └── build.gradle       # App-level build configuration
├── gradle/                 # Gradle wrapper files
├── build.gradle           # Project-level build configuration
├── settings.gradle        # Project settings
├── .github/workflows/     # CI/CD configuration
├── CONTRIBUTING.md        # Contribution guidelines
└── LICENSE                # MIT License
```

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, please open an issue in this repository.
