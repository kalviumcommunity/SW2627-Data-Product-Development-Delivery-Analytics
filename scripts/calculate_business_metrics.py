"""
Business Metrics Query Design Demo Script
Demonstrates SQL queries for calculating business metrics.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv
from src.sql.db_integration import (
    create_connection,
    create_tables_from_dataframes,
    execute_query
)
from src.sql.business_metrics import (
    calculate_employee_utilization,
    calculate_department_metrics,
    calculate_project_billing,
    calculate_allocation_efficiency,
    calculate_revenue_by_department,
    get_business_metrics_summary
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
    print("SQL BUSINESS METRICS QUERY DESIGN")
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
    
    # Calculate metrics
    print("\n" + "=" * 60)
    print("BUSINESS METRICS RESULTS")
    print("=" * 60)
    
    # Employee utilization
    print("\n--- Employee Utilization (Top 5) ---")
    utilization = calculate_employee_utilization(conn)
    print(utilization.head(5).to_string(index=False))
    
    # Department metrics
    print("\n--- Department Metrics ---")
    department = calculate_department_metrics(conn)
    print(department.to_string(index=False))
    
    # Project billing
    print("\n--- Project Billing (Top 5) ---")
    billing = calculate_project_billing(conn)
    print(billing.head(5).to_string(index=False))
    
    # Allocation efficiency
    print("\n--- Allocation Efficiency (Top 5) ---")
    efficiency = calculate_allocation_efficiency(conn)
    print(efficiency.head(5).to_string(index=False))
    
    # Revenue by department
    print("\n--- Revenue by Department ---")
    revenue = calculate_revenue_by_department(conn)
    print(revenue.to_string(index=False))
    
    # Summary
    print("\n--- Business Metrics Summary ---")
    summary = get_business_metrics_summary(conn)
    for category, metrics in summary.items():
        print(f"\n{category}:")
        for metric, value in metrics.items():
            print(f"  {metric}: {value}")
    
    # Close connection
    conn.close()
    
    print(f"\n{'=' * 60}")
    print("BUSINESS METRICS ANALYSIS COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()