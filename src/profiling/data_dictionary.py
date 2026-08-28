"""
Data Dictionary Module
Provides functions for loading and using data dictionaries.
"""

import pandas as pd
from pathlib import Path


def load_data_dictionary(file_path: str) -> pd.DataFrame:
    """
    Load a data dictionary from CSV file.
    
    Args:
        file_path: Path to the data dictionary CSV
    
    Returns:
        pandas DataFrame with data dictionary
    """
    return pd.read_csv(file_path)


def get_column_info(data_dict: pd.DataFrame, file_name: str, column_name: str) -> dict:
    """
    Get information about a specific column from the data dictionary.
    
    Args:
        data_dict: Data dictionary DataFrame
        file_name: Name of the source file
        column_name: Name of the column
    
    Returns:
        Dictionary with column information
    """
    mask = (data_dict["file"] == file_name) & (data_dict["column"] == column_name)
    result = data_dict[mask]
    
    if len(result) == 0:
        return None
    
    row = result.iloc[0]
    return {
        "file": row["file"],
        "column": row["column"],
        "type": row["type"],
        "meaning": row["meaning"],
        "project_use": row["project_use"]
    }


def get_file_columns(data_dict: pd.DataFrame, file_name: str) -> list:
    """
    Get all columns for a specific file from the data dictionary.
    
    Args:
        data_dict: Data dictionary DataFrame
        file_name: Name of the source file
    
    Returns:
        List of column information dictionaries
    """
    mask = data_dict["file"] == file_name
    result = data_dict[mask]
    
    columns = []
    for _, row in result.iterrows():
        columns.append({
            "column": row["column"],
            "type": row["type"],
            "meaning": row["meaning"],
            "project_use": row["project_use"]
        })
    
    return columns


def get_kpi_columns(data_dict: pd.DataFrame) -> list:
    """
    Get columns related to KPIs from the data dictionary.
    
    Args:
        data_dict: Data dictionary DataFrame
    
    Returns:
        List of column information dictionaries
    """
    kpi_keywords = ["utilization", "billable", "hours", "rate", "amount"]
    kpi_columns = []
    
    for _, row in data_dict.iterrows():
        if any(keyword in row["meaning"].lower() for keyword in kpi_keywords):
            kpi_columns.append({
                "file": row["file"],
                "column": row["column"],
                "type": row["type"],
                "meaning": row["meaning"],
                "project_use": row["project_use"]
            })
    
    return kpi_columns


def generate_data_dictionary_report(data_dict: pd.DataFrame) -> str:
    """
    Generate a formatted data dictionary report.
    
    Args:
        data_dict: Data dictionary DataFrame
    
    Returns:
        Formatted string report
    """
    report = []
    report.append("=" * 70)
    report.append("DATA DICTIONARY REPORT")
    report.append("=" * 70)
    
    # Group by file
    files = data_dict["file"].unique()
    
    for file_name in files:
        report.append(f"\n{'-' * 70}")
        report.append(f"FILE: {file_name}")
        report.append(f"{'-' * 70}")
        
        columns = get_file_columns(data_dict, file_name)
        for col in columns:
            report.append(f"\n  Column: {col['column']}")
            report.append(f"    Type: {col['type']}")
            report.append(f"    Meaning: {col['meaning']}")
            report.append(f"    Project Use: {col['project_use']}")
    
    return "\n".join(report)
