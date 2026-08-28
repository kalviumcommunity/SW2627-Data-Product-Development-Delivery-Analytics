"""
Time-Series Analysis Demo Script
Demonstrates time-series trend and rolling metrics on the raw datasets.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv
from src.analytics.time_series import (
    set_time_index,
    calculate_rolling_mean,
    calculate_rolling_std,
    calculate_monthly_trend,
    calculate_weekly_trend,
    detect_trend_direction,
    get_time_series_summary
)

import pandas as pd


# Define the raw datasets with date columns
RAW_DATASETS = {
    "timesheets_raw.csv": {"label": "Timesheets", "date_col": "work_date", "value_col": "billable_hours"},
    "allocations_raw.csv": {"label": "Allocations", "date_col": "allocation_start_date", "value_col": "allocated_hours"},
    "billing_raw.csv": {"label": "Billing", "date_col": "billing_date", "value_col": "billed_amount"}
}


def main():
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    
    print("=" * 60)
    print("TIME-SERIES TREND & ROLLING METRICS")
    print("=" * 60)
    
    for filename, config in RAW_DATASETS.items():
        file_path = data_dir / filename
        print(f"\n{'-' * 60}")
        print(f"Analyzing: {config['label']}")
        print(f"{'-' * 60}")
        
        if not file_path.exists():
            print(f"  [MISSING] FILE NOT FOUND")
            continue
        
        try:
            df = load_csv(str(file_path))
            
            date_col = config['date_col']
            value_col = config['value_col']
            
            if date_col not in df.columns or value_col not in df.columns:
                print(f"  [ERROR] Required columns not found")
                continue
            
            # Set time index
            df_ts = set_time_index(df, date_col)
            
            # Time series summary
            summary = get_time_series_summary(df, date_col, value_col)
            print(f"  Date range: {summary['date_range']['start']} to {summary['date_range']['end']}")
            print(f"  Total points: {summary['total_points']}")
            print(f"  Trend direction: {summary['trend_direction']}")
            print(f"  Value stats: mean={summary['value_stats']['mean']:.2f}, std={summary['value_stats']['std']:.2f}")
            
            # Rolling metrics
            rolling_mean_7 = calculate_rolling_mean(df_ts, value_col, 7)
            rolling_mean_30 = calculate_rolling_mean(df_ts, value_col, 30)
            rolling_std_7 = calculate_rolling_std(df_ts, value_col, 7)
            
            print(f"  Rolling mean (7d): {rolling_mean_7.iloc[-1]:.2f}")
            print(f"  Rolling mean (30d): {rolling_mean_30.iloc[-1]:.2f}")
            print(f"  Rolling std (7d): {rolling_std_7.iloc[-1]:.2f}")
            
            # Monthly trend
            monthly = calculate_monthly_trend(df, value_col, date_col)
            if not monthly.empty:
                print(f"  Monthly periods: {len(monthly)}")
                print(f"  Latest month total: {monthly['total'].iloc[-1]:.2f}")
                print(f"  MoM change: {monthly['mom_change_pct'].iloc[-1]:.2f}%")
            
            # Weekly trend
            weekly = calculate_weekly_trend(df, value_col, date_col)
            if not weekly.empty:
                print(f"  Weekly periods: {len(weekly)}")
                print(f"  Latest week total: {weekly['total'].iloc[-1]:.2f}")
                print(f"  WoW change: {weekly['wow_change_pct'].iloc[-1]:.2f}%")
            
            print(f"  [OK] ANALYZED")
            
        except Exception as e:
            print(f"  [ERROR] {str(e)}")
    
    print(f"\n{'=' * 60}")
    print("TIME-SERIES ANALYSIS COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()