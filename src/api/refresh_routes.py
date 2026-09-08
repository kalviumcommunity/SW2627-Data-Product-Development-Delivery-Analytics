"""Admin-only data refresh endpoints."""

from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import require_roles
from src.refresh import refresh_data


router = APIRouter(prefix="/refresh", tags=["refresh"])


@router.post("")
def run_refresh(_: dict = Depends(require_roles("admin"))) -> dict:
    try:
        return refresh_data()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Refresh failed: {exc}") from exc


@router.get("/status")
def refresh_status(_: dict = Depends(require_roles("admin", "manager", "viewer"))) -> dict:
    from src.database import connection

    with connection() as conn:
        row = conn.execute(
            """SELECT id, status, started_at, completed_at, rows_loaded, error_message
               FROM refresh_runs ORDER BY id DESC LIMIT 1"""
        ).fetchone()
    return dict(row) if row else {"status": "never_run"}
