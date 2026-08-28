"""
Feature Engineering Demo Script
Demonstrates feature engineering and derived columns on the raw datasets.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv
from src.features.derive_features import create_derived_columns, get_feature_summary


# Define the raw datasets
RAW_DATASETS = {
    "timesheets_raw.csv": "Timesheets",
    "allocations_raw.csv": "Allocations",
    "billing_raw.csv": "Billing"
}


def main():
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    
    print("=" * 60)
    print("FEATURE ENGINEERING DEMO")
    print("=" * 60)
    
    for filename, label in RAW_DATASETS.items():
        file_path = data_dir / filename
        print(f"\n{'-' * 60}")
        print(f"Processing: {label}")
        print(f"{'-' * 60}")
        
        if not file_path.exists():
            print(f"  [MISSING] FILE NOT FOUND")
            continue
        
        try:
            df = load_csv(str(file_path))
            
            # Create derived columns
            df_derived = create_derived_columns(df)
            
            # Get feature summary
            summary = get_feature_summary(df_derived)
            
            print(f"  Original features: {len(df.columns)}")
            print(f"  Total features: {summary['total_features']}")
            print(f"  New features: {len(summary['new_features'])}")
            print(f"  New feature names: {summary['new_features']}")
            
            print(f"  [OK] PROCESSED")
            
        except Exception as e:
            print(f"  [ERROR] {str(e)}")
    
    print(f"\n{'=' * 60}")
    print("FEATURE ENGINEERING COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
