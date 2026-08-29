"""
SQL Joins & Multi-Table Analysis Module
Provides functions for SQL joins across multiple tables.
"""

import pandas as pd
import sqlite3
from typing import Dict, List, Optional


def join_timesheets_with_employees(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Join timesheets with employees table.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with joined data
    """
    query = """
    SELECT 
        t.*,
        e.department,
        e.team,
        e.designation,
        e.experience_years,
        e.location
    FROM timesheets t
    LEFT JOIN employees e ON t.employee_id = e.employee_id
    """
    return pd.read_sql_query(query, conn)


def join_allocations_with_employees(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Join allocations with employees table.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with joined data
    """
    query = """
    SELECT 
        a.*,
        e.department,
        e.team,
        e.designation,
        e.experience_years,
        e.location
    FROM allocations a
    LEFT JOIN employees e ON a.employee_id = e.employee_id
    """
    return pd.read_sql_query(query, conn)


def join_billing_with_employees(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Join billing with employees table.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with joined data
    """
    query = """
    SELECT 
        b.*,
        e.department,
        e.team,
        e.designation,
        e.experience_years,
        e.location
    FROM billing b
    LEFT JOIN employees e ON b.employee_id = e.employee_id
    """
    return pd.read_sql_query(query, conn)


def join_timesheets_with_allocations(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Join timesheets with allocations.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with joined data
    """
    query = """
    SELECT 
        t.*,
        a.allocated_hours,
        a.allocation_percentage,
        a.project_role,
        a.staffing_status
    FROM timesheets t
    LEFT JOIN allocations a ON t.employee_id = a.employee_id AND t.project_id = a.project_id
    """
    return pd.read_sql_query(query, conn)


def join_all_tables(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Join all tables into a comprehensive dataset.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with all joined data
    """
    query = """
    SELECT 
        t.employee_id,
        t.project_id,
        t.hours_logged,
        t.billable_hours,
        t.non_billable_hours,
        e.department,
        e.team,
        e.designation,
        e.experience_years,
        e.location,
        a.allocated_hours,
        a.allocation_percentage,
        a.project_role,
        b.billed_amount,
        b.billing_rate
    FROM timesheets t
    LEFT JOIN employees e ON t.employee_id = e.employee_id
    LEFT JOIN allocations a ON t.employee_id = a.employee_id AND t.project_id = a.project_id
    LEFT JOIN billing b ON t.employee_id = b.employee_id AND t.project_id = b.project_id
    """
    return pd.read_sql_query(query, conn)


def aggregate_by_department(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Aggregate metrics by department using joins.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with department aggregation
    """
    query = """
    SELECT 
        e.department,
        COUNT(DISTINCT t.employee_id) as employee_count,
        SUM(t.hours_logged) as total_hours,
        SUM(t.billable_hours) as total_billable,
        ROUND(SUM(t.billable_hours) * 100.0 / SUM(t.hours_logged), 2) as utilization_rate,
        SUM(b.billed_amount) as total_revenue
    FROM timesheets t
    LEFT JOIN employees e ON t.employee_id = e.employee_id
    LEFT JOIN billing b ON t.employee_id = b.employee_id AND t.project_id = b.project_id
    GROUP BY e.department
    ORDER BY total_revenue DESC
    """
    return pd.read_sql_query(query, conn)


def aggregate_by_project(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Aggregate metrics by project using joins.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with project aggregation
    """
    query = """
    SELECT 
        t.project_id,
        COUNT(DISTINCT t.employee_id) as employee_count,
        SUM(t.hours_logged) as total_hours,
        SUM(t.billable_hours) as total_billable,
        ROUND(SUM(t.billable_hours) * 100.0 / SUM(t.hours_logged), 2) as utilization_rate,
        SUM(b.billed_amount) as total_revenue,
        a.allocated_hours as planned_hours
    FROM timesheets t
    LEFT JOIN billing b ON t.employee_id = b.employee_id AND t.project_id = b.project_id
    LEFT JOIN allocations a ON t.employee_id = a.employee_id AND t.project_id = a.project_id
    GROUP BY t.project_id
    ORDER BY total_revenue DESC
    """
    return pd.read_sql_query(query, conn)


def get_join_summary(conn: sqlite3.Connection) -> Dict:
    """
    Get summary of join operations.
    
    Args:
        conn: SQLite connection
    
    Returns:
        Dictionary with join summary
    """
    timesheets = join_timesheets_with_employees(conn)
    allocations = join_allocations_with_employees(conn)
    billing = join_billing_with_employees(conn)
    all_tables = join_all_tables(conn)
    
    return {
        'timesheets_joined': len(timesheets),
        'allocations_joined': len(allocations),
        'billing_joined': len(billing),
        'all_tables_joined': len(all_tables),
        'unique_employees': timesheets['employee_id'].nunique() if 'employee_id' in timesheets.columns else 0,
        'unique_projects': timesheets['project_id'].nunique() if 'project_id' in timesheets.columns else 0
    }