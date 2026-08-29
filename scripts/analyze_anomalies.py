"""
Anomaly Detection Demo Script
Demonstrates anomaly detection and risk identification on the raw datasets.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv
from src.features.derive_features import create_derived_columns
from src.analytics.anomaly_detection import (
    detect_anomalies,
    detect_utilization_anomalies,
    calculate_risk_scores,
    identify_high_risk_records,
    get_risk_summary,
    classify_risk_level
)


# Define the raw datasets
RAW_DATASETS = {
    "timesheets_raw.csv": "Timesheets",
    "allocations_raw.csv": "Allocations",
    "billing_raw.csv": "Billing"
}


def main():
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    
    print("=" * 60)
    print("ANOMALY DETECTION & RISK IDENTIFICATION")
    print("=" * 60)
    
    # Load all datasets
    datasets = {}
    for filename, label in RAW_DATASETS.items():
        file_path = data_dir / filename
        if file_path.exists():
            datasets[label] = load_csv(str(file_path))
            print(f"Loaded {label}: {len(datasets[label])} rows")
    
    if 'Timesheets' not in datasets:
        print("[ERROR] Timesheets dataset not found")
        return
    
    # Create derived columns for KPIs
    print("\n" + "=" * 60)
    print("CREATING DERIVED COLUMNS")
    print("=" * 60)
    
    from src.features.derive_features import create_derived_columns
    timesheets = create_derived_columns(datasets['Timesheets'])
    
    print("\n" + "=" * 60)
    print("ANOMALY DETECTION RESULTS")
    print("=" * 60)
    
    # Detect anomalies in numeric columns
    print("\n--- General Anomaly Detection ---")
    anomalies = detect_anomalies(timesheets, method='iqr')
    print(f"Total rows analyzed: {anomalies['total_rows']}")
    print(f"Columns analyzed: {len(anomalies['columns_analyzed'])}")
    
    for col, stats in anomalies['anomalies'].items():
        if stats['count'] > 0:
            print(f"  {col}: {stats['count']} anomalies ({stats['percentage']}%)")
    
    # Detect utilization anomalies
    print("\n--- Utilization Anomalies ---")
    util_anomalies = detect_utilization_anomalies(timesheets)
    for metric, stats in util_anomalies.items():
        print(f"  {metric}: {stats['outlier_count']} outliers ({stats['percentage']}%)")
    
    # Calculate risk scores
    print("\n--- Risk Score Calculation ---")
    timesheets = timesheets.copy()
    timesheets['risk_score'] = calculate_risk_scores(timesheets)
    
    print(f"Average risk score: {timesheets['risk_score'].mean():.2f}")
    print(f"Max risk score: {timesheets['risk_score'].max():.2f}")
    
    # Get risk summary
    print("\n--- Risk Summary ---")
    risk_summary = get_risk_summary(timesheets)
    print(f"Total records: {risk_summary['total_records']}")
    print(f"High risk count: {risk_summary['high_risk_count']}")
    print(f"Critical risk count: {risk_summary['critical_risk_count']}")
    
    print("\nRisk Distribution:")
    for level, count in risk_summary['risk_distribution'].items():
        if count > 0:
            print(f"  {level}: {count}")
    
    # Identify high-risk records
    print("\n--- High Risk Records ---")
    high_risk = identify_high_risk_records(timesheets)
    print(f"High risk records: {len(high_risk)}")
    
    if len(high_risk) > 0:
        print("\nSample high risk records:")
        for idx, row in high_risk.head(5).iterrows():
            emp_id = row.get('employee_id', 'Unknown')
            risk = row['risk_score']
            level = classify_risk_level(risk)
            print(f"  Employee: {emp_id}, Risk Score: {risk:.0f}, Level: {level}")
    
    print(f"\n{'=' * 60}")
    print("ANOMALY DETECTION COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()