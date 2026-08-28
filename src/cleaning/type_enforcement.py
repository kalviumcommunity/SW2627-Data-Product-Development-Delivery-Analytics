"""
Type Enforcement Module
Provides functions for enforcing and standardizing data types.
"""

import pandas as pd
import numpy as np
from datetime import datetime


def enforce_date_type(df: pd.DataFrame, columns: list, date_format: str = None) -> pd.DataFrame:
    """
    Convert columns to datetime type.
    
    Args:
        df: pandas DataFrame
        columns: List of column names to convert
        date_format: Optional date format string
    
    Returns:
        DataFrame with converted date columns
    """
    df = df.copy()
    
    for col in columns:
        if col in df.columns:
            try:
                if date_format:
                    df[col] = pd.to_datetime(df[col], format=date_format)
                else:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                print(f"  Converted {col} to datetime")
            except Exception as e:
                print(f"  [WARN] Could not convert {col}: {str(e)}")
    
    return df


def enforce_numeric(df: pd.DataFrame, columns: list, handle_errors: str = "coerce") -> pd.DataFrame:
    """
    Convert columns to numeric type.
    
    Args:
        df: pandas DataFrame
        columns: List of column names to convert
        handle_errors: How to handle errors ('coerce', 'ignore', 'raise')
    
    Returns:
        DataFrame with converted numeric columns
    """
    df = df.copy()
    
    for col in columns:
        if col in df.columns:
            try:
                # Remove common non-numeric characters
                if df[col].dtype == 'object':
                    df[col] = df[col].astype(str).str.replace('[^0-9.-]', '', regex=True)
                
                df[col] = pd.to_numeric(df[col], errors=handle_errors)
                print(f"  Converted {col} to numeric")
            except Exception as e:
                print(f"  [WARN] Could not convert {col}: {str(e)}")
    
    return df


def enforce_boolean(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Convert columns to boolean type.
    
    Args:
        df: pandas DataFrame
        columns: List of column names to convert
    
    Returns:
        DataFrame with converted boolean columns
    """
    df = df.copy()
    
    bool_mapping = {
        'true': True, 'false': False,
        'yes': True, 'no': False,
        '1': True, '0': False,
        'y': True, 'n': False,
        't': True, 'f': False
    }
    
    for col in columns:
        if col in df.columns:
            try:
                df[col] = df[col].astype(str).str.lower().map(bool_mapping)
                print(f"  Converted {col} to boolean")
            except Exception as e:
                print(f"  [WARN] Could not convert {col}: {str(e)}")
    
    return df


def clean_currency(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Clean currency columns and convert to numeric.
    
    Args:
        df: pandas DataFrame
        columns: List of column names to clean
    
    Returns:
        DataFrame with cleaned currency columns
    """
    df = df.copy()
    
    for col in columns:
        if col in df.columns:
            try:
                # Remove currency symbols and commas
                df[col] = df[col].astype(str).str.replace('[$,€£¥]', '', regex=True)
                df[col] = pd.to_numeric(df[col], errors='coerce')
                print(f"  Cleaned currency column: {col}")
            except Exception as e:
                print(f"  [WARN] Could not clean {col}: {str(e)}")
    
    return df


def clean_percentage(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Clean percentage columns and convert to numeric.
    
    Args:
        df: pandas DataFrame
        columns: List of column names to clean
    
    Returns:
        DataFrame with cleaned percentage columns
    """
    df = df.copy()
    
    for col in columns:
        if col in df.columns:
            try:
                # Remove percentage signs
                df[col] = df[col].astype(str).str.replace('%', '', regex=True)
                df[col] = pd.to_numeric(df[col], errors='coerce')
                print(f"  Cleaned percentage column: {col}")
            except Exception as e:
                print(f"  [WARN] Could not clean {col}: {str(e)}")
    
    return df


def standardize_string(df: pd.DataFrame, columns: list, lowercase: bool = True, strip: bool = True) -> pd.DataFrame:
    """
    Standardize string columns.
    
    Args:
        df: pandas DataFrame
        columns: List of column names to standardize
        lowercase: Convert to lowercase
        strip: Strip whitespace
    
    Returns:
        DataFrame with standardized string columns
    """
    df = df.copy()
    
    for col in columns:
        if col in df.columns:
            try:
                if strip:
                    df[col] = df[col].astype(str).str.strip()
                if lowercase:
                    df[col] = df[col].astype(str).str.lower()
                print(f"  Standardized string column: {col}")
            except Exception as e:
                print(f"  [WARN] Could not standardize {col}: {str(e)}")
    
    return df


def get_type_summary(df: pd.DataFrame) -> dict:
    """
    Get a summary of data types in the DataFrame.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        Dictionary with type summary
    """
    type_counts = df.dtypes.value_counts().to_dict()
    
    return {
        "total_columns": len(df.columns),
        "type_counts": {str(k): int(v) for k, v in type_counts.items()},
        "columns_by_type": {
            str(dtype): list(df.select_dtypes(include=[dtype]).columns)
            for dtype in df.dtypes.unique()
        }
    }
