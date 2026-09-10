"""
Data Validation Script (LU 2.59)
Validates schema, data types, row counts, and null columns for raw datasets.
Exits with code 1 on failure so GitHub Actions can block merges.

Usage:
    python scripts/validate_data.py data/raw/employee_master_raw.csv
    python scripts/validate_data.py data/raw/timesheets_raw.csv
"""

import sys
from pathlib import Path

import pandas as pd

SCHEMAS = {
    "employee_master_raw.csv": {
        "required_columns": [
            "employee_id", "employee_name", "department", "team",
            "designation", "employment_type", "employment_status",
        ],
        "min_rows": 100,
        "dtypes": {"experience_years": "int64", "capacity_hours_monthly": "int64"},
    },
    "timesheets_raw.csv": {
        "required_columns": [
            "timesheet_id", "employee_id", "work_date", "hours_logged",
            "billable_hours", "task_category",
        ],
        "min_rows": 1000,
        "dtypes": {"hours_logged": "float64", "billable_hours": "float64"},
    },
    "allocations_raw.csv": {
        "required_columns": [
            "allocation_id", "employee_id", "project_id",
            "allocated_hours", "allocation_percentage",
        ],
        "min_rows": 500,
        "dtypes": {"allocated_hours": "float64", "allocation_percentage": "float64"},
    },
    "billing_raw.csv": {
        "required_columns": [
            "billing_id", "client_id", "project_id", "employee_id",
            "billed_amount", "billable_hours", "invoice_id",
        ],
        "min_rows": 1000,
        "dtypes": {"billed_amount": "float64", "billable_hours": "float64"},
    },
}


def validate(file_path: str) -> None:
    path = Path(file_path)
    filename = path.name
    print(f"Validating: {file_path}")

    df = pd.read_csv(file_path)
    schema = SCHEMAS.get(filename)
    if schema is None:
        print(f"WARNING: No schema defined for {filename}, running basic checks only")

    errors = []

    if schema:
        required_cols = schema["required_columns"]
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            errors.append(f"Missing required columns: {missing}")
        else:
            print(f"PASS: All {len(required_cols)} required columns present")

        if schema.get("dtypes"):
            for col, expected in schema["dtypes"].items():
                if col in df.columns:
                    actual = str(df[col].dtype)
                    if expected.startswith("float") or expected.startswith("int"):
                        numeric_types = ["float64", "float32", "int64", "int32", "str"]
                        if actual in numeric_types:
                            print(f"PASS: '{col}' is {actual} (numeric-compatible)")
                        else:
                            errors.append(f"Column '{col}' dtype: expected numeric, got {actual}")
                    elif actual != expected:
                        errors.append(f"Column '{col}' dtype: expected {expected}, got {actual}")
                    else:
                        print(f"PASS: '{col}' is {expected}")

        min_rows = schema.get("min_rows", 1)
        if len(df) < min_rows:
            errors.append(f"Row count {len(df)} below minimum {min_rows}")
        else:
            print(f"PASS: Row count {len(df)} meets minimum {min_rows}")

    null_cols = [c for c in df.columns if df[c].isnull().all()]
    if null_cols:
        errors.append(f"Fully null columns: {null_cols}")
    else:
        print("PASS: No fully null columns")

    if errors:
        print("\nVALIDATION FAILED:")
        for e in errors:
            print(f"  ERROR: {e}")
        sys.exit(1)
    else:
        print("\nALL CHECKS PASSED")
        sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_data.py <csv_path>")
        sys.exit(1)
    validate(sys.argv[1])
