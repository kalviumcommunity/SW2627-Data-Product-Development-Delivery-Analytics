"""
Root Cause Analysis Demo Script
Demonstrates root cause investigation workflow on the raw datasets.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv
from src.features.derive_features import create_derived_columns
from src.analytics.root_cause import (
    investigate_low_utilization,
    identify_bottlenecks,
    analyze_task_distribution,
    compare_allocated_vs_actual,
    generate_root_cause_report,
    get_root_cause_summary
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
    print("ROOT CAUSE INVESTIGATION WORKFLOW")
    print("=" * 60)
    
    # Load all datasets
    datasets = {}
    for filename, label in RAW_DATASETS.items():
        file_path = data_dir / filename
        if file_path.exists():
            datasets[label] = load_csv(str(file_path))
            print(f"Loaded {label}: {len(datasets[label])} rows")
    
    if 'Timesheets' not in datasets:
        print("[ERROR] Timesheets dataset not found")
        return
    
    # Create derived columns for KPIs
    print("\n" + "=" * 60)
    print("CREATING DERIVED COLUMNS")
    print("=" * 60)
    
    from src.features.derive_features import create_derived_columns
    timesheets = create_derived_columns(datasets['Timesheets'])
    
    if 'Allocations' in datasets:
        allocations = create_derived_columns(datasets['Allocations'])
    else:
        allocations = None
    
    if 'Billing' in datasets:
        billing = create_derived_columns(datasets['Billing'])
    else:
        billing = None
    
    print("\n" + "=" * 60)
    print("ROOT CAUSE ANALYSIS")
    print("=" * 60)
    
    # Investigate low utilization
    print("\n--- Low Utilization Investigation ---")
    low_util = investigate_low_utilization(timesheets)
    print(f"Low utilization count: {low_util.get('low_utilization_count', 0)}")
    print(f"Low utilization %: {low_util.get('low_utilization_pct', 0)}%")
    if 'affected_employees' in low_util:
        print(f"Affected employees: {len(low_util['affected_employees'])}")
    
    # Identify bottlenecks
    print("\n--- Bottleneck Identification ---")
    bottlenecks = identify_bottlenecks(timesheets)
    for key, value in bottlenecks.items():
        print(f"  {key}: {value}")
    
    # Compare allocated vs actual
    if allocations is not None:
        print("\n--- Allocated vs Actual Comparison ---")
        alloc_vs_actual = compare_allocated_vs_actual(allocations)
        if 'overall' in alloc_vs_actual:
            overall = alloc_vs_actual['overall']
            print(f"  Total allocated: {overall['total_allocated']}")
            print(f"  Total actual: {overall['total_actual']}")
            print(f"  Variance: {overall['total_variance']}")
            print(f"  Over allocated: {overall['over_allocated_count']}")
            print(f"  Under allocated: {overall['under_allocated_count']}")
    
    # Generate root cause report
    print("\n--- Root Cause Report ---")
    report = generate_root_cause_report(timesheets)
    summary = get_root_cause_summary(report)
    
    if 'low_utilization_pct' in summary:
        print(f"  Low utilization: {summary['low_utilization_pct']}%")
    
    if 'bottlenecks' in summary:
        print(f"  Bottlenecks:")
        for key, value in summary['bottlenecks'].items():
            print(f"    {key}: {value}")
    
    if 'affected_employee_count' in summary:
        print(f"  Affected employees: {summary['affected_employee_count']}")
    
    print(f"\n{'=' * 60}")
    print("ROOT CAUSE ANALYSIS COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()