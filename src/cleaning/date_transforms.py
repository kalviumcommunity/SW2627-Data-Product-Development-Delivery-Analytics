"""
Date Transformation Module
Provides functions for parsing and transforming date/time data.
"""

import pandas as pd
from datetime import datetime


def parse_dates(df: pd.DataFrame, columns: list = None, format: str = 'auto') -> pd.DataFrame:
    """
    Parse date columns to datetime format.
    
    Args:
        df: pandas DataFrame
        columns: List of columns to parse (None for all string/object columns)
        format: Date format ('auto' for automatic detection, or strftime format)
    
    Returns:
        DataFrame with parsed dates
    """
    df = df.copy()
    
    if columns is None:
        # Find columns that might be dates
        columns = []
        for col in df.select_dtypes(include=['object']).columns:
            # Check if column contains date-like strings
            sample = df[col].dropna().head(10)
            if sample.str.match(r'\d{4}-\d{2}-\d{2}').any():
                columns.append(col)
    
    for col in columns:
        if col in df.columns:
            if format == 'auto':
                df[col] = pd.to_datetime(df[col], errors='coerce')
            else:
                df[col] = pd.to_datetime(df[col], format=format, errors='coerce')
    
    print(f"  Parsed dates in {len(columns)} columns")
    return df


def extract_date_features(df: pd.DataFrame, date_column: str, prefix: str = None) -> pd.DataFrame:
    """
    Extract date features from a date column.
    
    Args:
        df: pandas DataFrame
        date_column: Column containing dates
        prefix: Prefix for new column names (default: date_column name)
    
    Returns:
        DataFrame with extracted date features
    """
    df = df.copy()
    
    if date_column not in df.columns:
        print(f"  Column '{date_column}' not found")
        return df
    
    # Ensure column is datetime
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    
    if prefix is None:
        prefix = date_column
    
    # Extract features
    df[f'{prefix}_year'] = df[date_column].dt.year
    df[f'{prefix}_month'] = df[date_column].dt.month
    df[f'{prefix}_day'] = df[date_column].dt.day
    df[f'{prefix}_day_of_week'] = df[date_column].dt.dayofweek
    df[f'{prefix}_day_name'] = df[date_column].dt.day_name()
    df[f'{prefix}_month_name'] = df[date_column].dt.month_name()
    df[f'{prefix}_quarter'] = df[date_column].dt.quarter
    df[f'{prefix}_week'] = df[date_column].dt.isocalendar().week
    df[f'{prefix}_is_weekend'] = df[date_column].dt.dayofweek >= 5
    
    print(f"  Extracted 9 date features from '{date_column}'")
    return df


def calculate_time_since(df: pd.DataFrame, date_column: str, reference_date: datetime = None, unit: str = 'days') -> pd.DataFrame:
    """
    Calculate time since a reference date.
    
    Args:
        df: pandas DataFrame
        date_column: Column containing dates
        reference_date: Reference date (default: today)
        unit: Unit for time difference ('days', 'hours', 'weeks')
    
    Returns:
        DataFrame with time since column
    """
    df = df.copy()
    
    if date_column not in df.columns:
        print(f"  Column '{date_column}' not found")
        return df
    
    # Ensure column is datetime
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    
    if reference_date is None:
        reference_date = pd.Timestamp.now()
    
    # Calculate difference
    diff = reference_date - df[date_column]
    
    if unit == 'days':
        df[f'{date_column}_days_since'] = diff.dt.days
    elif unit == 'hours':
        df[f'{date_column}_hours_since'] = diff.dt.total_seconds() / 3600
    elif unit == 'weeks':
        df[f'{date_column}_weeks_since'] = diff.dt.days / 7
    
    print(f"  Calculated time since reference date for '{date_column}'")
    return df


def create_date_ranges(df: pd.DataFrame, start_col: str, end_col: str, name: str = None) -> pd.DataFrame:
    """
    Create date range column from start and end dates.
    
    Args:
        df: pandas DataFrame
        start_col: Column containing start dates
        end_col: Column containing end dates
        name: Name for the new range column
    
    Returns:
        DataFrame with date range column
    """
    df = df.copy()
    
    if start_col not in df.columns or end_col not in df.columns:
        print(f"  Columns '{start_col}' or '{end_col}' not found")
        return df
    
    # Ensure columns are datetime
    if not pd.api.types.is_datetime64_any_dtype(df[start_col]):
        df[start_col] = pd.to_datetime(df[start_col], errors='coerce')
    if not pd.api.types.is_datetime64_any_dtype(df[end_col]):
        df[end_col] = pd.to_datetime(df[end_col], errors='coerce')
    
    if name is None:
        name = f'{start_col}_to_{end_col}'
    
    # Calculate duration
    df[f'{name}_days'] = (df[end_col] - df[start_col]).dt.days
    
    print(f"  Created date range from '{start_col}' to '{end_col}'")
    return df


def get_date_summary(df: pd.DataFrame, columns: list = None) -> dict:
    """
    Get summary statistics for date columns.
    
    Args:
        df: pandas DataFrame
        columns: List of columns to analyze (None for all datetime columns)
    
    Returns:
        Dictionary with date statistics
    """
    if columns is None:
        columns = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    summary = {}
    
    for col in columns:
        if col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                non_null = df[col].dropna()
                summary[col] = {
                    'total_count': len(df[col]),
                    'non_null_count': len(non_null),
                    'null_count': df[col].isna().sum(),
                    'min_date': non_null.min() if len(non_null) > 0 else None,
                    'max_date': non_null.max() if len(non_null) > 0 else None,
                    'date_range_days': (non_null.max() - non_null.min()).days if len(non_null) > 0 else 0
                }
    
    return summary
