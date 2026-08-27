"""
Data Ingestion Script
Loads all raw datasets and generates ingestion reports.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv, get_file_info, generate_ingestion_report


# Define the raw datasets to load
RAW_DATASETS = {
    "employee_master_raw.csv": "Employee Master",
    "timesheets_raw.csv": "Timesheets",
    "allocations_raw.csv": "Allocations",
    "billing_raw.csv": "Billing"
}


def ingest_all_datasets(data_dir: str) -> dict:
    """
    Ingest all raw datasets and generate reports.
    
    Args:
        data_dir: Path to the raw data directory
    
    Returns:
        Dictionary mapping dataset names to DataFrames
    """
    data_path = Path(data_dir)
    datasets = {}
    reports = {}
    
    print("=" * 60)
    print("DATA INGESTION REPORT")
    print("=" * 60)
    
    for filename, label in RAW_DATASETS.items():
        file_path = data_path / filename
        print(f"\n{'─' * 60}")
        print(f"Loading: {label} ({filename})")
        print(f"{'─' * 60}")
        
        # Check file info
        info = get_file_info(str(file_path))
        print(f"  File size: {info['size_mb']} MB")
        print(f"  Extension: {info['extension']}")
        
        if not info["exists"]:
            print(f"  ❌ FILE NOT FOUND")
            continue
        
        try:
            df = load_csv(str(file_path))
            report = generate_ingestion_report(df, label)
            
            print(f"  Rows: {report['rows']}")
            print(f"  Columns: {report['columns']}")
            print(f"  Memory: {report['memory_mb']} MB")
            print(f"  Null columns: {sum(1 for v in report['null_counts'].values() if v > 0)}")
            print(f"  ✅ LOADED SUCCESSFULLY")
            
            datasets[filename] = df
            reports[filename] = report
            
        except Exception as e:
            print(f"  ❌ ERROR: {str(e)}")
    
    print(f"\n{'=' * 60}")
    print(f"SUMMARY: Loaded {len(datasets)}/{len(RAW_DATASETS)} datasets")
    print(f"{'=' * 60}")
    
    return datasets


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ingest_data.py <data_directory>")
        sys.exit(1)
    
    datasets = ingest_all_datasets(sys.argv[1])
