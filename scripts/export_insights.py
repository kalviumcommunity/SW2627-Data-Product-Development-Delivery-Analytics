"""
Insight Export & Report Generation Demo Script
Demonstrates exporting insights and generating reports.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from src.export.insight_export import (
    export_to_csv,
    export_to_json,
    generate_insight_report,
    generate_comparative_report,
    validate_export_data,
    get_export_format_recommendations
)
from src.ingestion.load_data import load_csv


def main():
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    
    print("=" * 60)
    print("INSIGHT EXPORT & REPORT GENERATION")
    print("=" * 60)
    
    # Load datasets
    print("\n--- Loading Data ---")
    datasets = {}
    for filename, label in [("timesheets_raw.csv", "Timesheets"), ("billing_raw.csv", "Billing")]:
        file_path = data_dir / filename
        if file_path.exists():
            df = load_csv(str(file_path))
            datasets[label] = df
            print(f"Loaded {label}: {len(df)} rows")
    
    # Export to CSV
    print("\n" + "=" * 60)
    print("EXPORT TO CSV")
    print("=" * 60)
    
    if 'Timesheets' in datasets:
        ts = datasets['Timesheets']
        result = export_to_csv(ts[['employee_id', 'hours_logged', 'billable_hours']], 'exports/timesheet_export.csv')
        print(f"Success: {result['success']}")
        print(f"Rows exported: {result['rows_exported']}")
        print(f"Columns exported: {result['columns_exported']}")
    
    # Export to JSON
    print("\n" + "=" * 60)
    print("EXPORT TO JSON")
    print("=" * 60)
    
    if 'Timesheets' in datasets:
        ts = datasets['Timesheets']
        result = export_to_json(ts[['employee_id', 'hours_logged']].head(10), 'exports/timesheet_sample.json')
        print(f"Success: {result['success']}")
        print(f"Rows exported: {result['rows_exported']}")
    
    # Generate insight report
    print("\n" + "=" * 60)
    print("INSIGHT REPORT")
    print("=" * 60)
    
    if 'Timesheets' in datasets:
        ts = datasets['Timesheets']
        report = generate_insight_report(ts, 'hours_logged', 'task_category')
        print(f"Metric: {report['metric']}")
        print(f"Total: {report['total']:,.2f}")
        print(f"Average: {report['average']:,.2f}")
        print(f"Count: {report['count']:,}")
        print(f"Trend: {report['trend']}")
        print(f"Group analysis: {len(report['group_analysis'])} groups")
    
    # Comparative report
    print("\n" + "=" * 60)
    print("COMPARATIVE REPORT")
    print("=" * 60)
    
    if 'Timesheets' in datasets and 'Billing' in datasets:
        ts = datasets['Timesheets']
        billing = datasets['Billing']
        report = generate_comparative_report(ts, billing, 'hours_logged')
        print(f"DF1 total: {report['df1_total']:,.2f}")
        print(f"DF2 total: {report['df2_total']:,.2f}")
        print(f"Difference: {report['difference']:,.2f}")
        print(f"Percentage change: {report['percentage_change']:.2f}%")
        print(f"Trend: {report['trend']}")
    
    # Validate data
    print("\n" + "=" * 60)
    print("DATA VALIDATION")
    print("=" * 60)
    
    if 'Timesheets' in datasets:
        ts = datasets['Timesheets']
        validation = validate_export_data(ts, ['employee_id', 'hours_logged', 'billable_hours'])
        print(f"Valid: {validation['valid']}")
        print(f"Missing columns: {validation['missing_columns']}")
        print(f"Null count: {validation['null_count']}")
    
    # Format recommendations
    print("\n" + "=" * 60)
    print("EXPORT FORMAT RECOMMENDATIONS")
    print("=" * 60)
    
    if 'Timesheets' in datasets:
        ts = datasets['Timesheets']
        recs = get_export_format_recommendations(ts, 'hours_logged')
        print(f"Recommended format: {recs['recommended_format']}")
        print(f"Compression: {recs['compression']}")
        print(f"Include timestamps: {recs['include_timestamps']}")
        print(f"Include metadata: {recs['include_metadata']}")
        print(f"Batch size: {recs['batch_size']}")
    
    print(f"\n{'=' * 60}")
    print("INSIGHT EXPORT COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
