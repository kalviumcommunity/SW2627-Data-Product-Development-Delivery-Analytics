"""
Data Consistency & Validation Rules Module
Provides functions for validating data consistency and business rules.
"""

import pandas as pd


def check_null_thresholds(df: pd.DataFrame, column_thresholds: dict = None) -> dict:
    """
    Check if columns exceed null percentage thresholds.
    
    Args:
        df: pandas DataFrame
        column_thresholds: Dictionary mapping column names to threshold percentages
    
    Returns:
        Dictionary with validation results
    """
    if column_thresholds is None:
        column_thresholds = {col: 50.0 for col in df.columns}
    
    results = {}
    
    for col, threshold in column_thresholds.items():
        if col in df.columns:
            null_pct = (df[col].isna().sum() / len(df)) * 100
            results[col] = {
                'null_percentage': round(null_pct, 2),
                'threshold': threshold,
                'exceeds_threshold': null_pct > threshold,
                'status': 'FAIL' if null_pct > threshold else 'PASS'
            }
    
    return results


def check_value_ranges(df: pd.DataFrame, column_ranges: dict) -> dict:
    """
    Check if columns contain values within expected ranges.
    
    Args:
        df: pandas DataFrame
        column_ranges: Dictionary mapping column names to (min, max) tuples
    
    Returns:
        Dictionary with validation results
    """
    results = {}
    
    for col, (min_val, max_val) in column_ranges.items():
        if col in df.columns:
            # Try to convert to numeric
            try:
                numeric_col = pd.to_numeric(df[col], errors='coerce')
                below_min = (numeric_col < min_val).sum()
                above_max = (numeric_col > max_val).sum()
                out_of_range = below_min + above_max
                
                results[col] = {
                    'min_value': min_val,
                    'max_value': max_val,
                    'below_min': int(below_min),
                    'above_max': int(above_max),
                    'out_of_range_count': int(out_of_range),
                    'out_of_range_pct': round(out_of_range / len(df) * 100, 2),
                    'status': 'PASS' if out_of_range == 0 else 'FAIL'
                }
            except Exception as e:
                results[col] = {
                    'error': str(e),
                    'status': 'ERROR'
                }
    
    return results


def check_referential_integrity(df_child: pd.DataFrame, df_parent: pd.DataFrame, fk_column: str, pk_column: str = None) -> dict:
    """
    Check referential integrity between child and parent DataFrames.
    
    Args:
        df_child: Child DataFrame containing foreign key
        df_parent: Parent DataFrame containing primary key
        fk_column: Foreign key column name in child
        pk_column: Primary key column name in parent (default: same as fk_column)
    
    Returns:
        Dictionary with validation results
    """
    if pk_column is None:
        pk_column = fk_column
    
    if fk_column not in df_child.columns:
        return {'error': f'Column {fk_column} not found in child DataFrame', 'status': 'ERROR'}
    
    if pk_column not in df_parent.columns:
        return {'error': f'Column {pk_column} not found in parent DataFrame', 'status': 'ERROR'}
    
    child_keys = set(df_child[fk_column].dropna())
    parent_keys = set(df_parent[pk_column].dropna())
    
    orphans = child_keys - parent_keys
    
    return {
        'child_key_count': len(child_keys),
        'parent_key_count': len(parent_keys),
        'orphan_count': len(orphans),
        'orphan_pct': round(len(orphans) / len(child_keys) * 100, 2) if len(child_keys) > 0 else 0,
        'orphan_samples': list(orphans)[:5],
        'status': 'PASS' if len(orphans) == 0 else 'FAIL'
    }


def check_business_rules(df: pd.DataFrame, rules_dict: dict) -> dict:
    """
    Check business rules on DataFrame.
    
    Args:
        df: pandas DataFrame
        rules_dict: Dictionary mapping rule names to lambda functions
    
    Returns:
        Dictionary with validation results
    """
    results = {}
    
    for rule_name, rule_func in rules_dict.items():
        try:
            violations = (~rule_func(df)).sum()
            results[rule_name] = {
                'violation_count': int(violations),
                'violation_pct': round(violations / len(df) * 100, 2),
                'status': 'PASS' if violations == 0 else 'FAIL'
            }
        except Exception as e:
            results[rule_name] = {
                'error': str(e),
                'status': 'ERROR'
            }
    
    return results


