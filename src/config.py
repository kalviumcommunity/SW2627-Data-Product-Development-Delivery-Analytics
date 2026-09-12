"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def _project_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else PROJECT_ROOT / path


DATABASE_PATH = _project_path(os.getenv("DATABASE_PATH", "data/app.db"))
APP_ENV = os.getenv("APP_ENV", "development")
APP_DEBUG = os.getenv("APP_DEBUG", "true").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
RAW_DATA_PATH = _project_path(os.getenv("RAW_DATA_PATH", "data/raw"))
PROCESSED_DATA_PATH = _project_path(os.getenv("PROCESSED_DATA_PATH", "data/processed"))
OUTPUT_PATH = _project_path(os.getenv("OUTPUT_PATH", "output"))
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))
JWT_SECRET = os.getenv("JWT_SECRET", "development-only-change-me")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")
ADMIN_NAME = os.getenv("ADMIN_NAME", "System Administrator")


def validate_security_config() -> None:
    """Reject missing or development-grade credentials outside development."""
    if APP_ENV.lower() not in {"production", "staging"}:
        return

    problems = []
    if APP_DEBUG:
        problems.append("APP_DEBUG must be false")
    if len(JWT_SECRET) < 32 or JWT_SECRET in {"development-only-change-me", "replace-with-a-long-random-secret"}:
        problems.append("JWT_SECRET must be a unique value of at least 32 characters")
    if not ADMIN_EMAIL.strip():
        problems.append("ADMIN_EMAIL is required")
    if (
        len(ADMIN_PASSWORD) < 12
        or ADMIN_PASSWORD == "replace-with-a-secure-password"
        or ADMIN_PASSWORD.casefold() == ADMIN_EMAIL.strip().casefold()
    ):
        problems.append("ADMIN_PASSWORD must be a unique value of at least 12 characters")

    if problems:
        raise RuntimeError("Invalid production security configuration: " + "; ".join(problems))
