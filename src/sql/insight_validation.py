"""
SQL-Based Insight Validation Module
Provides functions for validating business insights using SQL queries.
"""

import pandas as pd
import sqlite3
from typing import Dict, List, Optional


def validate_utilization_insight(conn: sqlite3.Connection, threshold: float = 65) -> Dict:
    """
    Validate utilization insight against threshold.
    
    Args:
        conn: SQLite connection
        threshold: Utilization threshold to validate
    
    Returns:
        Dictionary with validation results
    """
    query = """
    SELECT 
        COUNT(DISTINCT employee_id) as total_employees,
        ROUND(AVG(billable_hours * 100.0 / hours_logged), 2) as avg_utilization,
        SUM(CASE WHEN billable_hours * 100.0 / hours_logged > ? THEN 1 ELSE 0 END) as above_threshold,
        SUM(CASE WHEN billable_hours * 100.0 / hours_logged <= ? THEN 1 ELSE 0 END) as below_threshold
    FROM timesheets
    WHERE hours_logged > 0
    """
    df = pd.read_sql_query(query, conn, params=(threshold, threshold))
    
    return {
        'insight': f'Utilization threshold validation at {threshold}%',
        'total_employees': int(df['total_employees'].iloc[0]),
        'avg_utilization': float(df['avg_utilization'].iloc[0]),
        'above_threshold': int(df['above_threshold'].iloc[0]),
        'below_threshold': int(df['below_threshold'].iloc[0]),
        'validation_passed': df['avg_utilization'].iloc[0] >= threshold
    }


def validate_revenue_insight(conn: sqlite3.Connection, min_revenue: float = 100000) -> Dict:
    """
    Validate revenue insight against minimum threshold.
    
    Args:
        conn: SQLite connection
        min_revenue: Minimum revenue threshold
    
    Returns:
        Dictionary with validation results
    """
    query = """
    SELECT 
        employee_id,
        SUM(billed_amount) as total_revenue
    FROM billing
    GROUP BY employee_id
    HAVING SUM(billed_amount) > ?
    ORDER BY total_revenue DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_revenue,))
    
    return {
        'insight': f'Revenue validation above {min_revenue:,.0f}',
        'employees_above_threshold': len(df),
        'total_revenue': round(df['total_revenue'].sum(), 2),
        'avg_revenue': round(df['total_revenue'].mean(), 2),
        'validation_passed': len(df) > 0
    }


def validate_department_performance(conn: sqlite3.Connection) -> Dict:
    """
    Validate department performance consistency.
    
    Args:
        conn: SQLite connection
    
    Returns:
        Dictionary with validation results
    """
    query = """
    SELECT 
        e.department,
        COUNT(DISTINCT t.employee_id) as employee_count,
        ROUND(AVG(t.billable_hours * 100.0 / t.hours_logged), 2) as avg_utilization,
        ROUND(SUM(t.billable_hours * 100.0 / t.hours_logged) / COUNT(DISTINCT t.employee_id), 2) as utilization_stddev
    FROM timesheets t
    LEFT JOIN employees e ON t.employee_id = e.employee_id
    WHERE t.hours_logged > 0
    GROUP BY e.department
    HAVING COUNT(DISTINCT t.employee_id) > 5
    """
    df = pd.read_sql_query(query, conn)
    
    return {
        'insight': 'Department performance consistency validation',
        'departments_analyzed': len(df),
        'avg_utilization': round(df['avg_utilization'].mean(), 2),
        'min_utilization': round(df['avg_utilization'].min(), 2),
        'max_utilization': round(df['avg_utilization'].max(), 2),
        'validation_passed': df['avg_utilization'].std() < 10
    }


def validate_billing_accuracy(conn: sqlite3.Connection) -> Dict:
    """
    Validate billing accuracy between hours and amounts.
    
    Args:
        conn: SQLite connection
    
    Returns:
        Dictionary with validation results
    """
    query = """
    SELECT 
        billing_id,
        billable_hours,
        billed_amount,
        billing_rate,
        ROUND(billed_amount / billable_hours, 2) as calculated_rate
    FROM billing
    WHERE billable_hours > 0
    """
    df = pd.read_sql_query(query, conn)
    
    if len(df) == 0:
        return {'insight': 'Billing accuracy validation', 'validation_passed': False}
    
    rate_diff = (df['calculated_rate'] - df['billing_rate']).abs()
    
    return {
        'insight': 'Billing accuracy validation',
        'total_records': len(df),
        'avg_rate_difference': round(rate_diff.mean(), 2),
        'max_rate_difference': round(rate_diff.max(), 2),
        'accuracy_rate': round((rate_diff < 1).sum() / len(df) * 100, 2),
        'validation_passed': rate_diff.mean() < 5
    }


def validate_allocation_efficiency(conn: sqlite3.Connection) -> Dict:
    """
    Validate allocation efficiency.
    
    Args:
        conn: SQLite connection
    
    Returns:
        Dictionary with validation results
    """
    query = """
    SELECT 
        employee_id,
        SUM(allocated_hours) as total_allocated,
        SUM(planned_billable_hours) as total_planned,
        ROUND(SUM(planned_billable_hours) * 100.0 / SUM(allocated_hours), 2) as efficiency
    FROM allocations
    GROUP BY employee_id
    HAVING SUM(allocated_hours) > 0
    """
    df = pd.read_sql_query(query, conn)
    
    return {
        'insight': 'Allocation efficiency validation',
        'employees_analyzed': len(df),
        'avg_efficiency': round(df['efficiency'].mean(), 2),
        'min_efficiency': round(df['efficiency'].min(), 2),
        'max_efficiency': round(df['efficiency'].max(), 2),
        'validation_passed': df['efficiency'].mean() > 50
    }


def run_all_validations(conn: sqlite3.Connection) -> Dict:
    """
    Run all insight validations.
    
    Args:
        conn: SQLite connection
    
    Returns:
        Dictionary with all validation results
    """
    return {
        'utilization': validate_utilization_insight(conn),
        'revenue': validate_revenue_insight(conn),
        'department': validate_department_performance(conn),
        'billing': validate_billing_accuracy(conn),
        'allocation': validate_allocation_efficiency(conn)
    }


def get_validation_summary(results: Dict) -> Dict:
    """
    Get summary of all validations.
    
    Args:
        results: Validation results dictionary
    
    Returns:
        Summary dictionary
    """
    passed = sum(1 for v in results.values() if v.get('validation_passed', False))
    total = len(results)
    
    return {
        'total_validations': total,
        'passed': passed,
        'failed': total - passed,
        'pass_rate': round(passed / total * 100, 2) if total > 0 else 0
    }