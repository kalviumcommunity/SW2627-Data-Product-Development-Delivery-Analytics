"""
Distribution Analysis Demo Script
Demonstrates distribution analysis on the raw datasets.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv
from src.analytics.distribution_analysis import (
    analyze_utilization_distribution,
    analyze_hours_distribution,
    analyze_billing_distribution,
    get_distribution_summary
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
    print("DISTRIBUTION ANALYSIS")
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
            
            # Get distribution summary
            summary = get_distribution_summary(df)
            
            print(f"  Total rows: {len(df)}")
            print(f"  Numeric columns: {len(summary)}")
            
            for col, stats in summary.items():
                if 'mean' in stats:
                    print(f"\n  {col}:")
                    print(f"    Mean: {stats['mean']:.2f}")
                    print(f"    Std: {stats['std']:.2f}")
                    print(f"    Min: {stats['min']:.2f}")
                    print(f"    Max: {stats['max']:.2f}")
            
            print(f"  [OK] ANALYZED")
            
        except Exception as e:
            print(f"  [ERROR] {str(e)}")
    
    print(f"\n{'=' * 60}")
    print("DISTRIBUTION ANALYSIS COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
