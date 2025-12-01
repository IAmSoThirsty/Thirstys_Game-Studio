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
