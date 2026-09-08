"""Small HTTP client used by Streamlit to communicate with FastAPI."""

from __future__ import annotations

import os

import requests


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


def _request(method: str, path: str, token: str, **kwargs) -> requests.Response:
    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {token}"
    return requests.request(method, f"{API_BASE_URL}{path}", headers=headers, timeout=10, **kwargs)


def login(email: str, password: str) -> tuple[dict | None, str | None]:
    try:
        response = requests.post(f"{API_BASE_URL}/auth/login", json={"email": email, "password": password}, timeout=10)
    except requests.RequestException:
        return None, "The API is unavailable. Start FastAPI before signing in."
    if response.status_code != 200:
        return None, response.json().get("detail", "Invalid email or password")
    return response.json(), None


def get_employees(token: str) -> list[dict]:
    response = _request("GET", "/employees", token)
    response.raise_for_status()
    return response.json()


def get_assignments(token: str, start_date: str | None = None, end_date: str | None = None) -> list[dict]:
    params = {key: value for key, value in {"start_date": start_date, "end_date": end_date}.items() if value}
    response = _request("GET", "/assignments", token, params=params)
    response.raise_for_status()
    return response.json()


def create_assignment(token: str, payload: dict) -> dict:
    response = _request("POST", "/assignments", token, json=payload)
    response.raise_for_status()
    return response.json()


def update_assignment(token: str, assignment_id: int, payload: dict) -> dict:
    response = _request("PUT", f"/assignments/{assignment_id}", token, json=payload)
    response.raise_for_status()
    return response.json()


def delete_assignment(token: str, assignment_id: int) -> None:
    response = _request("DELETE", f"/assignments/{assignment_id}", token)
    response.raise_for_status()


def list_users(token: str) -> list[dict]:
    response = _request("GET", "/users", token)
    response.raise_for_status()
    return response.json()


def create_user(token: str, payload: dict) -> dict:
    response = _request("POST", "/users", token, json=payload)
    response.raise_for_status()
    return response.json()


def update_user_role(token: str, user_id: int, role: str) -> dict:
    response = _request("PATCH", f"/users/{user_id}/role", token, json={"role": role})
    response.raise_for_status()
    return response.json()


def update_user_status(token: str, user_id: int, active: bool) -> dict:
    response = _request("PATCH", f"/users/{user_id}/status", token, params={"active": str(active).lower()})
    response.raise_for_status()
    return response.json()
