"""
Data Cleaning Module
Provides reusable functions for cleaning and transforming datasets.
"""

import pandas as pd


def get_basic_profile(df: pd.DataFrame) -> dict:
    """
    Get basic profile of a DataFrame.
    
    Args:
        df: pandas DataFrame to profile
    
    Returns:
        Dictionary with profiling information
    """
    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "null_counts": df.isnull().sum().to_dict(),
        "null_percentage": (df.isnull().sum() / len(df) * 100).to_dict(),
        "memory_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
    }


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean column names by stripping whitespace and converting to lowercase.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        DataFrame with cleaned column names
    """
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def remove_duplicates(df: pd.DataFrame, subset: list = None) -> pd.DataFrame:
    """
    Remove duplicate rows from DataFrame.
    
    Args:
        df: pandas DataFrame
        subset: List of columns to check for duplicates
    
    Returns:
        DataFrame without duplicates
    """
    initial_count = len(df)
    df_clean = df.drop_duplicates(subset=subset, keep="first")
    removed_count = initial_count - len(df_clean)
    print(f"Removed {removed_count} duplicate rows")
    return df_clean
