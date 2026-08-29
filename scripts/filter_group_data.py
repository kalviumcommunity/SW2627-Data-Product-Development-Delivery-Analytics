"""
SQL Filtering, Grouping & Aggregation Demo Script
Demonstrates SQL queries with filtering and grouping.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv
from src.sql.db_integration import (
    create_connection,
    create_tables_from_dataframes
)
from src.sql.filtering_grouping import (
    filter_employees_by_department,
    filter_employees_by_experience,
    group_employees_by_department,
    group_timesheets_by_project,
    aggregate_billing_by_month,
    filter_high_utilization,
    group_allocations_by_role,
    get_aggregation_summary
)


# Define the raw datasets
RAW_DATASETS = {
    "employee_master_raw.csv": "employees",
    "timesheets_raw.csv": "timesheets",
    "allocations_raw.csv": "allocations",
    "billing_raw.csv": "billing"
}


def main():
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    
    print("=" * 60)
    print("SQL FILTERING, GROUPING & AGGREGATION")
    print("=" * 60)
    
    # Create database connection
    print("\n--- Database Setup ---")
    conn = create_connection()
    
    # Load all datasets
    print("\n--- Loading Data ---")
    dataframes = {}
    for filename, table_name in RAW_DATASETS.items():
        file_path = data_dir / filename
        if file_path.exists():
            df = load_csv(str(file_path))
            dataframes[table_name] = df
            print(f"Loaded {table_name}: {len(df)} rows")
    
    # Create tables
    print("\n--- Creating Tables ---")
    create_tables_from_dataframes(conn, dataframes)
    print("Tables created successfully")
    
    # Filtering
    print("\n" + "=" * 60)
    print("FILTERING RESULTS")
    print("=" * 60)
    
    # Filter by department
    print("\n--- Employees in Engineering Department ---")
    eng = filter_employees_by_department(conn, "Engineering")
    print(f"Found {len(eng)} employees")
    print(eng.head(3).to_string(index=False))
    
    # Filter by experience
    print("\n--- Employees with 5+ Years Experience ---")
    experienced = filter_employees_by_experience(conn, 5)
    print(f"Found {len(experienced)} employees")
    print(experienced.head(3).to_string(index=False))
    
    # Grouping
    print("\n" + "=" * 60)
    print("GROUPING RESULTS")
    print("=" * 60)
    
    # Group by department
    print("\n--- Employees by Department ---")
    dept = group_employees_by_department(conn)
    print(dept.to_string(index=False))
    
    # Group by project
    print("\n--- Timesheets by Project (Top 5) ---")
    project = group_timesheets_by_project(conn)
    print(project.head(5).to_string(index=False))
    
    # Aggregation
    print("\n" + "=" * 60)
    print("AGGREGATION RESULTS")
    print("=" * 60)
    
    # Monthly billing
    print("\n--- Monthly Billing ---")
    monthly = aggregate_billing_by_month(conn)
    print(monthly.head(10).to_string(index=False))
    
    # High utilization
    print("\n--- High Utilization Employees (70%+) ---")
    high_util = filter_high_utilization(conn, 70)
    print(f"Found {len(high_util)} employees")
    print(high_util.head(5).to_string(index=False))
    
    # Group by role
    print("\n--- Allocations by Role ---")
    roles = group_allocations_by_role(conn)
    print(roles.to_string(index=False))
    
    # Summary
    print("\n--- Aggregation Summary ---")
    summary = get_aggregation_summary(conn)
    for metric, value in summary.items():
        print(f"  {metric}: {value}")
    
    # Close connection
    conn.close()
    
    print(f"\n{'=' * 60}")
    print("FILTERING, GROUPING & AGGREGATION COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()