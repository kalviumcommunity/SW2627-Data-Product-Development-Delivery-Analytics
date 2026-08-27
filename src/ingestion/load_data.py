"""
Data Loading Module
Provides reusable functions for loading CSV and JSON datasets.
"""

import pandas as pd
from pathlib import Path


def detect_encoding(file_path: str) -> str:
    """
    Detect the encoding of a file.
    
    Args:
        file_path: Path to the file
    
    Returns:
        Detected encoding string
    """
    encodings = ["utf-8", "latin-1", "cp1252", "iso-8859-1"]
    
    for encoding in encodings:
        try:
            with open(file_path, encoding=encoding) as f:
                f.read(1000)
            return encoding
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    return "utf-8"


def load_csv(file_path: str, encoding: str = None, delimiter: str = ",") -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame with automatic encoding detection.
    
    Args:
        file_path: Path to the CSV file
        encoding: File encoding (None for auto-detect)
        delimiter: Column delimiter (default: ,)
    
    Returns:
        pandas DataFrame with the loaded data
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if encoding is None:
        encoding = detect_encoding(file_path)
        print(f"Detected encoding: {encoding}")
    
    df = pd.read_csv(file_path, encoding=encoding, delimiter=delimiter)
    print(f"Loaded {file_path}: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def load_json(file_path: str, encoding: str = None) -> pd.DataFrame:
    """
    Load a JSON file into a DataFrame.
    
    Args:
        file_path: Path to the JSON file
        encoding: File encoding (None for auto-detect)
    
    Returns:
        pandas DataFrame with the loaded data
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if encoding is None:
        encoding = detect_encoding(file_path)
        print(f"Detected encoding: {encoding}")
    
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


def generate_ingestion_report(df: pd.DataFrame, source_name: str) -> dict:
    """
    Generate an ingestion report for a loaded DataFrame.
    
    Args:
        df: pandas DataFrame
        source_name: Name of the data source
    
    Returns:
        Dictionary with ingestion report
    """
    return {
        "source": source_name,
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "null_counts": df.isnull().sum().to_dict(),
        "memory_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
    }
