"""
Data Export Module
Provides reusable functions for exporting processed data.
"""

import pandas as pd
from pathlib import Path


def export_csv(df: pd.DataFrame, file_path: str, index: bool = False) -> str:
    """
    Export DataFrame to CSV file.
    
    Args:
        df: pandas DataFrame to export
        file_path: Output file path
        index: Whether to write row indices (default: False)
    
    Returns:
        Path to the exported file
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(file_path, index=index)
    print(f"Exported to {file_path}: {df.shape[0]} rows")
    return file_path


def export_json(df: pd.DataFrame, file_path: str, orient: str = "records") -> str:
    """
    Export DataFrame to JSON file.
    
    Args:
        df: pandas DataFrame to export
        file_path: Output file path
        orient: JSON orientation (default: records)
    
    Returns:
        Path to the exported file
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_json(file_path, orient=orient, indent=2)
    print(f"Exported to {file_path}: {df.shape[0]} rows")
    return file_path
