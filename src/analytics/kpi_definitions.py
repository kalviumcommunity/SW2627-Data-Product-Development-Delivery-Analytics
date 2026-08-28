"""
KPI Definition & Business Metric Design Module
Provides functions for calculating key performance indicators.
"""

import pandas as pd
import numpy as np


def calculate_billable_utilization_rate(billable_hours: pd.Series, total_hours: pd.Series) -> pd.Series:
    """
    Calculate billable utilization rate.
    
    KPI: Billable Utilization Rate = billable_hours / total_hours * 100
    
    Args:
        billable_hours: Series of billable hours
        total_hours: Series of total hours
    
    Returns:
        Series of utilization rates (percentage)
    """
    return np.where(total_hours > 0, (billable_hours / total_hours) * 100, 0)


def calculate_allocation_efficiency(actual_hours: pd.Series, allocated_hours: pd.Series) -> pd.Series:
    """
    Calculate allocation efficiency.
    
    KPI: Allocation Efficiency = actual_hours / allocated_hours * 100
    
    Args:
        actual_hours: Series of actual hours worked
        allocated_hours: Series of allocated hours
    
    Returns:
        Series of allocation efficiency (percentage)
    """
    return np.where(allocated_hours > 0, (actual_hours / allocated_hours) * 100, 0)


def calculate_revenue_per_hour(billed_amount: pd.Series, billable_hours: pd.Series) -> pd.Series:
    """
    Calculate revenue per billable hour.
    
    KPI: Revenue per Hour = billed_amount / billable_hours
    
    Args:
        billed_amount: Series of billed amounts
        billable_hours: Series of billable hours
    
    Returns:
        Series of revenue per hour
    """
    return np.where(billable_hours > 0, billed_amount / billable_hours, 0)


def calculate_non_billable_load(non_billable_hours: pd.Series, total_hours: pd.Series) -> pd.Series:
    """
    Calculate non-billable load percentage.
    
    KPI: Non-Billable Load = non_billable_hours / total_hours * 100
    
    Args:
        non_billable_hours: Series of non-billable hours
        total_hours: Series of total hours
    
    Returns:
        Series of non-billable load (percentage)
    """
    return np.where(total_hours > 0, (non_billable_hours / total_hours) * 100, 0)


def calculate_timesheet_compliance(approved_count: pd.Series, total_count: pd.Series) -> pd.Series:
    """
    Calculate timesheet compliance rate.
    
    KPI: Timesheet Compliance = approved_timesheets / total_timesheets * 100
    
    Args:
        approved_count: Series of approved timesheet counts
        total_count: Series of total timesheet counts
    
    Returns:
        Series of compliance rates (percentage)
    """
    return np.where(total_count > 0, (approved_count / total_count) * 100, 0)


def calculate_billing_accuracy(billed_hours: pd.Series, timesheet_billable_hours: pd.Series) -> pd.Series:
    """
    Calculate billing accuracy.
    
    KPI: Billing Accuracy = billed_hours / timesheet_billable_hours * 100
    
    Args:
        billed_hours: Series of billed hours
        timesheet_billable_hours: Series of timesheet billable hours
    
    Returns:
        Series of billing accuracy (percentage)
    """
    return np.where(timesheet_billable_hours > 0, (billed_hours / timesheet_billable_hours) * 100, 0)


def calculate_writeoff_rate(writeoff_hours: pd.Series, billed_hours: pd.Series) -> pd.Series:
    """
    Calculate write-off rate.
    
    KPI: Write-Off Rate = writeoff_hours / billed_hours * 100
    
    Args:
        writeoff_hours: Series of write-off hours
        billed_hours: Series of billed hours
    
    Returns:
        Series of write-off rates (percentage)
    """
    return np.where(billed_hours > 0, (writeoff_hours / billed_hours) * 100, 0)


