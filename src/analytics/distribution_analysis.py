"""
Distribution Analysis Module
Provides functions for analyzing data distributions.
"""

import pandas as pd
import numpy as np


def analyze_numeric_distribution(df: pd.DataFrame, column: str) -> dict:
    """
    Analyze distribution of a numeric column.
    
    Args:
        df: pandas DataFrame
        column: Column to analyze
    
    Returns:
        Dictionary with distribution statistics
    """
    if column not in df.columns:
        return {'error': f'Column {column} not found'}
    
    if not pd.api.types.is_numeric_dtype(df[column]):
        return {'error': f'Column {column} is not numeric'}
    
    data = df[column].dropna()
    
    return {
        'column': column,
        'count': len(data),
        'mean': data.mean(),
        'std': data.std(),
        'min': data.min(),
        'q1': data.quantile(0.25),
        'median': data.median(),
        'q3': data.quantile(0.75),
        'max': data.max(),
        'skewness': data.skew(),
        'kurtosis': data.kurtosis()
    }


def analyze_categorical_distribution(df: pd.DataFrame, column: str) -> dict:
    """
    Analyze distribution of a categorical column.
    
    Args:
        df: pandas DataFrame
        column: Column to analyze
    
    Returns:
        Dictionary with distribution statistics
    """
    if column not in df.columns:
        return {'error': f'Column {column} not found'}
    
    value_counts = df[column].value_counts()
    
    return {
        'column': column,
        'total_count': len(df[column]),
        'unique_count': df[column].nunique(),
        'null_count': df[column].isna().sum(),
        'top_values': value_counts.head(10).to_dict(),
        'top_value_pct': round(value_counts.iloc[0] / len(df) * 100, 2) if len(value_counts) > 0 else 0
    }


def analyze_utilization_distribution(df: pd.DataFrame) -> dict:
    """
    Analyze utilization rate distribution.
    
    Args:
        df: pandas DataFrame with utilization data
    
    Returns:
        Dictionary with utilization distribution
    """
    if 'utilization_rate' not in df.columns:
        return {'error': 'utilization_rate column not found'}
    
    util_data = df['utilization_rate'].dropna()
    
    # Define utilization bands
    bands = [0, 20, 40, 60, 80, 100, float('inf')]
    labels = ['0-20%', '20-40%', '40-60%', '60-80%', '80-100%', '100%+']
    
    distribution = pd.cut(util_data, bins=bands, labels=labels, right=False).value_counts().sort_index()
    
    return {
        'mean': util_data.mean(),
        'median': util_data.median(),
        'std': util_data.std(),
        'distribution': distribution.to_dict(),
        'below_60_pct': round((util_data < 60).sum() / len(util_data) * 100, 2),
        'above_80_pct': round((util_data > 80).sum() / len(util_data) * 100, 2)
    }


def analyze_hours_distribution(df: pd.DataFrame) -> dict:
    """
    Analyze hours worked distribution.
    
    Args:
        df: pandas DataFrame with hours data
    
    Returns:
        Dictionary with hours distribution
    """
    if 'hours_worked' not in df.columns:
        return {'error': 'hours_worked column not found'}
    
    hours_data = df['hours_worked'].dropna()
    
    return {
        'mean': hours_data.mean(),
        'median': hours_data.median(),
        'std': hours_data.std(),
        'min': hours_data.min(),
        'max': hours_data.max(),
        'daily_avg': hours_data.mean(),
        'weekly_avg': hours_data.mean() * 5,
        'overtime_pct': round((hours_data > 8).sum() / len(hours_data) * 100, 2)
    }


def analyze_billing_distribution(df: pd.DataFrame) -> dict:
    """
    Analyze billing amount distribution.
    
    Args:
        df: pandas DataFrame with billing data
    
    Returns:
        Dictionary with billing distribution
    """
    if 'billed_amount' not in df.columns:
        return {'error': 'billed_amount column not found'}
    
    billing_data = df['billed_amount'].dropna()
    
    return {
        'mean': billing_data.mean(),
        'median': billing_data.median(),
        'std': billing_data.std(),
        'min': billing_data.min(),
        'max': billing_data.max(),
        'total': billing_data.sum(),
        'avg_per_employee': billing_data.mean()
    }


def get_distribution_summary(df: pd.DataFrame, columns: list = None) -> dict:
    """
    Get distribution summary for multiple columns.
    
    Args:
        df: pandas DataFrame
        columns: List of columns to analyze (None for all numeric columns)
    
    Returns:
        Dictionary with distribution summaries
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    summary = {}
    
    for col in columns:
        if col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                summary[col] = analyze_numeric_distribution(df, col)
            else:
                summary[col] = analyze_categorical_distribution(df, col)
    
    return summary
