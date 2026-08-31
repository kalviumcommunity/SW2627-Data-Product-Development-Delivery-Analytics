"""
KPI Card & Summary Metric Design Demo Script
Demonstrates KPI card design and summary metrics calculation.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from src.ingestion.load_data import load_csv
from src.metrics.kpi_design import (
    calculate_employee_utilization_kpi,
    calculate_revenue_kpi,
    calculate_allocation_kpi,
    create_kpi_card,
    format_number,
    get_summary_metrics,
    validate_kpi_data
)


# Define the raw datasets
RAW_DATASETS = {
    "timesheets_raw.csv": "Timesheets",
    "billing_raw.csv": "Billing",
    "allocations_raw.csv": "Allocations"
}


def main():
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    
    print("=" * 60)
    print("KPI CARD & SUMMARY METRIC DESIGN")
    print("=" * 60)
    
    # Load datasets
    print("\n--- Loading Data ---")
    datasets = {}
    for filename, label in RAW_DATASETS.items():
        file_path = data_dir / filename
        if file_path.exists():
            df = load_csv(str(file_path))
            datasets[label] = df
            print(f"Loaded {label}: {len(df)} rows")
    
    # Employee utilization KPI
    print("\n" + "=" * 60)
    print("EMPLOYEE UTILIZATION KPI")
    print("=" * 60)
    
    if 'Timesheets' in datasets:
        ts = datasets['Timesheets']
        util_kpi = calculate_employee_utilization_kpi(ts)
        print(f"  KPI: {util_kpi['kpi_name']}")
        print(f"  Value: {util_kpi['value']}%")
        print(f"  Target: {util_kpi['target']}%")
        print(f"  Status: {util_kpi['status']}")
        print(f"  Total Employees: {util_kpi['total_employees']}")
        print(f"  Total Hours Logged: {util_kpi['total_hours_logged']:,}")
        print(f"  Total Billable Hours: {util_kpi['total_billable_hours']:,}")
        print(f"  Trend: {util_kpi['trend']}")
        
        # Create KPI card
        card = create_kpi_card('Employee Utilization', util_kpi['value'], util_kpi['target'], util_kpi['threshold'])
        print(f"  Card Status: {card['status']}")
        print(f"  Card Progress: {card['progress']}%")
    
    # Revenue KPI
    print("\n" + "=" * 60)
    print("REVENUE KPI")
    print("=" * 60)
    
    if 'Billing' in datasets:
        billing = datasets['Billing']
        rev_kpi = calculate_revenue_kpi(billing)
        print(f"  KPI: {rev_kpi['kpi_name']}")
        print(f"  Value: {rev_kpi['formatted_value']}")
        print(f"  Target: ${rev_kpi['target']:,.2f}")
        print(f"  Status: {rev_kpi['status']}")
        print(f"  Total Transactions: {rev_kpi['total_transactions']}")
        print(f"  Avg per Transaction: ${rev_kpi['avg_per_transaction']:,.2f}")
        print(f"  Trend: {rev_kpi['trend']}")
    
    # Allocation KPI
    print("\n" + "=" * 60)
    print("ALLOCATION EFFICIENCY KPI")
    print("=" * 60)
    
    if 'Allocations' in datasets:
        alloc = datasets['Allocations']
        alloc_kpi = calculate_allocation_kpi(alloc)
        print(f"  KPI: {alloc_kpi['kpi_name']}")
        print(f"  Value: {alloc_kpi['value']}%")
        print(f"  Target: {alloc_kpi['target']}%")
        print(f"  Status: {alloc_kpi['status']}")
        print(f"  Total Allocated Hours: {alloc_kpi['total_allocated_hours']:,}")
        print(f"  Total Planned Billable: {alloc_kpi['total_planned_billable']:,}")
        print(f"  Trend: {alloc_kpi['trend']}")
    
    # Summary metrics
    print("\n" + "=" * 60)
    print("SUMMARY METRICS")
    print("=" * 60)
    
    if 'Timesheets' in datasets:
        ts = datasets['Timesheets']
        summary = get_summary_metrics(ts, 'hours_logged')
        print(f"  Metric: hours_logged")
        print(f"  Total: {format_number(summary['total'])}")
        print(f"  Average: {format_number(summary['average'])}")
        print(f"  Median: {format_number(summary['median'])}")
        print(f"  Min: {format_number(summary['minimum'])}")
        print(f"  Max: {format_number(summary['maximum'])}")
        print(f"  Std Dev: {format_number(summary['std_deviation'])}")
        print(f"  Count: {summary['count']:,}")
    
    # Data validation
    print("\n" + "=" * 60)
    print("KPI DATA VALIDATION")
    print("=" * 60)
    
    if 'Timesheets' in datasets:
        ts = datasets['Timesheets']
        validation = validate_kpi_data(ts, ['employee_id', 'hours_logged', 'billable_hours'])
        print(f"  Valid: {validation['valid']}")
        print(f"  Missing Columns: {validation['missing_columns']}")
        print(f"  Total Null Count: {validation['total_null_count']}")
        print(f"  Total Rows: {validation['total_rows']}")
        print(f"  Data Quality Score: {validation['data_quality_score']}")
    
    print(f"\n{'=' * 60}")
    print("KPI CARD & SUMMARY METRIC DESIGN COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()