"""
Dataset Profiling Module
Provides functions for profiling datasets and assessing data quality.
"""

import pandas as pd
import numpy as np


def profile_dataframe(df: pd.DataFrame, name: str = "DataFrame") -> dict:
    """
    Generate a comprehensive profile of a DataFrame.
    
    Args:
        df: pandas DataFrame to profile
        name: Name of the dataset for reporting
    
    Returns:
        Dictionary with profiling information
    """
    profile = {
        "name": name,
        "shape": df.shape,
        "rows": df.shape[0],
        "columns": df.shape[1],
        "memory_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
        "column_info": []
    }
    
    for col in df.columns:
        col_info = {
            "name": col,
            "dtype": str(df[col].dtype),
            "null_count": int(df[col].isnull().sum()),
            "null_percentage": round(df[col].isnull().sum() / len(df) * 100, 2),
            "unique_count": int(df[col].nunique()),
            "unique_percentage": round(df[col].nunique() / len(df) * 100, 2)
        }
        
        # Add numeric stats if applicable
        if pd.api.types.is_numeric_dtype(df[col]):
            col_info["min"] = float(df[col].min()) if not df[col].isnull().all() else None
            col_info["max"] = float(df[col].max()) if not df[col].isnull().all() else None
            col_info["mean"] = round(float(df[col].mean()), 2) if not df[col].isnull().all() else None
            col_info["median"] = float(df[col].median()) if not df[col].isnull().all() else None
            col_info["std"] = round(float(df[col].std()), 2) if not df[col].isnull().all() else None
        
        # Add categorical stats if applicable
        if pd.api.types.is_object_dtype(df[col]):
            value_counts = df[col].value_counts().head(5)
            col_info["top_values"] = value_counts.to_dict()
        
        profile["column_info"].append(col_info)
    
    return profile


def detect_missing_patterns(df: pd.DataFrame) -> dict:
    """
    Detect patterns in missing values.
    
    Args:
        df: pandas DataFrame to analyze
    
    Returns:
        Dictionary with missing value patterns
    """
    missing = df.isnull()
    
    return {
        "total_missing": int(missing.sum().sum()),
        "total_cells": df.shape[0] * df.shape[1],
        "missing_percentage": round(missing.sum().sum() / (df.shape[0] * df.shape[1]) * 100, 2),
        "columns_with_missing": list(missing.columns[missing.any()]),
        "rows_with_missing": int(missing.any(axis=1).sum()),
        "complete_rows": int((~missing.any(axis=1)).sum())
    }


def detect_duplicates(df: pd.DataFrame, subset: list = None) -> dict:
    """
    Detect duplicate records in DataFrame.
    
    Args:
        df: pandas DataFrame to analyze
        subset: List of columns to check for duplicates
    
    Returns:
        Dictionary with duplicate information
    """
    duplicates = df.duplicated(subset=subset, keep=False)
    
    return {
        "total_duplicates": int(duplicates.sum()),
        "duplicate_percentage": round(duplicates.sum() / len(df) * 100, 2),
        "unique_rows": int((~duplicates).sum()),
        "duplicate_groups": int(df.duplicated(subset=subset, keep='first').sum())
    }


def profile_categorical_columns(df: pd.DataFrame) -> dict:
    """
    Profile all categorical columns in DataFrame.
    
    Args:
        df: pandas DataFrame to analyze
    
    Returns:
        Dictionary with categorical column profiles
    """
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    profiles = {}
    
    for col in categorical_cols:
        value_counts = df[col].value_counts()
        profiles[col] = {
            "unique_values": int(df[col].nunique()),
            "top_value": value_counts.index[0] if len(value_counts) > 0 else None,
            "top_value_count": int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
            "top_value_percentage": round(value_counts.iloc[0] / len(df) * 100, 2) if len(value_counts) > 0 else 0,
            "null_count": int(df[col].isnull().sum())
        }
    
    return profiles


def profile_numeric_columns(df: pd.DataFrame) -> dict:
    """
    Profile all numeric columns in DataFrame.
    
    Args:
        df: pandas DataFrame to analyze
    
    Returns:
        Dictionary with numeric column profiles
    """
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    profiles = {}
    
    for col in numeric_cols:
        if df[col].isnull().all():
            profiles[col] = {"status": "all_null"}
            continue
            
        profiles[col] = {
            "min": float(df[col].min()),
            "max": float(df[col].max()),
            "mean": round(float(df[col].mean()), 2),
            "median": float(df[col].median()),
            "std": round(float(df[col].std()), 2),
            "q25": float(df[col].quantile(0.25)),
            "q75": float(df[col].quantile(0.75)),
            "null_count": int(df[col].isnull().sum()),
            "negative_count": int((df[col] < 0).sum()),
            "zero_count": int((df[col] == 0).sum())
        }
    
    return profiles


def generate_full_report(df: pd.DataFrame, name: str = "DataFrame") -> dict:
    """
    Generate a complete profiling report for a DataFrame.
    
    Args:
        df: pandas DataFrame to profile
        name: Name of the dataset
    
    Returns:
        Dictionary with complete profiling report
    """
    return {
        "basic_profile": profile_dataframe(df, name),
        "missing_patterns": detect_missing_patterns(df),
        "duplicates": detect_duplicates(df),
        "categorical_profiles": profile_categorical_columns(df),
        "numeric_profiles": profile_numeric_columns(df)
    }
