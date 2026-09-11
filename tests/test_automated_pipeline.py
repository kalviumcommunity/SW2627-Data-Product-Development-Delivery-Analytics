import pandas as pd

from scripts.automated_pipeline import aggregate


def test_utilization_by_category_groups_by_task_category():
    frames = {
        "timesheets": pd.DataFrame(
            {
                "task_category": ["Development", "Development", "Support"],
                "hours_logged": [8, 4, 5],
                "billable_hours": [6, 2, 5],
                "timesheet_id": ["TS1", "TS2", "TS3"],
            }
        ),
        "billing": pd.DataFrame(
            {"client_id": [], "billed_amount": [], "billable_hours": [], "invoice_id": []}
        ),
        "employee_master": pd.DataFrame({"department": [], "team": [], "employee_id": []}),
        "allocations": pd.DataFrame({"project_id": [], "allocated_hours": [], "employee_id": []}),
    }

    result = aggregate(frames)["utilization_by_category"].set_index("task_category")

    assert list(result.index) == ["Development", "Support"]
    assert result.loc["Development", "total_hours"] == 12
    assert result.loc["Development", "total_billable"] == 8
    assert result.loc["Development", "utilization_rate"] == 66.67