def validate_timesheet_hours(df: pd.DataFrame) -> dict:
    """
    Validate timesheet hours for consistency.
    
    Args:
        df: pandas DataFrame with timesheet data
    
    Returns:
        Dictionary with validation results
    """
    results = {}
    
    if 'hours_worked' in df.columns:
        # Check hours are positive
        negative_hours = (df['hours_worked'] < 0).sum()
        results['negative_hours'] = {
            'count': int(negative_hours),
            'status': 'PASS' if negative_hours == 0 else 'FAIL'
        }
        
        # Check hours are reasonable (0-24)
        unreasonable_hours = ((df['hours_worked'] < 0) | (df['hours_worked'] > 24)).sum()
        results['unreasonable_hours'] = {
            'count': int(unreasonable_hours),
            'status': 'PASS' if unreasonable_hours == 0 else 'FAIL'
        }
    
    if 'billable_hours' in df.columns:
        # Check billable hours are non-negative
        negative_billable = (df['billable_hours'] < 0).sum()
        results['negative_billable_hours'] = {
            'count': int(negative_billable),
            'status': 'PASS' if negative_billable == 0 else 'FAIL'
        }
    
    return results


def validate_allocation_percentages(df: pd.DataFrame) -> dict:
    """
    Validate allocation percentages for consistency.
    
    Args:
        df: pandas DataFrame with allocation data
    
    Returns:
        Dictionary with validation results
    """
    results = {}
    
    if 'allocation_percentage' in df.columns:
        # Check percentages are between 0 and 100
        invalid_pct = ((df['allocation_percentage'] < 0) | (df['allocation_percentage'] > 100)).sum()
        results['invalid_percentages'] = {
            'count': int(invalid_pct),
            'status': 'PASS' if invalid_pct == 0 else 'FAIL'
        }
    
    if 'expected_utilization' in df.columns:
        # Check utilization is between 0 and 100
        invalid_util = ((df['expected_utilization'] < 0) | (df['expected_utilization'] > 100)).sum()
        results['invalid_utilization'] = {
            'count': int(invalid_util),
            'status': 'PASS' if invalid_util == 0 else 'FAIL'
        }
    
    return results


def validate_billing_rates(df: pd.DataFrame) -> dict:
    """
    Validate billing rates for consistency.
    
    Args:
        df: pandas DataFrame with billing data
    
    Returns:
        Dictionary with validation results
    """
    results = {}
    
    if 'billing_rate' in df.columns:
        # Check rates are positive
        negative_rates = (df['billing_rate'] < 0).sum()
        results['negative_rates'] = {
            'count': int(negative_rates),
            'status': 'PASS' if negative_rates == 0 else 'FAIL'
        }
    
    if 'billed_amount' in df.columns:
        # Check amounts are non-negative
        negative_amounts = (df['billed_amount'] < 0).sum()
        results['negative_amounts'] = {
            'count': int(negative_amounts),
            'status': 'PASS' if negative_amounts == 0 else 'FAIL'
        }
    
    return results


def run_all_validations(df: pd.DataFrame, dataset_name: str) -> dict:
    """
    Run all validation checks on a dataset.
    
    Args:
        df: pandas DataFrame
        dataset_name: Name of the dataset
    
    Returns:
        Dictionary with all validation results
    """
    print(f"\n{'-' * 60}")
    print(f"Validating: {dataset_name}")
    print(f"{'-' * 60}")
    
    results = {
        'dataset': dataset_name,
        'total_rows': len(df),
        'validations': {}
    }
    
    # Run null threshold check
    null_results = check_null_thresholds(df)
    results['validations']['null_thresholds'] = null_results
    
    # Run business rules based on dataset
    if dataset_name == 'Timesheets':
        results['validations']['timesheet_hours'] = validate_timesheet_hours(df)
    elif dataset_name == 'Allocations':
        results['validations']['allocation_percentages'] = validate_allocation_percentages(df)
    elif dataset_name == 'Billing':
        results['validations']['billing_rates'] = validate_billing_rates(df)
    
    # Print summary
    total_checks = 0
    passed_checks = 0
    failed_checks = 0
    
    for validation_type, validation_results in results['validations'].items():
        if isinstance(validation_results, dict):
            for check_name, check_result in validation_results.items():
                if isinstance(check_result, dict) and 'status' in check_result:
                    total_checks += 1
                    if check_result['status'] == 'PASS':
                        passed_checks += 1
                    else:
                        failed_checks += 1
    
    print(f"  Total checks: {total_checks}")
    print(f"  Passed: {passed_checks}")
    print(f"  Failed: {failed_checks}")
    print(f"  Status: {'PASS' if failed_checks == 0 else 'FAIL'}")
    
    return results
