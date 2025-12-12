# 📦 Simple CSV Storage API

A FastAPI-based service that lets users upload, store, and download CSV files.


This project is built with:

- [FastAPI](https://fastapi.tiangolo.com/) – for the web API
- [uv](https://github.com/astral-sh/uv) – for Python dependency and environment management
- [Alembic](https://alembic.sqlalchemy.org/) – for database migrations
- [Taskfile](https://taskfile.dev/) – to simplify common commands (like setup, running, and testing)

> ‼️ **You don’t need to worry about installing or configuring those manually** as Taskfile takes care of everything for you
>  👉 Follow the steps in [🚀 Getting Started](#getting-started)

## 🚀 Getting Started

- ✅ 1. Install Task (if you haven’t already). Installation guide → [https://taskfile.dev/installation](https://taskfile.dev/installation)
- ✅ 2. Run setup to install all dependencies and prepares database:
```bash
task setup
```
- ✅ Once the project is initialized, you can run the app with:

```bash
task dev
```

### Pre-commit (Pre-push) Setup

This repository uses `pre-commit` to run CI-like checks locally before pushing code. The checks mirror the GitHub Actions workflow and help catch issues early.

To install pre-commit hooks (one-time setup):
```bash
# Make sure project dependencies installed:
uv sync --locked --all-extras --dev

# Install pre-commit:
uv run pre-commit install --hook-type pre-push
```

To manually run the pre-push (without pushing):

```bash
uv run pre-commit run --hook-stage pre-push --all-files
```

### 🧪 Run Tests

Tests are written with `pytest` and can be run with:

```bash
task test
```

## 📚 API Endpoints

Full interactive API docs are available at:

- [http://localhost:8000/docs](http://localhost:8000/docs) – Swagger UI
- [http://localhost:8000/redoc](http://localhost:8000/redoc) – ReDoc

## 📊 Log Telemetry Analysis

A helper script is included to analyze performance telemetry logs saved by the app. By default, the script reads all `.jsonl` log files in the `logs/` directory and compute request count and average processing time per endpoint. Run the script directly from the project root:

```bash
uv run scripts/log_telemetry_stats.py
```