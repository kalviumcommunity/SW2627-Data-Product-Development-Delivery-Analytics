"""
Deduplication Demo Script
Demonstrates duplicate detection and removal on the raw datasets.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv
from src.cleaning.deduplication import (
    analyze_duplicates,
    find_exact_duplicates,
    remove_duplicates,
    log_duplicates_removed
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
    print("DUPLICATE DETECTION ANALYSIS")
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
            analysis = analyze_duplicates(df)
            
            print(f"  Total rows: {len(df)}")
            print(f"  Has duplicates: {analysis['has_duplicates']}")
            print(f"  Duplicate count: {analysis['duplicate_count']}")
            print(f"  Duplicate percentage: {analysis['duplicate_percentage']}%")
            
            if analysis['has_duplicates']:
                print(f"\n  Sample duplicates:")
                dup_df = find_exact_duplicates(df)
                print(dup_df.head())
            
            print(f"  [OK] ANALYZED")
            
        except Exception as e:
            print(f"  [ERROR] {str(e)}")
    
    print(f"\n{'=' * 60}")
    print("ANALYSIS COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
