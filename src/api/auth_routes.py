"""Authentication and Admin user-management endpoints."""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from src.api.dependencies import get_current_user, require_roles
from src.auth.security import create_access_token, hash_password, verify_password
from src.database import connection


router = APIRouter(prefix="/auth", tags=["authentication"])
admin_router = APIRouter(prefix="/users", tags=["users"])
Role = Literal["admin", "manager", "viewer"]


class LoginRequest(BaseModel):
    email: str
    password: str


class UserCreate(BaseModel):
    email: str
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=1, max_length=120)
    role: Role = "viewer"


class UserRoleUpdate(BaseModel):
    role: Role


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str
    role: Role
    is_active: bool
    created_at: str


def _user_response(row) -> UserResponse:
    data = dict(row)
    data["is_active"] = bool(data["is_active"])
    return UserResponse(**data)


@router.post("/login")
def login(request: LoginRequest) -> dict:
    with connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE email = ? COLLATE NOCASE", (request.email.strip(),)).fetchone()
    if row is None or not row["is_active"] or not verify_password(request.password, row["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    user = _user_response(row)
    return {"access_token": create_access_token(user.id, user.role, user.email), "token_type": "bearer", "user": user}


@router.get("/me", response_model=UserResponse)
def current_user(user: dict = Depends(get_current_user)) -> UserResponse:
    data = dict(user)
    data["is_active"] = bool(data["is_active"])
    return UserResponse(**data)


@admin_router.get("", response_model=list[UserResponse])
def list_users(_: dict = Depends(require_roles("admin"))) -> list[UserResponse]:
    with connection() as conn:
        rows = conn.execute(
            "SELECT id, email, full_name, role, is_active, created_at FROM users ORDER BY full_name"
        ).fetchall()
    return [_user_response(row) for row in rows]


@admin_router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(request: UserCreate, _: dict = Depends(require_roles("admin"))) -> UserResponse:
    try:
        with connection() as conn:
            cursor = conn.execute(
                "INSERT INTO users (email, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                (request.email.strip(), hash_password(request.password), request.full_name.strip(), request.role),
            )
            row = conn.execute(
                "SELECT id, email, full_name, role, is_active, created_at FROM users WHERE id = ?",
                (cursor.lastrowid,),
            ).fetchone()
    except Exception as exc:
        if "UNIQUE constraint failed" in str(exc):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists") from exc
        raise
    return _user_response(row)


@admin_router.patch("/{user_id}/role", response_model=UserResponse)
def update_role(user_id: int, request: UserRoleUpdate, _: dict = Depends(require_roles("admin"))) -> UserResponse:
    with connection() as conn:
        conn.execute("UPDATE users SET role = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (request.role, user_id))
        row = conn.execute(
            "SELECT id, email, full_name, role, is_active, created_at FROM users WHERE id = ?", (user_id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return _user_response(row)


@admin_router.patch("/{user_id}/status", response_model=UserResponse)
def update_status(user_id: int, active: bool, _: dict = Depends(require_roles("admin"))) -> UserResponse:
    with connection() as conn:
        conn.execute("UPDATE users SET is_active = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (int(active), user_id))
        row = conn.execute(
            "SELECT id, email, full_name, role, is_active, created_at FROM users WHERE id = ?", (user_id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return _user_response(row)
