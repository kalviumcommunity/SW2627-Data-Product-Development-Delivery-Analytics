"""FastAPI dependencies for authenticated and role-protected routes."""

from __future__ import annotations

from typing import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.auth.security import decode_access_token
from src.database import connection


bearer = HTTPBearer(auto_error=False)


def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)) -> dict:
    """Resolve the active database user represented by a bearer token."""
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token") from exc

    with connection() as conn:
        row = conn.execute(
            "SELECT id, email, full_name, role, is_active, created_at FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
    if row is None or not row["is_active"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is inactive or not found")
    return dict(row)


def require_roles(*roles: str) -> Callable:
    """Build a dependency requiring one of the supplied roles."""
    def dependency(user: dict = Depends(get_current_user)) -> dict:
        if user["role"] not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user

    return dependency
