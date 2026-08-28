"""
Date Transformation Demo Script
Demonstrates date parsing and transformation on the raw datasets.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv
from src.cleaning.date_transforms import (
    parse_dates,
    extract_date_features,
    get_date_summary
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
    print("DATE TRANSFORMATION ANALYSIS")
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
            
            # Parse dates
            df_parsed = parse_dates(df)
            
            # Get date summary
            summary = get_date_summary(df_parsed)
            
            print(f"  Total rows: {len(df)}")
            print(f"  Date columns: {len(summary)}")
            
            for col, stats in summary.items():
                print(f"\n  {col}:")
                print(f"    Null count: {stats['null_count']}")
                print(f"    Min date: {stats['min_date']}")
                print(f"    Max date: {stats['max_date']}")
                print(f"    Date range: {stats['date_range_days']} days")
            
            print(f"  [OK] ANALYZED")
            
        except Exception as e:
            print(f"  [ERROR] {str(e)}")
    
    print(f"\n{'=' * 60}")
    print("ANALYSIS COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
