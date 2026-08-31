"""
Insight Export & Report Generation Module
Provides functions for exporting insights and generating comprehensive reports.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime


def export_to_csv(df: pd.DataFrame, file_path: str, columns: List[str] = None) -> Dict:
    """
    Export DataFrame to CSV file.
    
    Args:
        df: DataFrame to export
        file_path: Path to output file
        columns: Columns to include (None for all)
    
    Returns:
        Dictionary with export results
    """
    if columns:
        df = df[columns]
    
    df.to_csv(file_path, index=False)
    
    return {
        'success': True,
        'file_path': file_path,
        'rows_exported': len(df),
        'columns_exported': len(df.columns),
        'export_timestamp': datetime.now().isoformat()
    }


def export_to_json(df: pd.DataFrame, file_path: str, orient: str = 'records') -> Dict:
    """
    Export DataFrame to JSON file.
    
    Args:
        df: DataFrame to export
        file_path: Path to output file
        orient: JSON orientation format
    
    Returns:
        Dictionary with export results
    """
    df.to_json(file_path, orient=orient, date_format='iso')
    
    return {
        'success': True,
        'file_path': file_path,
        'rows_exported': len(df),
        'export_timestamp': datetime.now().isoformat()
    }


def generate_insight_report(df: pd.DataFrame, metric_col: str, group_col: str = None) -> Dict:
    """
    Generate a comprehensive insight report from DataFrame.
    
    Args:
        df: DataFrame with data
        metric_col: Column with metric values
        group_col: Column to group by (optional)
    
    Returns:
        Dictionary with insight report
    """
    metric_data = pd.to_numeric(df[metric_col], errors='coerce').dropna()
    
    total = float(metric_data.sum())
    average = float(metric_data.mean())
    median = float(metric_data.median())
    minimum = float(metric_data.min())
    maximum = float(metric_data.max())
    std_dev = float(metric_data.std())
    count = int(metric_data.count())
    
    # Determine trend
    trend = "STABLE"
    if count > 1:
        first_half = metric_data.iloc[:len(metric_data)//2].mean()
        second_half = metric_data.iloc[len(metric_data)//2:].mean()
        if second_half > first_half * 1.05:
            trend = "IMPROVING"
        elif second_half < first_half * 0.95:
            trend = "DECLINING"
    
    # Group analysis if group_col provided
    group_analysis = {}
    if group_col and group_col in df.columns:
        for group in df[group_col].unique():
            group_df = df[df[group_col] == group]
            group_metric = pd.to_numeric(group_df[metric_col], errors='coerce').dropna()
            if len(group_metric) > 0:
                group_analysis[str(group)] = {
                    'total': float(group_metric.sum()),
                    'average': float(group_metric.mean()),
                    'count': int(len(group_metric))
                }
    
    return {
        'metric': metric_col,
        'total': total,
        'average': average,
        'median': median,
        'minimum': minimum,
        'maximum': maximum,
        'std_dev': std_dev,
        'count': count,
        'trend': trend,
        'group_analysis': group_analysis,
        'insights': {
            'total_insight': f"Analyzed {count:,} data points with average {average:.2f}",
            'trend_insight': f"Shows {trend.lower()} trend over the analysis period",
            'range_insight': f"Range from {minimum:.2f} to {maximum:.2f} indicates {maximum - minimum:.2f} units of variation"
        }
    }


def generate_comparative_report(df1: pd.DataFrame, df2: pd.DataFrame, metric_col: str, 
                                 group_col: str = None) -> Dict:
    """
    Generate a comparative report between two DataFrames.
    
    Args:
        df1: First DataFrame
        df2: Second DataFrame
        metric_col: Column with metric values
        group_col: Column to group by (optional)
    
    Returns:
        Dictionary with comparative report
    """
    metric1 = pd.to_numeric(df1[metric_col], errors='coerce').dropna()
    metric2 = pd.to_numeric(df2[metric_col], errors='coerce').dropna()
    
    return {
        'metric': metric_col,
        'df1_total': float(metric1.sum()),
        'df2_total': float(metric2.sum()),
        'df1_average': float(metric1.mean()),
        'df2_average': float(metric2.mean()),
        'df1_count': int(metric1.count()),
        'df2_count': int(metric2.count()),
        'difference': float(metric2.sum() - metric1.sum()),
        'percentage_change': float((metric2.sum() - metric1.sum()) / metric1.sum() * 100) if metric1.sum() != 0 else 0,
        'trend': 'IMPROVING' if metric2.sum() > metric1.sum() else 'DECLINING' if metric2.sum() < metric1.sum() else 'STABLE',
        'group_analysis': {}
    }


def validate_export_data(df: pd.DataFrame, required_columns: List[str]) -> Dict:
    """
    Validate data before export.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required columns
    
    Returns:
        Dictionary with validation results
    """
    missing = [col for col in required_columns if col not in df.columns]
    null_count = df[required_columns].isnull().sum().sum() if all(col in df.columns for col in required_columns) else 0
    
    return {
        'valid': len(missing) == 0,
        'missing_columns': missing,
        'null_count': int(null_count),
        'total_rows': len(df)
    }


def get_export_format_recommendations(df: pd.DataFrame, metric_col: str) -> Dict:
    """
    Get export format recommendations based on data characteristics.
    
    Args:
        df: DataFrame with data
        metric_col: Column with metric values
    
    Returns:
        Dictionary with format recommendations
    """
    metric_data = pd.to_numeric(df[metric_col], errors='coerce').dropna()
    count = int(metric_data.count())
    avg = float(metric_data.mean())
    
    return {
        'recommended_format': 'csv' if count > 1000 else 'json',
        'compression': 'recommended for large exports',
        'include_timestamps': True,
        'include_metadata': avg >= 65,
        'batch_size': 10000
    }
