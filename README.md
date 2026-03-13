# 📦 Simple CSV Storage API

A FastAPI-based service that lets users upload, store, and download CSV files.


This project is built with:

- [FastAPI](https://fastapi.tiangolo.com/) – for the web API
- [Docker Compose](https://docs.docker.com/compose/) – for running the development environment  
- [uv](https://github.com/astral-sh/uv) – for Python dependency and environment management
- [Alembic](https://alembic.sqlalchemy.org/) – for database migrations
- [Taskfile](https://taskfile.dev/) – to simplify common commands (like setup, running, and testing)

> ‼️ **You don’t need to worry about installing or configuring those manually** as Docker and Taskfile take care of everything for you
>  👉 Follow the steps in [🚀 Getting Started](#getting-started)

## 🚀 Getting Started

### 1. Install prerequisites

Make sure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Task](https://taskfile.dev/installation)

---

### 2. Start the development environment

Run:

```bash
task dev
```
This will:
- Build the Docker image
- Start the backend container
- Automatically run database migrations
- Start the FastAPI server

Once running, the API will be available at:
```
http://localhost:8000
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