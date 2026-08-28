"""
Multi-Source Merging Demo Script
Demonstrates dataset merging and validation on the raw datasets.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv
from src.merging.merge_datasets import (
    validate_keys_before_merge,
    merge_with_validation,
    create_analytics_dataset,
    get_merge_summary
)


# Define the raw datasets
RAW_DATASETS = {
    "employee_master_raw.csv": "Employee Master",
    "timesheets_raw.csv": "Timesheets",
    "allocations_raw.csv": "Allocations",
    "billing_raw.csv": "Billing"
}


def main():
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    
    print("=" * 60)
    print("MULTI-SOURCE MERGING DEMO")
    print("=" * 60)
    
    # Load all datasets
    datasets = {}
    for filename, label in RAW_DATASETS.items():
        file_path = data_dir / filename
        if file_path.exists():
            datasets[label] = load_csv(str(file_path))
            print(f"Loaded {label}: {len(datasets[label])} rows")
    
    if len(datasets) < 2:
        print("\n[ERROR] Need at least 2 datasets to demonstrate merging")
        return
    
    # Validate keys before merge
    print("\n" + "=" * 60)
    print("KEY VALIDATION")
    print("=" * 60)
    
    if 'Employee Master' in datasets and 'Timesheets' in datasets:
        validation = validate_keys_before_merge(
            datasets['Timesheets'],
            datasets['Employee Master'],
            'employee_id'
        )
        print(f"\nEmployee ID overlap: {validation.get('overlap_pct', 0)}%")
    
    # Create analytics dataset
    if all(k in datasets for k in ['Timesheets', 'Allocations', 'Billing', 'Employee Master']):
        analytics_df = create_analytics_dataset(
            datasets['Timesheets'],
            datasets['Allocations'],
            datasets['Billing'],
            datasets['Employee Master']
        )
        
        summary = get_merge_summary(analytics_df)
        print(f"\nAnalytics dataset summary:")
        print(f"  Rows: {summary['total_rows']}")
        print(f"  Columns: {summary['total_columns']}")
    
    print(f"\n{'=' * 60}")
    print("MERGING DEMO COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
