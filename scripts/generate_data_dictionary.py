"""
Data Dictionary Report Script
Generates a comprehensive data dictionary report from the data dictionary CSV.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.profiling.data_dictionary import (
    load_data_dictionary,
    generate_data_dictionary_report,
    get_kpi_columns
)


def main():
    # Default to data/raw/ relative to project root
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    dict_path = data_dir / "data_dictionary.csv"
    
    if not dict_path.exists():
        print(f"[ERROR] Data dictionary not found: {dict_path}")
        sys.exit(1)
    
    print("Loading data dictionary...")
    data_dict = load_data_dictionary(str(dict_path))
    
    # Generate full report
    report = generate_data_dictionary_report(data_dict)
    print(report)
    
    # Show KPI-related columns
    print(f"\n{'=' * 70}")
    print("KPI-RELATED COLUMNS")
    print(f"{'=' * 70}")
    
    kpi_columns = get_kpi_columns(data_dict)
    for col in kpi_columns:
        print(f"\n  {col['file']}.{col['column']}")
        print(f"    {col['meaning']}")
        print(f"    Use: {col['project_use']}")
    
    print(f"\n{'=' * 70}")
    print(f"Total columns documented: {len(data_dict)}")
    print(f"KPI-related columns: {len(kpi_columns)}")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
