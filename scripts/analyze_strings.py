"""
String Normalization Demo Script
Demonstrates string cleaning and normalization on the raw datasets.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv
from src.cleaning.string_normalization import (
    normalize_whitespace,
    normalize_case,
    remove_special_characters,
    get_string_summary
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
    print("STRING NORMALIZATION ANALYSIS")
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
            summary = get_string_summary(df)
            
            print(f"  Total rows: {len(df)}")
            print(f"  String columns: {len(summary)}")
            
            for col, stats in summary.items():
                print(f"\n  {col}:")
                print(f"    Null count: {stats['null_count']}")
                print(f"    Unique values: {stats['unique_count']}")
                print(f"    Avg length: {stats['avg_length']:.1f}")
            
            print(f"  [OK] ANALYZED")
            
        except Exception as e:
            print(f"  [ERROR] {str(e)}")
    
    print(f"\n{'=' * 60}")
    print("ANALYSIS COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
