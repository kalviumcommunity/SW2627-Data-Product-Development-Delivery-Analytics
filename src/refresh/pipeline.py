"""Load raw analytics CSVs into the application SQLite database."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import PROJECT_ROOT
from src.database import connection, initialise_database


SOURCE_FILES = {
    "employee_master_raw.csv": "employee_source",
    "timesheets_raw.csv": "timesheets",
    "allocations_raw.csv": "allocations",
    "billing_raw.csv": "billing",
}


def _record_run(status: str, run_id: int, rows_loaded: int = 0, error_message: str | None = None) -> None:
    with connection() as conn:
        conn.execute(
            """UPDATE refresh_runs SET status = ?, completed_at = CURRENT_TIMESTAMP,
               rows_loaded = ?, error_message = ? WHERE id = ?""",
            (status, rows_loaded, error_message, run_id),
        )


def refresh_data(raw_path: str | Path | None = None) -> dict:
    """Refresh source tables and employee lookup records from raw CSV files."""
    source_dir = Path(raw_path) if raw_path else PROJECT_ROOT / "data" / "raw"
    initialise_database()
    with connection() as conn:
        run_id = conn.execute("INSERT INTO refresh_runs (status) VALUES ('running')").lastrowid

    rows_loaded = 0
    try:
        source_frames: dict[str, pd.DataFrame] = {}
        for filename, table_name in SOURCE_FILES.items():
            file_path = source_dir / filename
            if not file_path.exists():
                raise FileNotFoundError(f"Missing refresh source: {file_path}")
            frame = pd.read_csv(file_path)
            source_frames[table_name] = frame
            rows_loaded += len(frame)

        with connection() as conn:
            for table_name, frame in source_frames.items():
                frame.to_sql(table_name, conn, if_exists="replace", index=False)

            employees = source_frames["employee_source"]
            for row in employees.itertuples(index=False):
                conn.execute(
                    """INSERT INTO employees
                       (employee_id, employee_name, team, department, capacity_hours_monthly, is_active)
                       VALUES (?, ?, ?, ?, ?, ?)
                       ON CONFLICT(employee_id) DO UPDATE SET
                       employee_name = excluded.employee_name,
                       team = excluded.team,
                       department = excluded.department,
                       capacity_hours_monthly = excluded.capacity_hours_monthly,
                       is_active = excluded.is_active,
                       updated_at = CURRENT_TIMESTAMP""",
                    (
                        row.employee_id,
                        row.employee_name,
                        getattr(row, "team", None),
                        getattr(row, "department", None),
                        float(row.capacity_hours_monthly) if pd.notna(row.capacity_hours_monthly) else None,
                        1 if getattr(row, "employment_status", "Active") == "Active" else 0,
                    ),
                )
        _record_run("succeeded", run_id, rows_loaded)
        return {"run_id": run_id, "status": "succeeded", "rows_loaded": rows_loaded}
    except Exception as exc:
        _record_run("failed", run_id, rows_loaded, str(exc))
        raise
