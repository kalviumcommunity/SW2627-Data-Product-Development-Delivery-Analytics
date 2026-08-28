"""
Dataset Profiling Script
Profiles all raw datasets and generates quality reports.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv
from src.profiling.profile_dataset import (
    profile_dataframe,
    detect_missing_patterns,
    detect_duplicates,
    profile_categorical_columns,
    profile_numeric_columns
)


# Define the raw datasets to profile
RAW_DATASETS = {
    "employee_master_raw.csv": "Employee Master",
    "timesheets_raw.csv": "Timesheets",
    "allocations_raw.csv": "Allocations",
    "billing_raw.csv": "Billing"
}


def profile_all_datasets(data_dir: str) -> None:
    """
    Profile all raw datasets and generate reports.
    
    Args:
        data_dir: Path to the raw data directory
    """
    data_path = Path(data_dir)
    
    print("=" * 60)
    print("DATASET PROFILING REPORT")
    print("=" * 60)
    
    for filename, label in RAW_DATASETS.items():
        file_path = data_path / filename
        print(f"\n{'-' * 60}")
        print(f"Profiling: {label} ({filename})")
        print(f"{'-' * 60}")
        
        if not file_path.exists():
            print(f"  [MISSING] FILE NOT FOUND")
            continue
        
        try:
            df = load_csv(str(file_path))
            
            # Basic profile
            profile = profile_dataframe(df, label)
            print(f"  Shape: {profile['shape']}")
            print(f"  Memory: {profile['memory_mb']} MB")
            
            # Missing patterns
            missing = detect_missing_patterns(df)
            print(f"  Total missing: {missing['total_missing']} ({missing['missing_percentage']}%)")
            print(f"  Columns with missing: {len(missing['columns_with_missing'])}")
            
            # Duplicates
            duplicates = detect_duplicates(df)
            print(f"  Duplicate rows: {duplicates['total_duplicates']} ({duplicates['duplicate_percentage']}%)")
            
            # Column details
            print(f"\n  Column Details:")
            for col_info in profile["column_info"]:
                null_str = f"nulls={col_info['null_count']}" if col_info['null_count'] > 0 else ""
                unique_str = f"unique={col_info['unique_count']}"
                dtype_str = f"type={col_info['dtype']}"
                print(f"    {col_info['name']}: {dtype_str}, {unique_str} {null_str}")
            
            print(f"  [OK] PROFILED SUCCESSFULLY")
            
        except Exception as e:
            print(f"  [ERROR] {str(e)}")
    
    print(f"\n{'=' * 60}")
    print("PROFILING COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        data_dir = sys.argv[1]
    else:
        data_dir = str(Path(__file__).parent.parent / "data" / "raw")
        print(f"No directory specified, using default: {data_dir}")
    
    profile_all_datasets(data_dir)
