"""
Missing Values Module
Provides functions for detecting and handling missing values.
"""

import pandas as pd
import numpy as np


def analyze_missing_values(df: pd.DataFrame) -> dict:
    """
    Analyze missing values in a DataFrame.
    
    Args:
        df: pandas DataFrame to analyze
    
    Returns:
        Dictionary with missing value analysis
    """
    missing = df.isnull()
    
    column_analysis = {}
    for col in df.columns:
        null_count = int(missing[col].sum())
        if null_count > 0:
            column_analysis[col] = {
                "null_count": null_count,
                "null_percentage": round(null_count / len(df) * 100, 2),
                "dtype": str(df[col].dtype),
                "sample_values": df[col].dropna().head(3).tolist()
            }
    
    return {
        "total_missing": int(missing.sum().sum()),
        "total_cells": df.shape[0] * df.shape[1],
        "missing_percentage": round(missing.sum().sum() / (df.shape[0] * df.shape[1]) * 100, 2),
        "columns_with_missing": list(missing.columns[missing.any()]),
        "columns_without_missing": list(missing.columns[~missing.any()]),
        "column_details": column_analysis
    }


def impute_numeric(df: pd.DataFrame, column: str, strategy: str = "median") -> pd.DataFrame:
    """
    Impute missing values in a numeric column.
    
    Args:
        df: pandas DataFrame
        column: Column name to impute
        strategy: Imputation strategy ('mean', 'median', 'zero', 'value')
    
    Returns:
        DataFrame with imputed values
    """
    df = df.copy()
    
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column '{column}' is not numeric")
    
    if strategy == "mean":
        fill_value = df[column].mean()
    elif strategy == "median":
        fill_value = df[column].median()
    elif strategy == "zero":
        fill_value = 0
    else:
        fill_value = float(strategy)
    
    df[column] = df[column].fillna(fill_value)
    return df


def impute_categorical(df: pd.DataFrame, column: str, strategy: str = "mode") -> pd.DataFrame:
    """
    Impute missing values in a categorical column.
    
    Args:
        df: pandas DataFrame
        column: Column name to impute
        strategy: Imputation strategy ('mode', 'value')
    
    Returns:
        DataFrame with imputed values
    """
    df = df.copy()
    
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    if strategy == "mode":
        fill_value = df[column].mode()[0] if not df[column].mode().empty else "Unknown"
    else:
        fill_value = strategy
    
    df[column] = df[column].fillna(fill_value)
    return df


def impute_by_group(df: pd.DataFrame, column: str, group_col: str, strategy: str = "median") -> pd.DataFrame:
    """
    Impute missing values using group-based statistics.
    
    Args:
        df: pandas DataFrame
        column: Column name to impute
        group_col: Column name to group by
        strategy: Imputation strategy ('mean', 'median', 'mode')
    
    Returns:
        DataFrame with imputed values
    """
    df = df.copy()
    
    if column not in df.columns or group_col not in df.columns:
        raise ValueError(f"Column '{column}' or '{group_col}' not found in DataFrame")
    
    if strategy in ["mean", "median"] and pd.api.types.is_numeric_dtype(df[column]):
        group_stats = df.groupby(group_col)[column].agg(strategy)
        df[column] = df.groupby(group_col)[column].transform(
            lambda x: x.fillna(group_stats[x.name] if x.name in group_stats else x.median())
        )
    elif strategy == "mode":
        group_mode = df.groupby(group_col)[column].agg(lambda x: x.mode()[0] if not x.mode().empty else "Unknown")
        df[column] = df.groupby(group_col)[column].transform(
            lambda x: x.fillna(group_mode[x.name] if x.name in group_mode else "Unknown")
        )
    
    return df


def flag_missing_records(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """
    Add a flag column indicating rows with missing values.
    
    Args:
        df: pandas DataFrame
        columns: List of columns to check (None for all columns)
    
    Returns:
        DataFrame with missing flag column
    """
    df = df.copy()
    
    if columns is None:
        columns = df.columns.tolist()
    
    df["has_missing"] = df[columns].isnull().any(axis=1).astype(int)
    
    return df


def compare_missing_before_after(df_before: pd.DataFrame, df_after: pd.DataFrame) -> dict:
    """
    Compare missing values before and after cleaning.
    
    Args:
        df_before: DataFrame before cleaning
        df_after: DataFrame after cleaning
    
    Returns:
        Dictionary with comparison results
    """
    before_missing = df_before.isnull().sum()
    after_missing = df_after.isnull().sum()
    
    comparison = {}
    for col in df_before.columns:
        if col in df_after.columns:
            before_count = int(before_missing[col])
            after_count = int(after_missing[col])
            comparison[col] = {
                "before": before_count,
                "after": after_count,
                "reduced": before_count - after_count
            }
    
    return comparison
