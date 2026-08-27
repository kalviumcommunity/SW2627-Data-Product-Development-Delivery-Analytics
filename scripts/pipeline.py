"""
Simple Data Pipeline Example
Demonstrates the read-process-output workflow pattern.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv, get_file_info
from src.processing.clean_data import get_basic_profile, clean_column_names
from src.output.export_data import export_csv


def run_pipeline(input_file: str, output_file: str) -> None:
    """
    Run a simple data pipeline: Read -> Process -> Output.
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file
    """
    print("=" * 50)
    print("STEP 1: READ - Loading data")
    print("=" * 50)
    df = load_csv(input_file)
    
    print("\n" + "=" * 50)
    print("STEP 2: PROCESS - Cleaning data")
    print("=" * 50)
    profile = get_basic_profile(df)
    print(f"Shape: {profile['shape']}")
    print(f"Columns: {profile['columns']}")
    
    df_clean = clean_column_names(df)
    print(f"Cleaned columns: {list(df_clean.columns)}")
    
    print("\n" + "=" * 50)
    print("STEP 3: OUTPUT - Exporting data")
    print("=" * 50)
    export_csv(df_clean, output_file)
    
    print("\nPipeline complete!")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pipeline.py <input_file> <output_file>")
        sys.exit(1)
    
    run_pipeline(sys.argv[1], sys.argv[2])
