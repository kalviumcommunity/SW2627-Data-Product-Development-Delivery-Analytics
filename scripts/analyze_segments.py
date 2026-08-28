"""
GroupBy Aggregation Demo Script
Demonstrates segment analysis and groupby operations on the raw datasets.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv
from src.analytics.groupby_analysis import (
    analyze_by_department,
    analyze_utilization_by_segment,
    calculate_department_summary,
    calculate_employee_summary,
    find_top_performers,
    find_bottom_performers,
    get_segment_insights
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
    print("GROUPBY AGGREGATION & SEGMENT INSIGHTS")
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
            
            print(f"  Total rows: {len(df)}")
            print(f"  Columns: {list(df.columns)}")
            
            # Get segment insights
            insights = get_segment_insights(df)
            
            # Print department analysis
            if 'by_department' in insights and insights['by_department']:
                print(f"\n  Department Analysis (billable_hours):")
                dept_df = pd.DataFrame(insights['by_department']).T
                print(dept_df.head())
            
            # Print top performers
            if 'billable_hours' in df.columns:
                top_performers = find_top_performers(df, 'billable_hours', 5)
                if not top_performers.empty:
                    print(f"\n  Top 5 by billable_hours:")
                    print(top_performers[['employee_id', 'billable_hours']].head() if 'employee_id' in top_performers.columns else top_performers.head())
            
            # Print department summary
            dept_summary = calculate_department_summary(df)
            if not dept_summary.empty:
                print(f"\n  Department Summary:")
                print(dept_summary.head())
            
            print(f"  [OK] ANALYZED")
            
        except Exception as e:
            print(f"  [ERROR] {str(e)}")
    
    print(f"\n{'=' * 60}")
    print("GROUPBY AGGREGATION COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    import pandas as pd
    main()