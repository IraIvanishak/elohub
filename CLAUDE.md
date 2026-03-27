# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SkillBoard (elohub) is a Python Flask app that aggregates user achievements from multiple platforms (Chess.com, GitHub) into a unified profile with a composite Power Score (0-1000), league ranks, and head-to-head comparisons. It uses server-rendered Jinja2 templates with no frontend JS framework.

## Tech Stack

- **Language:** Python 3.9+
- **Framework:** Flask 3.1 with Flask-SQLAlchemy, Flask-Login, Flask-WTF
- **Database:** SQLite (default, configurable via `SQLALCHEMY_DATABASE_URI`)
- **Auth:** bcrypt password hashing, session-based auth via Flask-Login
- **External APIs:** Chess.com public API, GitHub REST API (optional token for higher rate limits)
- **Testing/Linting:** Not yet configured

## Commands

```bash
# Run the dev server (port 8000, debug mode)
python run.py

# Install dependencies
pip install -r requirements.txt
```

## Conventions

- **snake_case** everywhere: filenames, functions, variables, URL slugs (e.g., `chess_com`, `power_score`)
- **Services are plain functions**, not classes (e.g., `register_user()`, `authenticate()`) — except where state is needed (custom exceptions as classes)
- **Platform adapters are classes** subclassing `PlatformAdapter`, one per file in `app/platforms/`
- **Routes** use Flask Blueprints named `<domain>_bp` (e.g., `auth_bp`, `profile_bp`), one blueprint per file in `app/routes/`
- **Module docstrings** on service and adapter files; no inline comments unless non-obvious
- **Explicit tablenames** on models (`__tablename__ = "users"`)
- **No type annotations** on model fields or route handlers; type hints used selectively on adapter methods

## Architecture

**App factory pattern** in `app/__init__.py` — creates Flask app, registers blueprints, initializes extensions (SQLAlchemy, Flask-Login, CSRF).

### Platform Adapter Pattern

The core extensibility mechanism. Each platform integration follows:

1. **`app/platforms/base.py`** — Abstract `PlatformAdapter` with `fetch(username)` and `compute_scores(data)` methods
2. **Concrete adapters** in `app/platforms/` (e.g., `chess_com.py`, `github.py`) — each implements fetching from external APIs and scoring via percentile curves
3. **Registry** in `app/platforms/__init__.py` — auto-discovers adapters; use `register()`, `get_adapter(slug)`, `all_adapters()`

To add a new platform: create a new adapter file, subclass `PlatformAdapter`, implement `fetch`/`compute_scores`, and call `register()`.

### Service Layer

Business logic lives in `app/services/`, not in routes:
- **`user_service.py`** — registration, authentication
- **`profile_service.py`** — connect/disconnect platforms, refresh data (handles caching + graceful API failure)
- **`compare_service.py`** — head-to-head comparison across shared platforms

### Data Model

- **User** — auth fields + computed `power_score` property (average across all platform scores) and `league` property (Bronze through Legend thresholds)
- **PlatformAccount** — links user to a platform username; stores `cached_data` (raw API JSON) and `scores` (computed metrics + power_score) with TTL-based cache freshness (1 hour default)

### Routes (Blueprints)

Four blueprints in `app/routes/`: `auth`, `profile`, `leaderboard`, `compare`. Templates in `app/templates/` use Jinja2.

### Seeding

`seed.py` auto-populates 3 demo users on app start if the DB is empty (useful for in-memory SQLite during development).

## Key Design Decisions

- Scoring uses **logistic/logarithmic percentile approximations** rather than real population data — keeps it self-contained without needing external percentile APIs
- **Cached API responses** are stored in the DB so profiles render even when external APIs are down
- Server-rendered templates only (no frontend JS framework); static asset dirs exist but are empty
