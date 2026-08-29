"""
SQL-Based Insight Validation Demo Script
Demonstrates SQL queries for validating business insights.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv
from src.sql.db_integration import (
    create_connection,
    create_tables_from_dataframes
)
from src.sql.insight_validation import (
    validate_utilization_insight,
    validate_revenue_insight,
    validate_department_performance,
    validate_billing_accuracy,
    validate_allocation_efficiency,
    run_all_validations,
    get_validation_summary
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
    print("SQL-BASED INSIGHT VALIDATION")
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
    
    # Validation results
    print("\n" + "=" * 60)
    print("VALIDATION RESULTS")
    print("=" * 60)
    
    # Utilization validation
    print("\n--- Utilization Validation ---")
    util = validate_utilization_insight(conn, 65)
    print(f"  Insight: {util['insight']}")
    print(f"  Total employees: {util['total_employees']}")
    print(f"  Average utilization: {util['avg_utilization']}%")
    print(f"  Above threshold: {util['above_threshold']}")
    print(f"  Below threshold: {util['below_threshold']}")
    print(f"  Validation passed: {util['validation_passed']}")
    
    # Revenue validation
    print("\n--- Revenue Validation ---")
    rev = validate_revenue_insight(conn, 100000)
    print(f"  Insight: {rev['insight']}")
    print(f"  Employees above threshold: {rev['employees_above_threshold']}")
    print(f"  Total revenue: ${rev['total_revenue']:,.2f}")
    print(f"  Validation passed: {rev['validation_passed']}")
    
    # Department performance validation
    print("\n--- Department Performance Validation ---")
    dept = validate_department_performance(conn)
    print(f"  Insight: {dept['insight']}")
    print(f"  Departments analyzed: {dept['departments_analyzed']}")
    print(f"  Average utilization: {dept['avg_utilization']}%")
    print(f"  Min utilization: {dept['min_utilization']}%")
    print(f"  Max utilization: {dept['max_utilization']}%")
    print(f"  Validation passed: {dept['validation_passed']}")
    
    # Billing accuracy validation
    print("\n--- Billing Accuracy Validation ---")
    bill = validate_billing_accuracy(conn)
    print(f"  Insight: {bill['insight']}")
    print(f"  Total records: {bill['total_records']}")
    print(f"  Accuracy rate: {bill['accuracy_rate']}%")
    print(f"  Validation passed: {bill['validation_passed']}")
    
    # Allocation efficiency validation
    print("\n--- Allocation Efficiency Validation ---")
    alloc = validate_allocation_efficiency(conn)
    print(f"  Insight: {alloc['insight']}")
    print(f"  Employees analyzed: {alloc['employees_analyzed']}")
    print(f"  Average efficiency: {alloc['avg_efficiency']}%")
    print(f"  Validation passed: {alloc['validation_passed']}")
    
    # Run all validations
    print("\n" + "=" * 60)
    print("OVERALL VALIDATION SUMMARY")
    print("=" * 60)
    
    all_results = run_all_validations(conn)
    summary = get_validation_summary(all_results)
    
    print(f"  Total validations: {summary['total_validations']}")
    print(f"  Passed: {summary['passed']}")
    print(f"  Failed: {summary['failed']}")
    print(f"  Pass rate: {summary['pass_rate']}%")
    
    # Close connection
    conn.close()
    
    print(f"\n{'=' * 60}")
    print("INSIGHT VALIDATION COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()