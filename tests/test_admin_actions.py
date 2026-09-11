from importlib import import_module

from src.auth.security import hash_password


def test_admin_can_manage_users_but_viewer_cannot(tmp_path, monkeypatch):
    database_module = import_module("src.database.connection")
    database_path = tmp_path / "admin.db"
    monkeypatch.setattr(database_module, "DATABASE_PATH", database_path)
    database_module.initialise_database(database_path)

    with database_module.get_connection(database_path) as conn:
        conn.execute(
            "INSERT INTO users (email, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
            ("admin@example.com", hash_password("AdminPass123"), "Admin", "admin"),
        )
        conn.execute(
            "INSERT INTO users (email, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
            ("viewer@example.com", hash_password("ViewerPass123"), "Viewer", "viewer"),
        )

    from fastapi.testclient import TestClient
    from src.api.main import app

    with TestClient(app) as client:
        admin_login = client.post(
            "/auth/login", json={"email": "admin@example.com", "password": "AdminPass123"}
        )
        viewer_login = client.post(
            "/auth/login", json={"email": "viewer@example.com", "password": "ViewerPass123"}
        )
        admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}
        viewer_headers = {"Authorization": f"Bearer {viewer_login.json()['access_token']}"}

        created = client.post(
            "/users",
            headers=admin_headers,
            json={
                "email": "manager@example.com",
                "password": "ManagerPass123",
                "full_name": "Manager",
                "role": "manager",
            },
        )
        assert created.status_code == 201
        user_id = created.json()["id"]

        assert client.get("/users", headers=viewer_headers).status_code == 403
        assert client.patch(f"/users/{user_id}/role", headers=admin_headers, json={"role": "admin"}).status_code == 200
        deactivated = client.patch(f"/users/{user_id}/status?active=false", headers=admin_headers)
        assert deactivated.status_code == 200
        assert deactivated.json()["is_active"] is False
