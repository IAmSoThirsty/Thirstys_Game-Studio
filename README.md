# Thirstys Game Studio

## Quick Start (Python)

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
