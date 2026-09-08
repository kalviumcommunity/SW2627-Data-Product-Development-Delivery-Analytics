"""FastAPI entry point for the workforce planning backend."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import APP_DEBUG, APP_ENV
from src.database import connection, initialise_database


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialise_database()
    yield


app = FastAPI(
    title="Workforce Planner API",
    version="0.1.0",
    debug=APP_DEBUG,
    lifespan=lifespan,
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Return service and database readiness information."""
    with connection() as conn:
        conn.execute("SELECT 1").fetchone()
    return {"status": "ok", "environment": APP_ENV, "database": "ok"}
