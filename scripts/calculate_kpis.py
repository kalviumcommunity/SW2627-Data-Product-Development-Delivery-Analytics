"""
KPI Definition Demo Script
Demonstrates KPI calculation and business metric design on the raw datasets.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv
from src.analytics.kpi_definitions import (
    calculate_all_kpis,
    get_kpi_summary,
    get_kpi_targets,
    flag_kpi_violations,
    create_kpi_dashboard_data
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
    print("KPI DEFINITION & BUSINESS METRIC DESIGN")
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
            
            # Calculate all KPIs
            df_kpi = calculate_all_kpis(df)
            
            # Get KPI summary
            summary = get_kpi_summary(df_kpi)
            
            print(f"  Total rows: {len(df)}")
            print(f"  KPIs calculated: {len(summary)}")
            
            for kpi, stats in summary.items():
                print(f"\n  {kpi}:")
                print(f"    Mean: {stats['mean']:.2f}")
                print(f"    Median: {stats['median']:.2f}")
                print(f"    Std: {stats['std']:.2f}")
                print(f"    Range: {stats['min']:.2f} - {stats['max']:.2f}")
            
            # Get targets
            targets = get_kpi_targets()
            print(f"\n  KPI Targets:")
            for kpi, target in targets.items():
                if kpi in summary:
                    print(f"    {kpi}: target={target['target']}, warning={target['warning']}, critical={target['critical']}")
            
            # Flag violations
            print(f"\n  Violation Flags:")
            for kpi in summary.keys():
                if kpi in df.columns:
                    flags = flag_kpi_violations(df, kpi)
                    flag_counts = flags.value_counts().to_dict()
                    print(f"    {kpi}: {flag_counts}")
            
            # Dashboard data
            dashboard = create_kpi_dashboard_data(df)
            print(f"\n  Dashboard Summary:")
            for kpi, data in dashboard.items():
                print(f"    {kpi}: current={data['current']:.2f}, target={data['target']}, status={data['status']}")
            
            print(f"  [OK] ANALYZED")
            
        except Exception as e:
            print(f"  [ERROR] {str(e)}")
    
    print(f"\n{'=' * 60}")
    print("KPI DEFINITION COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()