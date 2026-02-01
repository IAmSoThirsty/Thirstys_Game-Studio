# Thirstys Game Studio

## 🎮 TWO PRODUCTION-READY GAMES!

### 1. Energy Empire - Addictive Idle Game ⚡
**Thirsty's Game - Energy Empire** is a production-ready incremental/idle game with exceptional architecture and addictive gameplay!

### 2. Survival Shooter - Multiplayer Co-op Action 🔫
**NEW!** **Thirsty's Survival Shooter** is a production-grade multiplayer survival shooter with:
- 4-player co-op PvE with 100+ player scalability
- 4 unique classes, 6 themed zones
- Wave-based survival with zone control
- Full marketplace with cosmetics
- Kubernetes-ready deployment

**[📖 See Survival Shooter Documentation →](SURVIVAL_SHOOTER.md)**

## 🚀 **END-TO-END DEPLOYABLE** - One Command Deployment

Deploy the complete stack with a single command:

```bash
make deploy-all
```

This deploys:
- ✅ Game server (headless mode)
- ✅ Agent system (community insights)
- ✅ Persistent storage
- ✅ Health monitoring
- ✅ Auto-scaling (Kubernetes)
- ✅ Complete monitoring

**See [DEPLOYMENT_COMPLETE.md](DEPLOYMENT_COMPLETE.md) for full deployment guide.**

## Quick Start (Game)

1. **Install and Run:**
   ```bash
   git clone https://github.com/IAmSoThirsty/Thirstys_Game-Studio.git
   cd Thirstys_Game-Studio
   pip install -r requirements.txt
   python main.py
   ```

2. **Play the Game:**
   - Click the center orb to generate energy
   - Press Q/W/E/R to purchase producers
   - Press S to save your progress
   - Build an energy empire!

## 🌟 Game Features

- **Addictive Incremental Mechanics**: Click-based and idle generation
- **Multiple Resource Types**: Energy → Crystals → Essence
- **Achievement System**: Unlock rewards and multipliers
- **Beautiful Particle Effects**: Smooth 60 FPS animations
- **Save/Load System**: Never lose your progress
- **F2P Friendly**: No pay-to-win, fair progression
- **52 Passing Tests**: Production-quality code

See [docs/GAME_GUIDE.md](docs/GAME_GUIDE.md) for complete game documentation.

---

## Quick Start (Python Agent)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/IAmSoThirsty/Thirstys_Game-Studio.git
   cd Thirstys_Game-Studio
   ```
2. **Set up a Python virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt  # or use `pip install .` if using pyproject.toml
   ```
4. **Run the application:**
   ```bash
   python main.py
   ```
   The main entrypoint is `app.main()` as defined in `main.py`.

---

## Running with Docker

1. **Build the Docker image:**
   ```bash
   docker build -t thirstys-game-studio .
   ```
2. **Run the container:**
   ```bash
   docker run --rm -p 8000:8000 thirstys-game-studio
   ```

---

## Running with Docker Compose

1. **Start all services:**
   ```bash
   docker-compose up --build
   ```
2. **Stop services:**
   ```bash
   docker-compose down
   ```

---

## Dependency & Environment Setup

- Python dependencies are listed in `requirements.txt` or defined in `pyproject.toml`.
- Ensure your environment variables are properly set. If an `.env` sample is present, copy it with:
  ```bash
  cp .env.example .env
  ```
- Minimum Python version: 3.8+

---

## Running Tests & Continuous Integration

- **Manual testing:**
  ```bash
  make test
  ```
  or directly via pytest:
  ```bash
  pytest tests/
  ```
- The `Makefile` includes convenient shortcuts for linting, testing, and CI tasks. To see all options, run:
  ```bash
  make help
  ```
- Automated tests are located in the `tests` directory. Make sure to run all tests before submitting changes.

---

For further development or contribution guidelines, please refer to `CONTRIBUTING.md` if available.
