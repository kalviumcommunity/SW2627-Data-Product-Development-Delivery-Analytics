"""
Source Validation Module
Provides functions for validating datasets before ingestion.
"""

import pandas as pd
from pathlib import Path


def validate_schema(df: pd.DataFrame, expected_columns: list) -> dict:
    """
    Validate DataFrame has expected columns.
    
    Args:
        df: pandas DataFrame to validate
        expected_columns: List of expected column names
    
    Returns:
        Dictionary with validation results
    """
    actual_columns = set(df.columns)
    expected_set = set(expected_columns)
    
    missing = expected_set - actual_columns
    extra = actual_columns - expected_set
    
    return {
        "valid": len(missing) == 0,
        "missing_columns": list(missing),
        "extra_columns": list(extra),
        "actual_count": len(actual_columns),
        "expected_count": len(expected_columns)
    }


def validate_row_count(df: pd.DataFrame, min_rows: int = 1, max_rows: int = None) -> dict:
    """
    Validate DataFrame has expected row count.
    
    Args:
        df: pandas DataFrame to validate
        min_rows: Minimum expected rows
        max_rows: Maximum expected rows (None for no limit)
    
    Returns:
        Dictionary with validation results
    """
    row_count = len(df)
    valid = row_count >= min_rows
    
    if max_rows is not None:
        valid = valid and row_count <= max_rows
    
    return {
        "valid": valid,
        "actual_rows": row_count,
        "min_rows": min_rows,
        "max_rows": max_rows
    }


def validate_data_types(df: pd.DataFrame, expected_types: dict) -> dict:
    """
    Validate DataFrame has expected data types.
    
    Args:
        df: pandas DataFrame to validate
        expected_types: Dictionary mapping column names to expected dtype strings
    
    Returns:
        Dictionary with validation results
    """
    mismatches = []
    
    for col, expected_dtype in expected_types.items():
        if col in df.columns:
            actual_dtype = str(df[col].dtype)
            if actual_dtype != expected_dtype:
                mismatches.append({
                    "column": col,
                    "expected": expected_dtype,
                    "actual": actual_dtype
                })
    
    return {
        "valid": len(mismatches) == 0,
        "mismatches": mismatches
    }


def validate_no_empty_columns(df: pd.DataFrame) -> dict:
    """
    Validate that no columns are completely empty.
    
    Args:
        df: pandas DataFrame to validate
    
    Returns:
        Dictionary with validation results
    """
    empty_cols = [col for col in df.columns if df[col].isnull().all()]
    
    return {
        "valid": len(empty_cols) == 0,
        "empty_columns": empty_cols
    }


def run_full_validation(df: pd.DataFrame, schema: dict = None) -> dict:
    """
    Run all validation checks on a DataFrame.
    
    Args:
        df: pandas DataFrame to validate
        schema: Optional dictionary with 'columns', 'min_rows', 'dtypes'
    
    Returns:
        Dictionary with all validation results
    """
    results = {
        "shape": df.shape,
        "row_count": validate_row_count(df),
        "empty_columns": validate_no_empty_columns(df)
    }
    
    if schema:
        if "columns" in schema:
            results["schema"] = validate_schema(df, schema["columns"])
        if "dtypes" in schema:
            results["dtypes"] = validate_data_types(df, schema["dtypes"])
    
    results["overall_valid"] = all([
        results["row_count"]["valid"],
        results["empty_columns"]["valid"],
        results.get("schema", {}).get("valid", True),
        results.get("dtypes", {}).get("valid", True)
    ])
    
    return results
