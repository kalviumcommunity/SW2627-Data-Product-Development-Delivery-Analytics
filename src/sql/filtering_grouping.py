"""
SQL Filtering, Grouping & Aggregation Module
Provides functions for SQL queries with filtering and grouping.
"""

import pandas as pd
import sqlite3
from typing import Dict, List, Optional


def filter_employees_by_department(conn: sqlite3.Connection, department: str) -> pd.DataFrame:
    """
    Filter employees by department.
    
    Args:
        conn: SQLite connection
        department: Department name to filter
    
    Returns:
        DataFrame with filtered employees
    """
    query = """
    SELECT * FROM employees
    WHERE department = ?
    """
    return pd.read_sql_query(query, conn, params=(department,))


def filter_employees_by_experience(conn: sqlite3.Connection, min_years: int) -> pd.DataFrame:
    """
    Filter employees by minimum experience.
    
    Args:
        conn: SQLite connection
        min_years: Minimum years of experience
    
    Returns:
        DataFrame with filtered employees
    """
    query = """
    SELECT * FROM employees
    WHERE experience_years >= ?
    """
    return pd.read_sql_query(query, conn, params=(min_years,))


def group_employees_by_department(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Group employees by department.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with department counts
    """
    query = """
    SELECT 
        department,
        COUNT(*) as employee_count,
        ROUND(AVG(experience_years), 2) as avg_experience
    FROM employees
    GROUP BY department
    ORDER BY employee_count DESC
    """
    return pd.read_sql_query(query, conn)


def group_timesheets_by_project(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Group timesheets by project.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with project summaries
    """
    query = """
    SELECT 
        project_id,
        COUNT(*) as timesheet_count,
        SUM(hours_logged) as total_hours,
        SUM(billable_hours) as total_billable,
        ROUND(SUM(billable_hours) * 100.0 / SUM(hours_logged), 2) as utilization_rate
    FROM timesheets
    GROUP BY project_id
    ORDER BY total_hours DESC
    """
    return pd.read_sql_query(query, conn)


def aggregate_billing_by_month(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Aggregate billing by month.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with monthly billing
    """
    query = """
    SELECT 
        billing_month,
        COUNT(*) as billing_count,
        SUM(billed_amount) as total_amount,
        ROUND(AVG(billed_amount), 2) as avg_amount
    FROM billing
    GROUP BY billing_month
    ORDER BY billing_month
    """
    return pd.read_sql_query(query, conn)


def filter_high_utilization(conn: sqlite3.Connection, threshold: float = 70) -> pd.DataFrame:
    """
    Filter employees with high utilization.
    
    Args:
        conn: SQLite connection
        threshold: Utilization threshold
    
    Returns:
        DataFrame with high utilization employees
    """
    query = """
    SELECT 
        employee_id,
        COUNT(*) as timesheet_count,
        SUM(hours_logged) as total_hours,
        SUM(billable_hours) as total_billable,
        ROUND(SUM(billable_hours) * 100.0 / SUM(hours_logged), 2) as utilization_rate
    FROM timesheets
    GROUP BY employee_id
    HAVING utilization_rate > ?
    ORDER BY utilization_rate DESC
    """
    return pd.read_sql_query(query, conn, params=(threshold,))


def group_allocations_by_role(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Group allocations by role.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with role summaries
    """
    query = """
    SELECT 
        project_role,
        COUNT(*) as allocation_count,
        SUM(allocated_hours) as total_hours,
        ROUND(AVG(allocation_percentage), 2) as avg_percentage
    FROM allocations
    GROUP BY project_role
    ORDER BY total_hours DESC
    """
    return pd.read_sql_query(query, conn)


def get_aggregation_summary(conn: sqlite3.Connection) -> Dict:
    """
    Get comprehensive aggregation summary.
    
    Args:
        conn: SQLite connection
    
    Returns:
        Dictionary with aggregation summary
    """
    dept = group_employees_by_department(conn)
    project = group_timesheets_by_project(conn)
    monthly = aggregate_billing_by_month(conn)
    
    return {
        'department_count': len(dept),
        'project_count': len(project),
        'monthly_billing_count': len(monthly),
        'avg_employees_per_dept': round(dept['employee_count'].mean(), 2),
        'avg_hours_per_project': round(project['total_hours'].mean(), 2),
        'total_monthly_revenue': round(monthly['total_amount'].sum(), 2)
    }