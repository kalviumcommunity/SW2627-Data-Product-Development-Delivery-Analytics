from src.auth.security import hash_password
from src.database.connection import get_connection, initialise_database
from importlib import import_module


def test_login_role_and_assignment_permissions(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"
    connection_module = import_module("src.database.connection")

    monkeypatch.setattr(connection_module, "DATABASE_PATH", database_path)
    initialise_database(database_path)
    with get_connection(database_path) as conn:
        conn.execute(
            "INSERT INTO users (email, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
            ("admin@example.com", hash_password("AdminPass123"), "Admin", "admin"),
        )
        conn.execute(
            "INSERT INTO users (email, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
            ("viewer@example.com", hash_password("ViewerPass123"), "Viewer", "viewer"),
        )
        conn.execute(
            "INSERT INTO employees (employee_id, employee_name, capacity_hours_monthly) VALUES (?, ?, ?)",
            ("E1", "Example Employee", 160),
        )

    from fastapi.testclient import TestClient
    from src.api.main import app

    with TestClient(app) as client:
        admin_login = client.post("/auth/login", json={"email": "admin@example.com", "password": "AdminPass123"})
        assert admin_login.status_code == 200
        admin_headers = {"Authorization": "Bearer " + admin_login.json()["access_token"]}
        viewer_login = client.post("/auth/login", json={"email": "viewer@example.com", "password": "ViewerPass123"})
        viewer_headers = {"Authorization": "Bearer " + viewer_login.json()["access_token"]}

        created = client.post(
            "/assignments",
            headers=admin_headers,
            json={"title": "Test work", "employee_id": "E1", "work_date": "2026-09-08", "start_time": "09:00:00", "duration_hours": 2},
        )
        assert created.status_code == 201
        denied = client.post(
            "/assignments",
            headers=viewer_headers,
            json={"title": "Denied work", "employee_id": "E1", "work_date": "2026-09-08", "start_time": "11:00:00", "duration_hours": 2},
        )
        assert denied.status_code == 403
