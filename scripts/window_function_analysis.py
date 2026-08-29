"""
SQL Window Functions & Ranking Systems Demo Script
Demonstrates SQL window functions for ranking and analysis.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv
from src.sql.db_integration import (
    create_connection,
    create_tables_from_dataframes
)
from src.sql.window_functions import (
    rank_employees_by_utilization,
    rank_employees_by_revenue,
    department_ranking,
    running_total_hours,
    moving_average_hours,
    dense_rank_employees,
    lag_lead_hours,
    percent_rank_utilization,
    ntile_groups,
    get_window_function_summary
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
    print("SQL WINDOW FUNCTIONS & RANKING SYSTEMS")
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
    
    # Window functions
    print("\n" + "=" * 60)
    print("WINDOW FUNCTION RESULTS")
    print("=" * 60)
    
    # Rank by utilization
    print("\n--- Employee Ranking by Utilization (Top 10) ---")
    rank_util = rank_employees_by_utilization(conn)
    print(rank_util.head(10).to_string(index=False))
    
    # Rank by revenue
    print("\n--- Employee Ranking by Revenue (Top 10) ---")
    rank_rev = rank_employees_by_revenue(conn)
    print(rank_rev.head(10).to_string(index=False))
    
    # Department ranking
    print("\n--- Department Ranking ---")
    dept_rank = department_ranking(conn)
    print(dept_rank.to_string(index=False))
    
    # Running total
    print("\n--- Running Total Hours (Sample) ---")
    running = running_total_hours(conn)
    print(running.head(10).to_string(index=False))
    
    # Moving average
    print("\n--- Moving Average Hours (Sample) ---")
    moving = moving_average_hours(conn, 7)
    print(moving.head(10).to_string(index=False))
    
    # Dense rank
    print("\n--- Dense Rank by Experience (Top 10) ---")
    dense = dense_rank_employees(conn)
    print(dense.head(10).to_string(index=False))
    
    # Lag/Lead
    print("\n--- Lag/Lead Hours (Sample) ---")
    lag_lead = lag_lead_hours(conn)
    print(lag_lead.head(10).to_string(index=False))
    
    # Percent rank
    print("\n--- Percent Rank Utilization (Top 10) ---")
    pct = percent_rank_utilization(conn)
    print(pct.head(10).to_string(index=False))
    
    # Ntile groups
    print("\n--- Utilization Quartiles ---")
    ntile = ntile_groups(conn, 4)
    print(ntile['utilization_group'].value_counts().sort_index().to_string())
    
    # Summary
    print("\n--- Window Function Summary ---")
    summary = get_window_function_summary(conn)
    for metric, value in summary.items():
        print(f"  {metric}: {value}")
    
    # Close connection
    conn.close()
    
    print(f"\n{'=' * 60}")
    print("SQL WINDOW FUNCTIONS & RANKING SYSTEMS COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()