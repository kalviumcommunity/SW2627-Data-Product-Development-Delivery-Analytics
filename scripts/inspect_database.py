"""Print a read-only summary of the local SQLite application database."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import DATABASE_PATH
from src.database import connection


def main() -> None:
    print(f"Database: {DATABASE_PATH}")
    if not DATABASE_PATH.exists():
        print("Database does not exist yet. Start the API or run the refresh first.")
        return
    with connection() as conn:
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
        ).fetchall()
        for row in tables:
            table = row[0]
            count = conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
            print(f"- {table}: {count:,} rows")

        refresh = conn.execute(
            """SELECT status, started_at, completed_at, rows_loaded, error_message
               FROM refresh_runs ORDER BY id DESC LIMIT 1"""
        ).fetchone()
        if refresh:
            print(f"Latest refresh: {refresh['status']} ({refresh['rows_loaded']:,} rows)")
            if refresh["error_message"]:
                print(f"Refresh error: {refresh['error_message']}")


if __name__ == "__main__":
    main()
