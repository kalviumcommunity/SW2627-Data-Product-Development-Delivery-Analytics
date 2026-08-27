"""
Data Loading Module
Provides reusable functions for loading CSV and JSON datasets.
"""

import pandas as pd
from pathlib import Path


def load_csv(file_path: str, encoding: str = "utf-8", delimiter: str = ",") -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame.
    
    Args:
        file_path: Path to the CSV file
        encoding: File encoding (default: utf-8)
        delimiter: Column delimiter (default: ,)
    
    Returns:
        pandas DataFrame with the loaded data
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    df = pd.read_csv(file_path, encoding=encoding, delimiter=delimiter)
    print(f"Loaded {file_path}: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def load_json(file_path: str, encoding: str = "utf-8") -> pd.DataFrame:
    """
    Load a JSON file into a DataFrame.
    
    Args:
        file_path: Path to the JSON file
        encoding: File encoding (default: utf-8)
    
    Returns:
        pandas DataFrame with the loaded data
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    df = pd.read_json(file_path, encoding=encoding)
    print(f"Loaded {file_path}: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def get_file_info(file_path: str) -> dict:
    """
    Get basic information about a file.
    
    Args:
        file_path: Path to the file
    
    Returns:
        Dictionary with file information
    """
    path = Path(file_path)
    return {
        "exists": path.exists(),
        "size_mb": round(path.stat().st_size / (1024 * 1024), 2) if path.exists() else 0,
        "extension": path.suffix
    }
