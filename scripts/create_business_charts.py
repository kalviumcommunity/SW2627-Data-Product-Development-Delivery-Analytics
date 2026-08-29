"""
Business Visualisation Principles Demo Script
Demonstrates business visualization best practices.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from src.ingestion.load_data import load_csv
from src.viz.business_viz import (
    get_color_palette,
    get_chart_type_recommendation,
    format_number,
    create_kpi_card_data,
    get_chart_title,
    validate_data_for_visualization,
    get_business_insights_from_data
)


# Define the raw datasets
RAW_DATASETS = {
    "employee_master_raw.csv": "Employees",
    "timesheets_raw.csv": "Timesheets",
    "allocations_raw.csv": "Allocations",
    "billing_raw.csv": "Billing"
}


def main():
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    
    print("=" * 60)
    print("BUSINESS VISUALISATION PRINCIPLES")
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
    
    # Color palette
    print("\n" + "=" * 60)
    print("BUSINESS COLOR PALETTE")
    print("=" * 60)
    
    colors = get_color_palette()
    print("Primary colors:")
    for name, hex_code in list(colors.items())[:9]:
        print(f"  {name}: {hex_code}")
    
    # Chart type recommendations
    print("\n" + "=" * 60)
    print("CHART TYPE RECOMMENDATIONS")
    print("=" * 60)
    
    data_types = ['categorical', 'numeric', 'time_series']
    analysis_types = ['comparison', 'distribution', 'trend', 'composition']
    
    for dt in data_types:
        for at in analysis_types:
            chart = get_chart_type_recommendation(dt, at)
            print(f"  {dt} + {at}: {chart}")
    
    # Number formatting
    print("\n" + "=" * 60)
    print("NUMBER FORMATTING")
    print("=" * 60)
    
    test_values = [1234567.89, 12345.67, 123.45, 0.6823]
    for val in test_values:
        print(f"  {val}:")
        print(f"    Currency: {format_number(val, 'currency')}")
        print(f"    Percentage: {format_number(val * 100 if val < 1 else val, 'percentage')}")
        print(f"    General: {format_number(val, 'general')}")
    
    # KPI card data
    print("\n" + "=" * 60)
    print("KPI CARD DATA")
    print("=" * 60)
    
    kpis = [
        (68.2, 'Average Utilization', 'percentage'),
        (514886231.36, 'Total Revenue', 'currency'),
        (850, 'Total Employees', 'general'),
        (181, 'Active Projects', 'general')
    ]
    
    for value, label, fmt in kpis:
        kpi = create_kpi_card_data(value, label, fmt)
        print(f"  {kpi['label']}: {kpi['formatted_value']}")
    
    # Chart titles
    print("\n" + "=" * 60)
    print("CHART TITLE GENERATION")
    print("=" * 60)
    
    contexts = ['Employee Utilization', 'Revenue', 'Project Performance']
    analyses = ['by Department', 'by Month', 'Distribution']
    
    for ctx in contexts:
        for ana in analyses:
            title = get_chart_title(ctx, ana)
            print(f"  {title}")
    
    # Data validation for visualization
    print("\n" + "=" * 60)
    print("DATA VALIDATION FOR VISUALIZATION")
    print("=" * 60)
    
    if 'Timesheets' in datasets:
        ts = datasets['Timesheets']
        required = ['employee_id', 'hours_logged', 'billable_hours']
        validation = validate_data_for_visualization(ts, required)
        print(f"  Timesheets data valid: {validation['valid']}")
        print(f"  Missing columns: {validation['missing_columns']}")
        print(f"  Row count: {validation['row_count']}")
    
    # Business insights
    print("\n" + "=" * 60)
    print("BUSINESS INSIGHTS FROM DATA")
    print("=" * 60)
    
    if 'Timesheets' in datasets:
        ts = datasets['Timesheets']
        insights = get_business_insights_from_data(ts, 'hours_logged')
        print(f"  Metric: {insights['metric']}")
        print(f"  Total: {format_number(insights['total'])}")
        print(f"  Average: {format_number(insights['average'])}")
        print(f"  Min: {format_number(insights['min'])}")
        print(f"  Max: {format_number(insights['max'])}")
    
    print(f"\n{'=' * 60}")
    print("BUSINESS VISUALISATION PRINCIPLES COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()