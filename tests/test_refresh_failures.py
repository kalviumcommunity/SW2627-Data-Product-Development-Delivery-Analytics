from importlib import import_module

import pytest

from src.refresh import pipeline


database_module = import_module("src.database.connection")


def test_refresh_records_failure_when_source_file_is_missing(tmp_path, monkeypatch):
    database_path = tmp_path / "refresh.db"
    monkeypatch.setattr(database_module, "DATABASE_PATH", database_path)

    with pytest.raises(FileNotFoundError, match="Missing refresh source"):
        pipeline.refresh_data(tmp_path)

    with database_module.connection(database_path) as conn:
        run = conn.execute(
            "SELECT status, rows_loaded, error_message, completed_at FROM refresh_runs ORDER BY id DESC LIMIT 1"
        ).fetchone()

    assert run["status"] == "failed"
    assert run["rows_loaded"] == 0
    assert "Missing refresh source" in run["error_message"]
    assert run["completed_at"] is not None
