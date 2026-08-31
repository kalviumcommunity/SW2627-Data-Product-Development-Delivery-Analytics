"""
KPI Card & Summary Metric Design Module
Provides functions for designing KPI cards and calculating summary metrics.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional


def calculate_employee_utilization_kpi(df: pd.DataFrame) -> Dict:
    """
    Calculate employee utilization KPI.
    
    Args:
        df: DataFrame with timesheet data containing hours_logged and billable_hours
    
    Returns:
        Dictionary with utilization KPI metrics
    """
    total_hours = pd.to_numeric(df['hours_logged'], errors='coerce').sum()
    total_billable = pd.to_numeric(df['billable_hours'], errors='coerce').sum()
    utilization_rate = round((total_billable / total_hours * 100) if total_hours > 0 and total_hours != float('inf') else 0, 2)
    
    return {
        'kpi_name': 'Employee Utilization Rate',
        'value': utilization_rate,
        'target': 65.0,
        'threshold': 60.0,
        'status': 'EXCEEDING' if utilization_rate >= 65 else 'WARNING' if utilization_rate >= 60 else 'CRITICAL',
        'total_employees': df['employee_id'].nunique() if 'employee_id' in df.columns else 0,
        'total_hours_logged': round(total_hours, 2),
        'total_billable_hours': round(total_billable, 2),
        'trend': 'IMPROVING' if utilization_rate > 68 else 'STABLE' if utilization_rate > 65 else 'DECLINING'
    }


def calculate_revenue_kpi(df: pd.DataFrame) -> Dict:
    """
    Calculate revenue KPI.
    
    Args:
        df: DataFrame with billing data containing billed_amount
    
    Returns:
        Dictionary with revenue KPI metrics
    """
    total_revenue = pd.to_numeric(df['billed_amount'], errors='coerce').sum() if 'billed_amount' in df.columns else 0
    avg_revenue = round(pd.to_numeric(df['billed_amount'], errors='coerce').mean(), 2) if 'billed_amount' in df.columns else 0
    total_transactions = len(df) if 'billed_amount' in df.columns else 0
    
    return {
        'kpi_name': 'Total Revenue',
        'value': total_revenue,
        'formatted_value': f'${total_revenue:,.2f}',
        'target': 50000000.0,
        'threshold': 40000000.0,
        'status': 'EXCEEDING' if total_revenue >= 50000000 else 'WARNING' if total_revenue >= 40000000 else 'CRITICAL',
        'avg_per_transaction': avg_revenue,
        'total_transactions': total_transactions,
        'trend': 'IMPROVING' if total_revenue > 45000000 else 'STABLE' if total_revenue > 40000000 else 'DECLINING'
    }


def calculate_allocation_kpi(df: pd.DataFrame) -> Dict:
    """
    Calculate allocation efficiency KPI.
    
    Args:
        df: DataFrame with allocation data containing allocated_hours and planned_billable_hours
    
    Returns:
        Dictionary with allocation KPI metrics
    """
    total_allocated = pd.to_numeric(df['allocated_hours'], errors='coerce').sum() if 'allocated_hours' in df.columns else 0
    total_planned = pd.to_numeric(df['planned_billable_hours'], errors='coerce').sum() if 'planned_billable_hours' in df.columns else 0
    efficiency = round((total_planned / total_allocated * 100) if total_allocated > 0 and total_allocated != float('inf') else 0, 2)
    
    return {
        'kpi_name': 'Allocation Efficiency',
        'value': efficiency,
        'target': 80.0,
        'threshold': 70.0,
        'status': 'EXCEEDING' if efficiency >= 80 else 'WARNING' if efficiency >= 70 else 'CRITICAL',
        'total_allocated_hours': round(total_allocated, 2),
        'total_planned_billable': round(total_planned, 2),
        'trend': 'IMPROVING' if efficiency > 85 else 'STABLE' if efficiency > 80 else 'DECLINING'
    }


def create_kpi_card(title: str, value: float, target: float, threshold: float) -> Dict:
    """
    Create KPI card structure.
    
    Args:
        title: KPI title
        value: Current value
        target: Target value
        threshold: Warning threshold
    
    Returns:
        Dictionary with KPI card structure
    """
    status = 'EXCEEDING' if value >= target else 'WARNING' if value >= threshold else 'CRITICAL'
    
    return {
        'title': title,
        'value': value,
        'formatted_value': format_number(value),
        'target': target,
        'threshold': threshold,
        'status': status,
        'progress': round((value / target * 100) if target > 0 else 0, 2)
    }


def format_number(value: float, format_type: str = 'currency') -> str:
    """
    Format number for display.
    
    Args:
        value: Number to format
        format_type: Type of format ('currency', 'percentage', 'general')
    
    Returns:
        Formatted string
    """
    if format_type == 'currency':
        if abs(value) >= 1000000:
            return f'${value/1000000:,.1f}M'
        elif abs(value) >= 1000:
            return f'${value/1000:,.1f}K'
        else:
            return f'${value:,.2f}'
    elif format_type == 'percentage':
        return f'{value:.1f}%'
    else:
        if abs(value) >= 1000000:
            return f'{value/1000000:,.1f}M'
        elif abs(value) >= 1000:
            return f'{value/1000:,.1f}K'
        else:
            return f'{value:,.2f}'


def get_summary_metrics(df: pd.DataFrame, metric_col: str, group_col: str = None) -> Dict:
    """
    Get summary metrics for a DataFrame.
    
    Args:
        df: DataFrame with data
        metric_col: Column with metric values
        group_col: Column to group by
    
    Returns:
        Dictionary with summary metrics
    """
    metric_data = pd.to_numeric(df[metric_col], errors='coerce').dropna()
    
    summary = {
        'total': round(float(metric_data.sum()), 2),
        'average': round(float(metric_data.mean()), 2),
        'median': round(float(metric_data.median()), 2),
        'minimum': round(float(metric_data.min()), 2),
        'maximum': round(float(metric_data.max()), 2),
        'std_deviation': round(float(metric_data.std()), 2),
        'count': int(metric_data.count())
    }
    
    if group_col and group_col in df.columns:
        group_summary = df.groupby(group_col)[metric_col].agg(['sum', 'mean', 'count'])
        summary['by_group'] = {
            str(k): {
                'total': round(float(v['sum']), 2),
                'average': round(float(v['mean']), 2),
                'count': int(v['count'])
            }
            for k, v in group_summary.iterrows()
        }
    
    return summary


def validate_kpi_data(df: pd.DataFrame, required_columns: List[str]) -> Dict:
    """
    Validate KPI data quality.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required columns
    
    Returns:
        Dictionary with validation results
    """
    missing = [col for col in required_columns if col not in df.columns]
    null_counts = df[required_columns].isnull().sum() if all(col in df.columns for col in required_columns) else {}
    
    return {
        'valid': len(missing) == 0,
        'missing_columns': missing,
        'total_null_count': int(null_counts.sum()) if not missing else 0,
        'total_rows': len(df),
        'data_quality_score': round(max(0, 100 - (len(missing) * 15 - int(null_counts.sum()) * 2)), 2) if not missing else 0
    }