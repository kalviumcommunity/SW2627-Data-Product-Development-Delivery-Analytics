"""
Multi-Source Merging & Join Validation Module
Provides functions for merging datasets with validation.
"""

import pandas as pd


def validate_keys_before_merge(df1: pd.DataFrame, df2: pd.DataFrame, key_column: str) -> dict:
    """
    Validate keys before merging DataFrames.
    
    Args:
        df1: First DataFrame
        df2: Second DataFrame
        key_column: Key column to validate
    
    Returns:
        Dictionary with validation results
    """
    results = {}
    
    if key_column not in df1.columns:
        results['error'] = f'Column {key_column} not found in first DataFrame'
        return results
    
    if key_column not in df2.columns:
        results['error'] = f'Column {key_column} not found in second DataFrame'
        return results
    
    # Get unique keys
    keys1 = set(df1[key_column].dropna())
    keys2 = set(df2[key_column].dropna())
    
    # Check for overlaps
    common_keys = keys1 & keys2
    only_in_df1 = keys1 - keys2
    only_in_df2 = keys2 - keys1
    
    results = {
        'key_column': key_column,
        'df1_key_count': len(keys1),
        'df2_key_count': len(keys2),
        'common_keys': len(common_keys),
        'only_in_df1': len(only_in_df1),
        'only_in_df2': len(only_in_df2),
        'overlap_pct': round(len(common_keys) / len(keys1 | keys2) * 100, 2) if len(keys1 | keys2) > 0 else 0
    }
    
    return results


def merge_with_validation(df1: pd.DataFrame, df2: pd.DataFrame, on: str, how: str = 'left') -> pd.DataFrame:
    """
    Merge DataFrames with validation.
    
    Args:
        df1: First DataFrame
        df2: Second DataFrame
        on: Key column(s) to merge on
        how: Type of merge ('left', 'right', 'inner', 'outer')
    
    Returns:
        Merged DataFrame
    """
    # Validate keys
    validation = validate_keys_before_merge(df1, df2, on)
    
    if 'error' in validation:
        print(f"  [ERROR] {validation['error']}")
        return pd.DataFrame()
    
    # Perform merge
    initial_rows = len(df1)
    df_merged = pd.merge(df1, df2, on=on, how=how)
    final_rows = len(df_merged)
    
    # Log results
    print(f"  Merged {on}: {initial_rows} rows -> {final_rows} rows")
    print(f"  Overlap: {validation['overlap_pct']}%")
    
    return df_merged


def check_row_count_integrity(df_merged: pd.DataFrame, df_original: pd.DataFrame, merge_type: str) -> dict:
    """
    Check row count integrity after merge.
    
    Args:
        df_merged: Merged DataFrame
        df_original: Original DataFrame before merge
        merge_type: Type of merge ('left', 'right', 'inner', 'outer')
    
    Returns:
        Dictionary with integrity check results
    """
    merged_rows = len(df_merged)
    original_rows = len(df_original)
    
    if merge_type == 'left':
        # Left merge should have at least as many rows as original
        has_duplicates = merged_rows > original_rows
    elif merge_type == 'inner':
        # Inner merge should have fewer or equal rows
        has_duplicates = merged_rows > original_rows
    else:
        # Other merges
        has_duplicates = merged_rows > original_rows * 1.5
    
    return {
        'original_rows': original_rows,
        'merged_rows': merged_rows,
        'row_change': merged_rows - original_rows,
        'has_duplicates': has_duplicates,
        'status': 'PASS' if not has_duplicates else 'FAIL'
    }


def identify_unmatched_records(df1: pd.DataFrame, df2: pd.DataFrame, key_column: str) -> dict:
    """
    Identify records that don't match between DataFrames.
    
    Args:
        df1: First DataFrame
        df2: Second DataFrame
        key_column: Key column to compare
    
    Returns:
        Dictionary with unmatched records information
    """
    if key_column not in df1.columns or key_column not in df2.columns:
        return {'error': f'Key column {key_column} not found in both DataFrames'}
    
    keys1 = set(df1[key_column].dropna())
    keys2 = set(df2[key_column].dropna())
    
    only_in_df1 = keys1 - keys2
    only_in_df2 = keys2 - keys1
    
    return {
        'only_in_df1_count': len(only_in_df1),
        'only_in_df2_count': len(only_in_df2),
        'only_in_df1_samples': list(only_in_df1)[:5],
        'only_in_df2_samples': list(only_in_df2)[:5]
    }


def create_analytics_dataset(timesheets: pd.DataFrame, allocations: pd.DataFrame, billing: pd.DataFrame, employees: pd.DataFrame) -> pd.DataFrame:
    """
    Create unified analytics dataset from multiple sources.
    
    Args:
        timesheets: Timesheets DataFrame
        allocations: Allocations DataFrame
        billing: Billing DataFrame
        employees: Employees DataFrame
    
    Returns:
        Merged analytics DataFrame
    """
    print("\n" + "=" * 60)
    print("CREATING ANALYTICS DATASET")
    print("=" * 60)
    
    # Start with timesheets
    df = timesheets.copy()
    print(f"\nStarting with timesheets: {len(df)} rows")
    
    # Merge with employees
    if 'employee_id' in df.columns and 'employee_id' in employees.columns:
        df = pd.merge(df, employees, on='employee_id', how='left')
        print(f"After merging with employees: {len(df)} rows")
    
    # Merge with allocations
    if 'employee_id' in df.columns and 'employee_id' in allocations.columns:
        # Aggregate allocations by employee
        alloc_agg = allocations.groupby('employee_id').agg({
            'allocated_hours': 'sum',
            'allocation_percentage': 'mean'
        }).reset_index()
        
        df = pd.merge(df, alloc_agg, on='employee_id', how='left')
        print(f"After merging with allocations: {len(df)} rows")
    
    # Merge with billing
    if 'employee_id' in df.columns and 'employee_id' in billing.columns:
        # Aggregate billing by employee
        billing_agg = billing.groupby('employee_id').agg({
            'billed_amount': 'sum',
            'billable_hours': 'sum'
        }).reset_index()
        
        df = pd.merge(df, billing_agg, on='employee_id', how='left')
        print(f"After merging with billing: {len(df)} rows")
    
    print(f"\nFinal analytics dataset: {len(df)} rows, {len(df.columns)} columns")
    
    return df


def get_merge_summary(df: pd.DataFrame) -> dict:
    """
    Get summary of merged DataFrame.
    
    Args:
        df: Merged DataFrame
    
    Returns:
        Dictionary with merge summary
    """
    return {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'columns': list(df.columns),
        'dtypes': df.dtypes.to_dict(),
        'null_counts': df.isna().sum().to_dict()
    }
