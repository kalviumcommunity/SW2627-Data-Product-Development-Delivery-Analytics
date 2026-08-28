"""
GroupBy Aggregation & Segment Insights Module
Provides functions for segment analysis and groupby operations.
"""

import pandas as pd
import numpy as np


def analyze_by_department(df: pd.DataFrame, metric_col: str = 'billable_hours') -> pd.DataFrame:
    """
    Analyze metrics by department.
    
    Args:
        df: pandas DataFrame
        metric_col: Column to aggregate
    
    Returns:
        DataFrame with department analysis
    """
    if 'department' not in df.columns or metric_col not in df.columns:
        return pd.DataFrame()
    
    return df.groupby('department')[metric_col].agg([
        'count', 'mean', 'median', 'std', 'min', 'max', 'sum'
    ]).round(2).sort_values('mean', ascending=False)


def analyze_by_team(df: pd.DataFrame, metric_col: str = 'billable_hours') -> pd.DataFrame:
    """
    Analyze metrics by team.
    
    Args:
        df: pandas DataFrame
        metric_col: Column to aggregate
    
    Returns:
        DataFrame with team analysis
    """
    if 'team' not in df.columns or metric_col not in df.columns:
        return pd.DataFrame()
    
    return df.groupby('team')[metric_col].agg([
        'count', 'mean', 'median', 'std', 'min', 'max', 'sum'
    ]).round(2).sort_values('mean', ascending=False)


def analyze_by_experience_segment(df: pd.DataFrame, metric_col: str = 'billable_hours') -> pd.DataFrame:
    """
    Analyze metrics by experience segment.
    
    Args:
        df: pandas DataFrame
        metric_col: Column to aggregate
    
    Returns:
        DataFrame with experience segment analysis
    """
    if 'experience_segment' not in df.columns or metric_col not in df.columns:
        return pd.DataFrame()
    
    return df.groupby('experience_segment')[metric_col].agg([
        'count', 'mean', 'median', 'std', 'min', 'max', 'sum'
    ]).round(2).sort_values('mean', ascending=False)


def analyze_utilization_by_segment(df: pd.DataFrame, segment_col: str) -> pd.DataFrame:
    """
    Analyze utilization rate by segment.
    
    Args:
        df: pandas DataFrame
        segment_col: Segment column to group by
    
    Returns:
        DataFrame with utilization analysis by segment
    """
    required_cols = ['billable_hours', 'total_hours', segment_col]
    if not all(col in df.columns for col in required_cols):
        return pd.DataFrame()
    
    # Calculate utilization rate
    df = df.copy()
    df['utilization_rate'] = (df['billable_hours'] / df['total_hours'] * 100).fillna(0)
    
    return df.groupby(segment_col)['utilization_rate'].agg([
        'count', 'mean', 'median', 'std', 'min', 'max'
    ]).round(2).sort_values('mean', ascending=False)


def find_top_performers(df: pd.DataFrame, metric_col: str, n: int = 10) -> pd.DataFrame:
    """
    Find top N performers by metric.
    
    Args:
        df: pandas DataFrame
        metric_col: Column to rank by
        n: Number of top performers
    
    Returns:
        DataFrame with top performers
    """
    if metric_col not in df.columns:
        return pd.DataFrame()
    
    return df.nlargest(n, metric_col)


def find_bottom_performers(df: pd.DataFrame, metric_col: str, n: int = 10) -> pd.DataFrame:
    """
    Find bottom N performers by metric.
    
    Args:
        df: pandas DataFrame
        metric_col: Column to rank by
        n: Number of bottom performers
    
    Returns:
        DataFrame with bottom performers
    """
    if metric_col not in df.columns:
        return pd.DataFrame()
    
    return df.nsmallest(n, metric_col)


def calculate_department_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate comprehensive department summary.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        DataFrame with department summary
    """
    required_cols = ['department', 'billable_hours', 'total_hours', 'hours_worked']
    if not all(col in df.columns for col in required_cols):
        return pd.DataFrame()
    
    df = df.copy()
    df['utilization_rate'] = (df['billable_hours'] / df['total_hours'] * 100).fillna(0)
    df['efficiency'] = (df['hours_worked'] / df['total_hours'] * 100).fillna(0)
    
    summary = df.groupby('department').agg(
        employee_count=('employee_id', 'nunique') if 'employee_id' in df.columns else ('billable_hours', 'count'),
        total_billable_hours=('billable_hours', 'sum'),
        total_hours=('total_hours', 'sum'),
        avg_utilization=('utilization_rate', 'mean'),
        avg_efficiency=('efficiency', 'mean'),
        avg_billable_hours=('billable_hours', 'mean'),
        utilization_std=('utilization_rate', 'std')
    ).round(2)
    
    return summary.sort_values('avg_utilization', ascending=False)


def calculate_project_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate project-level summary.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        DataFrame with project summary
    """
    if 'project_id' not in df.columns:
        return pd.DataFrame()
    
    agg_dict = {
        'hours_worked': ['sum', 'mean', 'count'],
        'billable_hours': ['sum', 'mean'],
    }
    
    if 'billed_amount' in df.columns:
        agg_dict['billed_amount'] = ['sum', 'mean']
    
    summary = df.groupby('project_id').agg(agg_dict).round(2)
    summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
    
    return summary.sort_values('hours_worked_sum', ascending=False)


def calculate_employee_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate employee-level summary.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        DataFrame with employee summary
    """
    required_cols = ['employee_id', 'billable_hours', 'total_hours']
    if not all(col in df.columns for col in required_cols):
        return pd.DataFrame()
    
    df = df.copy()
    df['utilization_rate'] = (df['billable_hours'] / df['total_hours'] * 100).fillna(0)
    
    summary = df.groupby('employee_id').agg(
        total_entries=('billable_hours', 'count'),
        total_billable_hours=('billable_hours', 'sum'),
        total_hours=('total_hours', 'sum'),
        avg_utilization=('utilization_rate', 'mean'),
        max_utilization=('utilization_rate', 'max'),
        min_utilization=('utilization_rate', 'min'),
        utilization_std=('utilization_rate', 'std')
    ).round(2)
    
    return summary.sort_values('avg_utilization', ascending=False)


def get_segment_insights(df: pd.DataFrame) -> dict:
    """
    Get comprehensive segment insights.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        Dictionary with segment insights
    """
    insights = {}
    
    # Department insights
    if 'department' in df.columns:
        insights['by_department'] = analyze_by_department(df).to_dict()
    
    # Team insights
    if 'team' in df.columns:
        insights['by_team'] = analyze_by_team(df).to_dict()
    
    # Experience segment insights
    if 'experience_segment' in df.columns:
        insights['by_experience'] = analyze_by_experience_segment(df).to_dict()
    
    # Utilization by segments
    for segment_col in ['department', 'team', 'experience_segment']:
        if segment_col in df.columns:
            insights[f'utilization_by_{segment_col}'] = analyze_utilization_by_segment(df, segment_col).to_dict()
    
    # Department summary
    insights['department_summary'] = calculate_department_summary(df).to_dict()
    
    # Employee summary
    insights['employee_summary'] = calculate_employee_summary(df).to_dict()
    
    return insights