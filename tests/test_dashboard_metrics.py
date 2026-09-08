from datetime import date

import pandas as pd

from src.dashboard.data_handler import calculate_capacity_metrics, filter_dataset, generate_insights


def test_custom_date_filter_is_inclusive():
    frame = pd.DataFrame({"work_date": ["2026-09-01", "2026-09-08", "2026-09-20"], "hours_logged": [1, 2, 3]})
    result = filter_dataset(frame, "Custom", start_date=date(2026, 9, 5), end_date=date(2026, 9, 10))
    assert result["hours_logged"].tolist() == [2]


def test_capacity_metrics_and_conflict_alerts():
    files = {
        "employees": pd.DataFrame({
            "employee_id": ["E1"],
            "employee_name": ["Example Employee"],
            "department": ["Engineering"],
            "team": ["Team A"],
            "capacity_hours_monthly": [10],
        }),
        "allocations": pd.DataFrame({
            "employee_id": ["E1"],
            "allocation_start_date": ["2026-09-08"],
            "allocated_hours": [12],
        }),
        "timesheets": pd.DataFrame({
            "employee_id": ["E1"],
            "work_date": ["2026-09-08"],
            "hours_logged": [8],
            "billable_hours": [4],
        }),
    }
    metrics = calculate_capacity_metrics(files, "Custom", date(2026, 9, 1), date(2026, 9, 30))
    assert metrics.iloc[0]["capacity_load_pct"] == 120
    alerts = generate_insights(metrics, [
        {"employee_id": "E1", "work_date": "2026-09-08", "start_time": "09:00:00", "duration_hours": 2, "title": "A"},
        {"employee_id": "E1", "work_date": "2026-09-08", "start_time": "10:00:00", "duration_hours": 2, "title": "B"},
    ])
    assert "Overloaded" in alerts["type"].tolist()
    assert "Assignment conflict" in alerts["type"].tolist()
