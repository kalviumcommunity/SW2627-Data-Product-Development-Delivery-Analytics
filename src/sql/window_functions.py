"""
SQL Window Functions & Ranking Systems Module
Provides functions for SQL window functions and ranking.
"""

import pandas as pd
import sqlite3
from typing import Dict, List, Optional


def rank_employees_by_utilization(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Rank employees by utilization rate.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with ranked employees
    """
    query = """
    SELECT 
        employee_id,
        SUM(hours_logged) as total_hours,
        SUM(billable_hours) as total_billable,
        ROUND(SUM(billable_hours) * 100.0 / SUM(hours_logged), 2) as utilization_rate,
        RANK() OVER (ORDER BY SUM(billable_hours) * 100.0 / SUM(hours_logged) DESC) as rank
    FROM timesheets
    GROUP BY employee_id
    ORDER BY rank
    """
    return pd.read_sql_query(query, conn)


def rank_employees_by_revenue(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Rank employees by total revenue.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with ranked employees
    """
    query = """
    SELECT 
        employee_id,
        SUM(billed_amount) as total_revenue,
        COUNT(*) as billing_count,
        RANK() OVER (ORDER BY SUM(billed_amount) DESC) as rank
    FROM billing
    GROUP BY employee_id
    ORDER BY rank
    """
    return pd.read_sql_query(query, conn)


def department_ranking(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Rank departments by utilization.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with ranked departments
    """
    query = """
    SELECT 
        e.department,
        COUNT(DISTINCT t.employee_id) as employee_count,
        ROUND(SUM(t.billable_hours) * 100.0 / SUM(t.hours_logged), 2) as utilization_rate,
        RANK() OVER (ORDER BY SUM(t.billable_hours) * 100.0 / SUM(t.hours_logged) DESC) as rank
    FROM timesheets t
    LEFT JOIN employees e ON t.employee_id = e.employee_id
    GROUP BY e.department
    ORDER BY rank
    """
    return pd.read_sql_query(query, conn)


def running_total_hours(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Calculate running total of hours by employee.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with running totals
    """
    query = """
    SELECT 
        employee_id,
        work_date,
        hours_logged,
        SUM(hours_logged) OVER (PARTITION BY employee_id ORDER BY work_date) as running_total
    FROM timesheets
    ORDER BY employee_id, work_date
    LIMIT 100
    """
    return pd.read_sql_query(query, conn)


def moving_average_hours(conn: sqlite3.Connection, window: int = 7) -> pd.DataFrame:
    """
    Calculate moving average of hours.
    
    Args:
        conn: SQLite connection
        window: Window size for moving average
    
    Returns:
        DataFrame with moving averages
    """
    query = f"""
    SELECT 
        employee_id,
        work_date,
        hours_logged,
        ROUND(AVG(hours_logged) OVER (PARTITION BY employee_id ORDER BY work_date ROWS BETWEEN {window-1} PRECEDING AND CURRENT ROW), 2) as moving_avg
    FROM timesheets
    ORDER BY employee_id, work_date
    LIMIT 100
    """
    return pd.read_sql_query(query, conn)


def dense_rank_employees(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Dense rank employees by experience.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with dense ranks
    """
    query = """
    SELECT 
        employee_id,
        department,
        experience_years,
        DENSE_RANK() OVER (PARTITION BY department ORDER BY experience_years DESC) as dept_rank,
        DENSE_RANK() OVER (ORDER BY experience_years DESC) as overall_rank
    FROM employees
    ORDER BY overall_rank
    """
    return pd.read_sql_query(query, conn)


def lag_lead_hours(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Calculate lag and lead of hours for trend analysis.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with lag/lead values
    """
    query = """
    SELECT 
        employee_id,
        work_date,
        hours_logged,
        LAG(hours_logged) OVER (PARTITION BY employee_id ORDER BY work_date) as prev_hours,
        LEAD(hours_logged) OVER (PARTITION BY employee_id ORDER BY work_date) as next_hours
    FROM timesheets
    ORDER BY employee_id, work_date
    LIMIT 100
    """
    return pd.read_sql_query(query, conn)


def percent_rank_utilization(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Calculate percent rank of utilization.
    
    Args:
        conn: SQLite connection
    
    Returns:
        DataFrame with percent ranks
    """
    query = """
    SELECT 
        employee_id,
        SUM(billable_hours) * 100.0 / SUM(hours_logged) as utilization_rate,
        PERCENT_RANK() OVER (ORDER BY SUM(billable_hours) * 100.0 / SUM(hours_logged)) as pct_rank
    FROM timesheets
    GROUP BY employee_id
    ORDER BY utilization_rate DESC
    """
    return pd.read_sql_query(query, conn)


def ntile_groups(conn: sqlite3.Connection, n: int = 4) -> pd.DataFrame:
    """
    Divide employees into n groups by utilization.
    
    Args:
        conn: SQLite connection
        n: Number of groups
    
    Returns:
        DataFrame with groups
    """
    query = f"""
    SELECT 
        employee_id,
        SUM(billable_hours) * 100.0 / SUM(hours_logged) as utilization_rate,
        NTILE({n}) OVER (ORDER BY SUM(billable_hours) * 100.0 / SUM(hours_logged)) as utilization_group
    FROM timesheets
    GROUP BY employee_id
    ORDER BY utilization_rate DESC
    """
    return pd.read_sql_query(query, conn)


def get_window_function_summary(conn: sqlite3.Connection) -> Dict:
    """
    Get summary of window function analysis.
    
    Args:
        conn: SQLite connection
    
    Returns:
        Dictionary with window function summary
    """
    ranked = rank_employees_by_utilization(conn)
    depts = department_ranking(conn)
    groups = ntile_groups(conn)
    
    return {
        'total_employees_ranked': len(ranked),
        'total_departments': len(depts),
        'top_employee': ranked.iloc[0]['employee_id'] if len(ranked) > 0 else None,
        'top_utilization': ranked.iloc[0]['utilization_rate'] if len(ranked) > 0 else None,
        'top_department': depts.iloc[0]['department'] if len(depts) > 0 else None,
        'quartile_distribution': groups['utilization_group'].value_counts().to_dict() if 'utilization_group' in groups.columns else {}
    }