"""
Executive Reporting & Stakeholder Communication Demo Script
Demonstrates executive reporting and stakeholder communication.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from src.reporting.executive_report import (
    generate_executive_summary,
    generate_stakeholder_report,
    format_report_for_presentation,
    validate_report_data,
    get_reporting_recommendations
)
from src.ingestion.load_data import load_csv


def main():
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    
    print("=" * 60)
    print("EXECUTIVE REPORTING & STAKEHOLDER COMMUNICATION")
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
    
    # Executive summary
    print("\n" + "=" * 60)
    print("EXECUTIVE SUMMARY")
    print("=" * 60)
    
    if 'Timesheets' in datasets:
        ts = datasets['Timesheets']
        summary = generate_executive_summary(ts, 'hours_logged')
        print(summary['executive_summary'])
    
    # Stakeholder report
    print("\n" + "=" * 60)
    print("STAKEHOLDER REPORT")
    print("=" * 60)
    
    if 'Timesheets' in datasets:
        ts = datasets['Timesheets']
        report = generate_stakeholder_report(ts, 'hours_logged', 'task_category')
        formatted = format_report_for_presentation(report)
        print(formatted[:800] + "...")
    
    # Reporting recommendations
    print("\n" + "=" * 60)
    print("REPORTING RECOMMENDATIONS")
    print("=" * 60)
    
    if 'Timesheets' in datasets:
        ts = datasets['Timesheets']
        recs = get_reporting_recommendations(ts, 'hours_logged', 'task_category')
        print(f"Recommended frequency: {recs['recommended_frequency']}")
        print(f"Recommended format: {recs['recommended_format']}")
        print(f"Stakeholder level: {recs['stakeholder_level']}")
        print(f"Alert threshold: {recs['alert_threshold']}%")
        print(f"Success criteria: {recs['success_criteria']}")
        print(f"Improvement focus: {recs['improvement_focus']}")
    
    # Data validation
    print("\n" + "=" * 60)
    print("DATA VALIDATION")
    print("=" * 60)
    
    if 'Timesheets' in datasets:
        ts = datasets['Timesheets']
        validation = validate_report_data(ts, ['employee_id', 'hours_logged', 'task_category'])
        print(f"Valid: {validation['valid']}")
        print(f"Meets minimum: {validation['meets_minimum']}")
        print(f"Data quality score: {validation['data_quality_score']}")
    
    print(f"\n{'=' * 60}")
    print("EXECUTIVE REPORTING COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()