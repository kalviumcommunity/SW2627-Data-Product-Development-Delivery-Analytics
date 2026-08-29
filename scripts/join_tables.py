"""
SQL Joins & Multi-Table Analysis Demo Script
Demonstrates SQL joins across multiple tables.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv
from src.sql.db_integration import (
    create_connection,
    create_tables_from_dataframes
)
from src.sql.joins import (
    join_timesheets_with_employees,
    join_allocations_with_employees,
    join_billing_with_employees,
    join_all_tables,
    aggregate_by_department,
    aggregate_by_project,
    get_join_summary
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
    print("SQL JOINS & MULTI-TABLE ANALYSIS")
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
    
    # Join operations
    print("\n" + "=" * 60)
    print("JOIN RESULTS")
    print("=" * 60)
    
    # Join timesheets with employees
    print("\n--- Timesheets with Employees ---")
    ts_emp = join_timesheets_with_employees(conn)
    print(f"Rows: {len(ts_emp)}, Columns: {len(ts_emp.columns)}")
    print(ts_emp.head(3).to_string(index=False))
    
    # Join allocations with employees
    print("\n--- Allocations with Employees ---")
    alloc_emp = join_allocations_with_employees(conn)
    print(f"Rows: {len(alloc_emp)}, Columns: {len(alloc_emp.columns)}")
    print(alloc_emp.head(3).to_string(index=False))
    
    # Join billing with employees
    print("\n--- Billing with Employees ---")
    bill_emp = join_billing_with_employees(conn)
    print(f"Rows: {len(bill_emp)}, Columns: {len(bill_emp.columns)}")
    print(bill_emp.head(3).to_string(index=False))
    
    # Join all tables
    print("\n--- All Tables Joined ---")
    all_data = join_all_tables(conn)
    print(f"Rows: {len(all_data)}, Columns: {len(all_data.columns)}")
    print(all_data.head(3).to_string(index=False))
    
    # Aggregation with joins
    print("\n" + "=" * 60)
    print("AGGREGATION WITH JOINS")
    print("=" * 60)
    
    # Aggregate by department
    print("\n--- Department Aggregation ---")
    dept_agg = aggregate_by_department(conn)
    print(dept_agg.to_string(index=False))
    
    # Aggregate by project
    print("\n--- Project Aggregation (Top 5) ---")
    proj_agg = aggregate_by_project(conn)
    print(proj_agg.head(5).to_string(index=False))
    
    # Summary
    print("\n--- Join Summary ---")
    summary = get_join_summary(conn)
    for metric, value in summary.items():
        print(f"  {metric}: {value}")
    
    # Close connection
    conn.close()
    
    print(f"\n{'=' * 60}")
    print("SQL JOINS & MULTI-TABLE ANALYSIS COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()