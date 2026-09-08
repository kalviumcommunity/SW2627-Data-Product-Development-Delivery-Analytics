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
