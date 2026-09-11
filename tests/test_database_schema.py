from src.database.connection import get_connection, initialise_database


def test_database_initialization_creates_tables_indexes_and_constraints(tmp_path):
    database_path = tmp_path / "schema.db"

    initialise_database(database_path)
    initialise_database(database_path)

    with get_connection(database_path) as conn:
        tables = {
            row[0]
            for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        }
        indexes = {
            row[0]
            for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'index'")
        }
        columns = {
            row[1]
            for row in conn.execute("PRAGMA table_info(users)")
        }

        assert {"users", "employees", "assignments", "refresh_runs"} <= tables
        assert {"idx_assignments_work_date", "idx_assignments_employee_date"} <= indexes
        assert {"email", "password_hash", "role", "is_active"} <= columns

        conn.execute(
            "INSERT INTO users (email, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
            ("viewer@example.com", "hash", "Viewer", "viewer"),
        )
        try:
            conn.execute(
                "INSERT INTO users (email, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                ("viewer@example.com", "hash", "Duplicate", "viewer"),
            )
        except Exception as exc:
            assert "UNIQUE" in str(exc).upper()
        else:
            raise AssertionError("Duplicate user email was accepted")
