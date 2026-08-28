"""
Deduplication Module
Provides functions for detecting and removing duplicate records.
"""

import pandas as pd


def find_exact_duplicates(df: pd.DataFrame, subset: list = None) -> pd.DataFrame:
    """
    Find exact duplicate rows in DataFrame.
    
    Args:
        df: pandas DataFrame
        subset: List of columns to check for duplicates
    
    Returns:
        DataFrame containing only duplicate rows
    """
    duplicates = df.duplicated(subset=subset, keep=False)
    return df[duplicates]


def find_first_duplicates(df: pd.DataFrame, subset: list = None) -> pd.DataFrame:
    """
    Find first occurrence of duplicate rows.
    
    Args:
        df: pandas DataFrame
        subset: List of columns to check for duplicates
    
    Returns:
        DataFrame containing first occurrence of each duplicate group
    """
    return df[df.duplicated(subset=subset, keep='first')]


def remove_duplicates(df: pd.DataFrame, subset: list = None, keep: str = 'first') -> pd.DataFrame:
    """
    Remove duplicate rows from DataFrame.
    
    Args:
        df: pandas DataFrame
        subset: List of columns to check for duplicates
        keep: Which duplicate to keep ('first', 'last', False)
    
    Returns:
        DataFrame without duplicates
    """
    initial_count = len(df)
    df_clean = df.drop_duplicates(subset=subset, keep=keep)
    removed_count = initial_count - len(df_clean)
    
    print(f"  Removed {removed_count} duplicate rows ({removed_count/initial_count*100:.2f}%)")
    print(f"  Remaining rows: {len(df_clean)}")
    
    return df_clean


def log_duplicates_removed(df_before: pd.DataFrame, df_after: pd.DataFrame, subset: list = None) -> dict:
    """
    Log details about removed duplicates.
    
    Args:
        df_before: DataFrame before deduplication
        df_after: DataFrame after deduplication
        subset: List of columns used for deduplication
    
    Returns:
        Dictionary with deduplication log
    """
    duplicates = df_before.duplicated(subset=subset, keep=False)
    
    return {
        "total_rows_before": len(df_before),
        "total_rows_after": len(df_after),
        "rows_removed": len(df_before) - len(df_after),
        "duplicate_groups": int(df_before.duplicated(subset=subset, keep='first').sum()),
        "columns_used": subset or list(df_before.columns),
        "reduction_percentage": round((len(df_before) - len(df_after)) / len(df_before) * 100, 2)
    }


def analyze_duplicates(df: pd.DataFrame, subset: list = None) -> dict:
    """
    Analyze duplicate patterns in DataFrame.
    
    Args:
        df: pandas DataFrame
        subset: List of columns to analyze
    
    Returns:
        Dictionary with duplicate analysis
    """
    duplicates = df.duplicated(subset=subset, keep=False)
    
    if not duplicates.any():
        return {
            "has_duplicates": False,
            "duplicate_count": 0,
            "duplicate_percentage": 0
        }
    
    dup_df = df[duplicates]
    
    return {
        "has_duplicates": True,
        "duplicate_count": int(duplicates.sum()),
        "duplicate_percentage": round(duplicates.sum() / len(df) * 100, 2),
        "unique_duplicate_groups": int(df.duplicated(subset=subset, keep='first').sum())
    }
