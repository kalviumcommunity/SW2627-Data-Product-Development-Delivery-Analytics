"""
Missing Values Demo Script
Demonstrates missing value detection and imputation on the raw datasets.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv
from src.cleaning.missing_values import (
    analyze_missing_values,
    impute_numeric,
    impute_categorical,
    compare_missing_before_after
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
    print("MISSING VALUES ANALYSIS")
    print("=" * 60)
    
    for filename, label in RAW_DATASETS.items():
        file_path = data_dir / filename
        print(f"\n{'-' * 60}")
        print(f"Analyzing: {label}")
        print(f"{'-' * 60}")
        
        if not file_path.exists():
            print(f"  [MISSING] FILE NOT FOUND")
            continue
        
        try:
            df = load_csv(str(file_path))
            analysis = analyze_missing_values(df)
            
            print(f"  Total missing: {analysis['total_missing']} ({analysis['missing_percentage']}%)")
            print(f"  Columns with missing: {len(analysis['columns_with_missing'])}")
            
            if analysis['column_details']:
                print(f"\n  Column Details:")
                for col, details in analysis['column_details'].items():
                    print(f"    {col}: {details['null_count']} nulls ({details['null_percentage']}%)")
            
            print(f"  [OK] ANALYZED")
            
        except Exception as e:
            print(f"  [ERROR] {str(e)}")
    
    print(f"\n{'=' * 60}")
    print("ANALYSIS COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
