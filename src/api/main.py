"""FastAPI entry point for the workforce planning backend."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import APP_DEBUG, APP_ENV
from src.config import ADMIN_EMAIL, ADMIN_NAME, ADMIN_PASSWORD
from src.auth.security import hash_password
from src.database import connection, initialise_database
from src.api.auth_routes import admin_router, router as auth_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialise_database()
    seed_admin()
    yield


app = FastAPI(
    title="Workforce Planner API",
    version="0.1.0",
    debug=APP_DEBUG,
    lifespan=lifespan,
)
app.include_router(auth_router)
app.include_router(admin_router)


def seed_admin() -> None:
    """Create the first Admin only when explicit credentials are configured."""
    if not ADMIN_EMAIL or not ADMIN_PASSWORD:
        return
    with connection() as conn:
        existing = conn.execute("SELECT id FROM users WHERE email = ? COLLATE NOCASE", (ADMIN_EMAIL.strip(),)).fetchone()
        if existing is None:
            conn.execute(
                "INSERT INTO users (email, password_hash, full_name, role) VALUES (?, ?, ?, 'admin')",
                (ADMIN_EMAIL.strip(), hash_password(ADMIN_PASSWORD), ADMIN_NAME.strip()),
            )


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Return service and database readiness information."""
    with connection() as conn:
        conn.execute("SELECT 1").fetchone()
    return {"status": "ok", "environment": APP_ENV, "database": "ok"}
