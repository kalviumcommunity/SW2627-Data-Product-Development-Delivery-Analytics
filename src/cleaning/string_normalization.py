"""
String Normalization Module
Provides functions for cleaning and normalizing text data.
"""

import pandas as pd
import re


def normalize_whitespace(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """
    Normalize whitespace in specified columns.
    
    Args:
        df: pandas DataFrame
        columns: List of columns to normalize (None for all string columns)
    
    Returns:
        DataFrame with normalized whitespace
    """
    df = df.copy()
    
    if columns is None:
        columns = df.select_dtypes(include=['object']).columns.tolist()
    
    for col in columns:
        if col in df.columns and df[col].dtype == 'object':
            # Strip leading/trailing whitespace
            df[col] = df[col].str.strip()
            # Replace multiple spaces with single space
            df[col] = df[col].str.replace(r'\s+', ' ', regex=True)
    
    print(f"  Normalized whitespace in {len(columns)} columns")
    return df


def normalize_case(df: pd.DataFrame, columns: list = None, case: str = 'lower') -> pd.DataFrame:
    """
    Normalize case in specified columns.
    
    Args:
        df: pandas DataFrame
        columns: List of columns to normalize (None for all string columns)
        case: Target case ('lower', 'upper', 'title')
    
    Returns:
        DataFrame with normalized case
    """
    df = df.copy()
    
    if columns is None:
        columns = df.select_dtypes(include=['object']).columns.tolist()
    
    for col in columns:
        if col in df.columns and df[col].dtype == 'object':
            if case == 'lower':
                df[col] = df[col].str.lower()
            elif case == 'upper':
                df[col] = df[col].str.upper()
            elif case == 'title':
                df[col] = df[col].str.title()
    
    print(f"  Normalized case to '{case}' in {len(columns)} columns")
    return df


def remove_special_characters(df: pd.DataFrame, columns: list = None, pattern: str = r'[^a-zA-Z0-9\s]') -> pd.DataFrame:
    """
    Remove special characters from specified columns.
    
    Args:
        df: pandas DataFrame
        columns: List of columns to clean (None for all string columns)
        pattern: Regex pattern for characters to remove
    
    Returns:
        DataFrame with special characters removed
    """
    df = df.copy()
    
    if columns is None:
        columns = df.select_dtypes(include=['object']).columns.tolist()
    
    for col in columns:
        if col in df.columns and df[col].dtype == 'object':
            df[col] = df[col].str.replace(pattern, '', regex=True)
    
    print(f"  Removed special characters from {len(columns)} columns")
    return df


def standardize_categorical_labels(df: pd.DataFrame, column: str, mapping_dict: dict) -> pd.DataFrame:
    """
    Standardize categorical labels using a mapping dictionary.
    
    Args:
        df: pandas DataFrame
        column: Column to standardize
        mapping_dict: Dictionary mapping old values to new values
    
    Returns:
        DataFrame with standardized labels
    """
    df = df.copy()
    
    if column in df.columns:
        # Apply mapping
        df[column] = df[column].map(mapping_dict).fillna(df[column])
        
        # Log changes
        old_values = set(mapping_dict.keys())
        new_values = set(mapping_dict.values())
        print(f"  Standardized '{column}': {len(old_values)} old values -> {len(new_values)} new values")
    
    return df


def clean_text_columns(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """
    Clean text columns by removing extra whitespace and special characters.
    
    Args:
        df: pandas DataFrame
        columns: List of columns to clean (None for all string columns)
    
    Returns:
        DataFrame with cleaned text
    """
    df = df.copy()
    
    if columns is None:
        columns = df.select_dtypes(include=['object']).columns.tolist()
    
    for col in columns:
        if col in df.columns and df[col].dtype == 'object':
            # Strip whitespace
            df[col] = df[col].str.strip()
            # Replace multiple spaces with single space
            df[col] = df[col].str.replace(r'\s+', ' ', regex=True)
            # Remove non-printable characters
            df[col] = df[col].apply(lambda x: ''.join(char for char in x if char.isprintable()) if isinstance(x, str) else x)
    
    print(f"  Cleaned {len(columns)} text columns")
    return df


def get_string_summary(df: pd.DataFrame, columns: list = None) -> dict:
    """
    Get summary statistics for string columns.
    
    Args:
        df: pandas DataFrame
        columns: List of columns to analyze (None for all string columns)
    
    Returns:
        Dictionary with string statistics
    """
    if columns is None:
        columns = df.select_dtypes(include=['object']).columns.tolist()
    
    summary = {}
    
    for col in columns:
        if col in df.columns and df[col].dtype == 'object':
            non_null = df[col].dropna()
            summary[col] = {
                'total_count': len(df[col]),
                'non_null_count': len(non_null),
                'null_count': df[col].isna().sum(),
                'unique_count': non_null.nunique(),
                'avg_length': non_null.str.len().mean() if len(non_null) > 0 else 0,
                'sample_values': non_null.head(3).tolist()
            }
    
    return summary
