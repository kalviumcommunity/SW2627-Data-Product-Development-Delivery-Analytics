"""
Interactive Plotly Chart Design Demo Script
Demonstrates creating interactive Plotly visualizations.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from src.ingestion.load_data import load_csv
from src.viz.plotly_charts import (
    create_bar_chart,
    create_line_chart,
    create_pie_chart,
    create_scatter_chart,
    create_histogram,
    create_box_plot,
    create_heatmap,
    create_grouped_bar_chart,
    get_chart_recommendations
)


# Define the raw datasets
RAW_DATASETS = {
    "employee_master_raw.csv": "Employees",
    "timesheets_raw.csv": "Timesheets",
    "billing_raw.csv": "Billing"
}


def main():
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    
    print("=" * 60)
    print("INTERACTIVE PLOTLY CHART DESIGN")
    print("=" * 60)
    
    # Load datasets
    print("\n--- Loading Data ---")
    datasets = {}
    for filename, label in RAW_DATASETS.items():
        file_path = data_dir / filename
        if file_path.exists():
            df = load_csv(str(file_path))
            datasets[label] = df
            print(f"Loaded {label}: {len(df)} rows")
    
    # Bar chart
    print("\n" + "=" * 60)
    print("CHART CONFIGURATIONS")
    print("=" * 60)
    
    if 'Employees' in datasets:
        emp = datasets['Employees']
        dept_counts = emp['department'].value_counts().reset_index()
        dept_counts.columns = ['department', 'count']
        
        print("\n--- Bar Chart: Employees by Department ---")
        bar = create_bar_chart(dept_counts, 'department', 'count', 'Employees by Department')
        print(f"  Type: {bar['type']}")
        print(f"  Title: {bar['title']}")
        print(f"  Categories: {len(bar['x'])}")
    
    # Pie chart
    if 'Employees' in datasets:
        print("\n--- Pie Chart: Department Distribution ---")
        pie = create_pie_chart(dept_counts, 'department', 'count', 'Department Distribution')
        print(f"  Type: {pie['type']}")
        print(f"  Title: {pie['title']}")
        print(f"  Slices: {len(pie['labels'])}")
    
    # Histogram
    if 'Timesheets' in datasets:
        ts = datasets['Timesheets']
        print("\n--- Histogram: Hours Logged Distribution ---")
        hist = create_histogram(ts, 'hours_logged', 30, 'Hours Logged Distribution')
        print(f"  Type: {hist['type']}")
        print(f"  Title: {hist['title']}")
        print(f"  Data points: {len(hist['x'])}")
    
    # Box plot
    if 'Timesheets' in datasets:
        print("\n--- Box Plot: Billable Hours by Task Category ---")
        box = create_box_plot(ts, 'billable_hours', 'task_category', 'Billable Hours by Task')
        print(f"  Type: {box['type']}")
        print(f"  Title: {box['title']}")
    
    # Scatter chart
    if 'Timesheets' in datasets:
        print("\n--- Scatter: Hours vs Billable Hours ---")
        scatter = create_scatter_chart(ts, 'hours_logged', 'billable_hours', 'Hours vs Billable')
        print(f"  Type: {scatter['type']}")
        print(f"  Title: {scatter['title']}")
        print(f"  Data points: {len(scatter['x'])}")
    
    # Grouped bar chart
    if 'Timesheets' in datasets:
        print("\n--- Grouped Bar: Task Hours by Category ---")
        task_hours = ts.groupby(['task_category', 'work_location'])['hours_logged'].sum().reset_index()
        grouped = create_grouped_bar_chart(task_hours, 'task_category', 'hours_logged', 'work_location', 'Task Hours by Category')
        print(f"  Type: {grouped['type']}")
        print(f"  Title: {grouped['title']}")
        print(f"  Groups: {len(grouped['traces'])}")
    
    # Chart recommendations
    print("\n" + "=" * 60)
    print("CHART RECOMMENDATIONS")
    print("=" * 60)
    
    if 'Timesheets' in datasets:
        ts = datasets['Timesheets']
        recommendations = get_chart_recommendations(ts, 'hours_logged', 'task_category')
        
        for i, rec in enumerate(recommendations, 1):
            print(f"\n  {i}. {rec['chart_type'].upper()}: {rec['description']}")
    
    print(f"\n{'=' * 60}")
    print("PLOTLY CHART DESIGN COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()