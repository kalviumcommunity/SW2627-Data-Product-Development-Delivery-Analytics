"""
Data Consistency Validation Script
Demonstrates consistency and validation rules on the raw datasets.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv
from src.profiling.consistency_rules import run_all_validations


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
    print("DATA CONSISTENCY VALIDATION")
    print("=" * 60)
    
    for filename, label in RAW_DATASETS.items():
        file_path = data_dir / filename
        
        if not file_path.exists():
            print(f"\n[MISSING] {label}: FILE NOT FOUND")
            continue
        
        try:
            df = load_csv(str(file_path))
            results = run_all_validations(df, label)
            
        except Exception as e:
            print(f"\n[ERROR] {label}: {str(e)}")
    
    print(f"\n{'=' * 60}")
    print("VALIDATION COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