def calculate_all_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate all KPIs for the dataset.
    
    Args:
        df: DataFrame with required columns
    
    Returns:
        DataFrame with KPI columns added
    """
    df = df.copy()
    
    # Billable Utilization Rate
    if 'billable_hours' in df.columns and 'total_hours' in df.columns:
        df['kpi_billable_utilization_rate'] = calculate_billable_utilization_rate(
            df['billable_hours'], df['total_hours']
        )
    
    # Allocation Efficiency
    if 'hours_worked' in df.columns and 'allocated_hours' in df.columns:
        df['kpi_allocation_efficiency'] = calculate_allocation_efficiency(
            df['hours_worked'], df['allocated_hours']
        )
    
    # Revenue per Hour
    if 'billed_amount' in df.columns and 'billable_hours' in df.columns:
        df['kpi_revenue_per_hour'] = calculate_revenue_per_hour(
            df['billed_amount'], df['billable_hours']
        )
    
    # Non-Billable Load
    if 'non_billable_hours' in df.columns and 'total_hours' in df.columns:
        df['kpi_non_billable_load'] = calculate_non_billable_load(
            df['non_billable_hours'], df['total_hours']
        )
    
    # Timesheet Compliance
    if 'timesheet_status' in df.columns:
        approved = (df['timesheet_status'] == 'Approved').astype(int)
        total = pd.Series(1, index=df.index)
        df['kpi_timesheet_compliance'] = calculate_timesheet_compliance(approved, total)
    
    # Billing Accuracy
    if 'billed_amount' in df.columns and 'billing_rate' in df.columns and 'billable_hours' in df.columns:
        billed_hours = df['billed_amount'] / df['billing_rate'].replace(0, np.nan)
        df['kpi_billing_accuracy'] = calculate_billing_accuracy(billed_hours, df['billable_hours'])
    
    # Write-Off Rate
    if 'writeoff_hours' in df.columns and 'billable_hours' in df.columns:
        df['kpi_writeoff_rate'] = calculate_writeoff_rate(
            df['writeoff_hours'], df['billable_hours']
        )
    
    return df


def get_kpi_summary(df: pd.DataFrame) -> dict:
    """
    Get summary statistics for all KPIs.
    
    Args:
        df: DataFrame with KPI columns
    
    Returns:
        Dictionary with KPI summaries
    """
    kpi_columns = [col for col in df.columns if col.startswith('kpi_')]
    summary = {}
    
    for col in kpi_columns:
        if col in df.columns:
            series = df[col].dropna()
            if len(series) > 0:
                summary[col] = {
                    'mean': round(series.mean(), 2),
                    'median': round(series.median(), 2),
                    'std': round(series.std(), 2),
                    'min': round(series.min(), 2),
                    'max': round(series.max(), 2),
                    'count': len(series)
                }
    
    return summary


def get_kpi_targets() -> dict:
    """
    Get target values for each KPI.
    
    Returns:
        Dictionary with KPI targets
    """
    return {
        'kpi_billable_utilization_rate': {'target': 75, 'warning': 60, 'critical': 50},
        'kpi_allocation_efficiency': {'target': 100, 'warning': 80, 'critical': 70},
        'kpi_revenue_per_hour': {'target': 100, 'warning': 80, 'critical': 60},
        'kpi_non_billable_load': {'target': 15, 'warning': 25, 'critical': 35},
        'kpi_timesheet_compliance': {'target': 95, 'warning': 90, 'critical': 80},
        'kpi_billing_accuracy': {'target': 98, 'warning': 95, 'critical': 90},
        'kpi_writeoff_rate': {'target': 5, 'warning': 10, 'critical': 15}
    }


def flag_kpi_violations(df: pd.DataFrame, kpi_col: str) -> pd.Series:
    """
    Flag KPI violations based on targets.
    
    Args:
        df: DataFrame with KPI column
        kpi_col: KPI column name
    
    Returns:
        Series with violation flags
    """
    targets = get_kpi_targets()
    
    if kpi_col not in targets:
        return pd.Series('unknown', index=df.index)
    
    target_info = targets[kpi_col]
    
    # For metrics where lower is better (non_billable_load, writeoff_rate)
    lower_is_better = kpi_col in ['kpi_non_billable_load', 'kpi_writeoff_rate']
    
    if lower_is_better:
        flags = pd.Series('on_target', index=df.index)
        flags[df[kpi_col] > target_info['warning']] = 'warning'
        flags[df[kpi_col] > target_info['critical']] = 'critical'
        flags[df[kpi_col] <= target_info['target']] = 'on_target'
    else:
        flags = pd.Series('on_target', index=df.index)
        flags[df[kpi_col] < target_info['warning']] = 'warning'
        flags[df[kpi_col] < target_info['critical']] = 'critical'
        flags[df[kpi_col] >= target_info['target']] = 'on_target'
    
    return flags


def create_kpi_dashboard_data(df: pd.DataFrame) -> dict:
    """
    Create dashboard-ready KPI data.
    
    Args:
        df: DataFrame with KPI columns
    
    Returns:
        Dictionary with dashboard data
    """
    kpi_summary = get_kpi_summary(df)
    targets = get_kpi_targets()
    
    dashboard = {}
    
    for kpi_col, stats in kpi_summary.items():
        target_info = targets.get(kpi_col, {})
        
        # Determine status based on mean vs target
        mean_val = stats['mean']
        status = 'on_target'
        
        if kpi_col in ['kpi_non_billable_load', 'kpi_writeoff_rate']:
            if mean_val > target_info.get('critical', 0):
                status = 'critical'
            elif mean_val > target_info.get('warning', 0):
                status = 'warning'
        else:
            if mean_val < target_info.get('critical', 0):
                status = 'critical'
            elif mean_val < target_info.get('warning', 0):
                status = 'warning'
        
        dashboard[kpi_col] = {
            'current': mean_val,
            'target': target_info.get('target'),
            'warning_threshold': target_info.get('warning'),
            'critical_threshold': target_info.get('critical'),
            'status': status,
            'trend': 'stable'  # Would need historical data for trend
        }
    
    return dashboard