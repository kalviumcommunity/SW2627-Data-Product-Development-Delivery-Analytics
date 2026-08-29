"""
SQL Business Metrics Query Design Module
Provides functions for calculating business metrics using SQL queries.
"""

import pandas as pd
import sqlite3
from typing import Dict, List, Optional


def calculate_employee_utilization(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Calculate employee utilization metrics.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with utilization metrics
    """
    query = """
    SELECT 
        employee_id,
        COUNT(*) as timesheet_count,
        SUM(hours_logged) as total_hours,
        SUM(billable_hours) as total_billable_hours,
        ROUND(SUM(billable_hours) * 100.0 / SUM(hours_logged), 2) as utilization_rate
    FROM timesheets
    GROUP BY employee_id
    ORDER BY utilization_rate DESC
    """
    return pd.read_sql_query(query, conn)


def calculate_department_metrics(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Calculate department-level metrics.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with department metrics
    """
    query = """
    SELECT 
        e.department,
        COUNT(DISTINCT e.employee_id) as employee_count,
        ROUND(AVG(t.hours_logged), 2) as avg_daily_hours,
        ROUND(SUM(t.billable_hours) * 100.0 / SUM(t.hours_logged), 2) as utilization_rate
    FROM employees e
    LEFT JOIN timesheets t ON e.employee_id = t.employee_id
    GROUP BY e.department
    ORDER BY utilization_rate DESC
    """
    return pd.read_sql_query(query, conn)


def calculate_project_billing(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Calculate project billing metrics.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with project billing
    """
    query = """
    SELECT 
        project_id,
        COUNT(*) as billing_records,
        SUM(billable_hours) as total_hours,
        SUM(billed_amount) as total_amount,
        ROUND(SUM(billed_amount) / SUM(billable_hours), 2) as hourly_rate
    FROM billing
    GROUP BY project_id
    ORDER BY total_amount DESC
    """
    return pd.read_sql_query(query, conn)


def calculate_allocation_efficiency(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Calculate allocation efficiency metrics.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with allocation efficiency
    """
    query = """
    SELECT 
        employee_id,
        SUM(allocated_hours) as total_allocated,
        SUM(planned_billable_hours) as total_planned_billable,
        ROUND(SUM(planned_billable_hours) * 100.0 / SUM(allocated_hours), 2) as efficiency_rate
    FROM allocations
    GROUP BY employee_id
    ORDER BY efficiency_rate DESC
    """
    return pd.read_sql_query(query, conn)


def calculate_revenue_by_department(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Calculate revenue by department.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with revenue by department
    """
    query = """
    SELECT 
        e.department,
        COUNT(DISTINCT b.billing_id) as billing_count,
        SUM(b.billed_amount) as total_revenue,
        ROUND(AVG(b.billed_amount), 2) as avg_billing_amount
    FROM billing b
    JOIN employees e ON b.employee_id = e.employee_id
    GROUP BY e.department
    ORDER BY total_revenue DESC
    """
    return pd.read_sql_query(query, conn)


def get_business_metrics_summary(conn: sqlite3.Connection) -> Dict:
    """
    Get comprehensive business metrics summary.
    
    Args:
        conn: SQLite connection
    
    Returns:
        Dictionary with business metrics
    """
    utilization = calculate_employee_utilization(conn)
    department = calculate_department_metrics(conn)
    billing = calculate_project_billing(conn)
    
    return {
        'employee_utilization': {
            'avg_rate': round(utilization['utilization_rate'].mean(), 2),
            'max_rate': round(utilization['utilization_rate'].max(), 2),
            'min_rate': round(utilization['utilization_rate'].min(), 2)
        },
        'department_metrics': {
            'avg_employees': round(department['employee_count'].mean(), 2),
            'avg_utilization': round(department['utilization_rate'].mean(), 2)
        },
        'billing_metrics': {
            'total_projects': len(billing),
            'avg_hourly_rate': round(billing['hourly_rate'].mean(), 2),
            'total_revenue': round(billing['total_amount'].sum(), 2)
        }
    }