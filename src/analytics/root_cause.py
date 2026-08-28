"""
Root Cause Investigation Workflow Module
Provides functions for investigating low utilization and identifying bottlenecks.
"""

import pandas as pd
import numpy as np


def investigate_low_utilization(df: pd.DataFrame, employee_id: str = None, threshold: float = 60) -> dict:
    """
    Investigate employees with low utilization.
    
    Args:
        df: DataFrame with utilization data
        employee_id: Specific employee to investigate (None for all)
        threshold: Utilization threshold for low utilization
    
    Returns:
        Dictionary with investigation results
    """
    if 'kpi_billable_utilization_rate' not in df.columns:
        return {'error': 'Utilization rate not calculated'}
    
    results = {}
    
    if employee_id:
        emp_data = df[df['employee_id'] == employee_id]
        if len(emp_data) == 0:
            return {'error': f'Employee {employee_id} not found'}
        low_util = emp_data[emp_data['kpi_billable_utilization_rate'] < threshold]
    else:
        low_util = df[df['kpi_billable_utilization_rate'] < threshold]
    
    results['low_utilization_count'] = len(low_util)
    results['low_utilization_pct'] = round(len(low_util) / len(df) * 100, 2)
    
    if len(low_util) > 0:
        results['affected_employees'] = low_util['employee_id'].unique().tolist() if 'employee_id' in low_util.columns else []
        results['avg_utilization'] = round(low_util['kpi_billable_utilization_rate'].mean(), 2)
        results['min_utilization'] = round(low_util['kpi_billable_utilization_rate'].min(), 2)
        
        # Analyze task distribution for low utilization employees
        if 'task_category' in low_util.columns:
            task_dist = low_util['task_category'].value_counts(normalize=True).round(4).to_dict()
            results['task_distribution'] = task_dist
        
        # Analyze non-billable hours
        if 'non_billable_hours' in low_util.columns:
            results['avg_non_billable'] = round(low_util['non_billable_hours'].mean(), 2)
            results['total_non_billable'] = round(low_util['non_billable_hours'].sum(), 2)
        
        # Analyze admin hours
        if 'admin_hours' in low_util.columns:
            results['avg_admin'] = round(low_util['admin_hours'].mean(), 2)
        
        # Analyze training hours
        if 'training_hours' in low_util.columns:
            results['avg_training'] = round(low_util['training_hours'].mean(), 2)
    
    return results


def identify_bottlenecks(df: pd.DataFrame, department: str = None) -> dict:
    """
    Identify operational bottlenecks by department or team.
    
    Args:
        df: DataFrame with operational data
        department: Specific department to analyze (None for all)
    
    Returns:
        Dictionary with bottleneck analysis
    """
    if department:
        dept_data = df[df['department'] == department] if 'department' in df.columns else df
    else:
        dept_data = df
    
    bottlenecks = {}
    
    if 'kpi_billable_utilization_rate' in dept_data.columns:
        # Low utilization as bottleneck indicator
        low_util = dept_data[dept_data['kpi_billable_utilization_rate'] < 60]
        bottlenecks['low_utilization_count'] = len(low_util)
        bottlenecks['low_utilization_pct'] = round(len(low_util) / len(dept_data) * 100, 2)
    
    if 'non_billable_hours' in dept_data.columns:
        high_non_billable = dept_data[dept_data['non_billable_hours'] > dept_data['non_billable_hours'].quantile(0.75)]
        bottlenecks['high_non_billable_count'] = len(high_non_billable)
        bottlenecks['high_non_billable_pct'] = round(len(high_non_billable) / len(dept_data) * 100, 2)
    
    if 'admin_hours' in dept_data.columns:
        high_admin = dept_data[dept_data['admin_hours'] > dept_data['admin_hours'].quantile(0.75)]
        bottlenecks['high_admin_count'] = len(high_admin)
        bottlenecks['high_admin_pct'] = round(len(high_admin) / len(dept_data) * 100, 2)
    
    if 'overtime_hours' in dept_data.columns:
        high_overtime = dept_data[dept_data['overtime_hours'] > dept_data['overtime_hours'].quantile(0.75)]
        bottlenecks['high_overtime_count'] = len(high_overtime)
        bottlenecks['high_overtime_pct'] = round(len(high_overtime) / len(dept_data) * 100, 2)
    
    if 'kpi_writeoff_rate' in dept_data.columns:
        high_writeoff = dept_data[dept_data['kpi_writeoff_rate'] > 10]
        bottlenecks['high_writeoff_count'] = len(high_writeoff)
        bottlenecks['high_writeoff_pct'] = round(len(high_writeoff) / len(dept_data) * 100, 2)
    
    return bottlenecks


def analyze_task_distribution(df: pd.DataFrame, employee_id: str) -> dict:
    """
    Analyze task distribution for a specific employee.
    
    Args:
        df: DataFrame with task data
        employee_id: Employee ID to analyze
    
    Returns:
        Dictionary with task distribution analysis
    """
    emp_data = df[df['employee_id'] == employee_id]
    
    if len(emp_data) == 0:
        return {'error': f'Employee {employee_id} not found'}
    
    results = {
        'total_entries': len(emp_data),
        'total_hours': round(emp_data['hours_logged'].sum(), 2) if 'hours_logged' in emp_data.columns else 0
    }
    
    if 'task_category' in emp_data.columns:
        task_dist = emp_data.groupby('task_category').agg({
            'hours_logged': 'sum',
            'billable_hours': 'sum'
        }).round(2)
        results['task_breakdown'] = task_dist.to_dict()
    
    if 'project_id' in emp_data.columns:
        project_dist = emp_data.groupby('project_id').agg({
            'hours_logged': 'sum',
            'billable_hours': 'sum'
        }).round(2).sort_values('hours_logged', ascending=False)
        results['project_breakdown'] = project_dist.head(10).to_dict()
    
    if 'billable_hours' in emp_data.columns and 'hours_logged' in emp_data.columns:
        results['billable_ratio'] = round(emp_data['billable_hours'].sum() / emp_data['hours_logged'].sum() * 100, 2)
    
    return results


def compare_allocated_vs_actual(df: pd.DataFrame) -> dict:
    """
    Compare allocated vs actual hours.
    
    Args:
        df: DataFrame with allocation and actual data
    
    Returns:
        Dictionary with comparison results
    """
    required = ['allocated_hours', 'hours_worked', 'employee_id']
    if not all(col in df.columns for col in required):
        return {'error': 'Required columns not found'}
    
    df = df.copy()
    df['variance'] = df['hours_worked'] - df['allocated_hours']
    df['variance_pct'] = np.where(df['allocated_hours'] > 0, (df['variance'] / df['allocated_hours']) * 100, 0)
    
    overall = {
        'total_allocated': round(df['allocated_hours'].sum(), 2),
        'total_actual': round(df['hours_worked'].sum(), 2),
        'total_variance': round(df['variance'].sum(), 2),
        'avg_variance_pct': round(df['variance_pct'].mean(), 2),
        'over_allocated_count': int((df['variance'] > 0).sum()),
        'under_allocated_count': int((df['variance'] < 0).sum()),
        'on_target_count': int((df['variance'] == 0).sum())
    }
    
    by_employee = df.groupby('employee_id').agg({
        'allocated_hours': 'sum',
        'hours_worked': 'sum',
        'variance': 'sum',
        'variance_pct': 'mean'
    }).round(2)
    
    return {
        'overall': overall,
        'by_employee': by_employee.to_dict()
    }


def generate_root_cause_report(df: pd.DataFrame, segment: str = None) -> dict:
    """
    Generate comprehensive root cause report.
    
    Args:
        df: DataFrame with analytics data
        segment: Segment to analyze ('department', 'team', 'employee')
    
    Returns:
        Dictionary with root cause report
    """
    report = {
        'segment': segment,
        'timestamp': pd.Timestamp.now().isoformat()
    }
    
    if segment == 'department' and 'department' in df.columns:
        dept_results = {}
        for dept in df['department'].unique():
            dept_data = df[df['department'] == dept]
            dept_results[dept] = {
                'low_utilization': investigate_low_utilization(dept_data),
                'bottlenecks': identify_bottlenecks(dept_data)
            }
        report['by_department'] = dept_results
    
    elif segment == 'employee' and 'employee_id' in df.columns:
        low_util_emps = df[df['kpi_billable_utilization_rate'] < 60]['employee_id'].unique()
        emp_results = {}
        for emp in low_util_emps:
            emp_results[emp] = {
                'low_utilization': investigate_low_utilization(df, emp),
                'task_distribution': analyze_task_distribution(df, emp)
            }
        report['low_utilization_employees'] = emp_results
    
    else:
        report['overall'] = {
            'low_utilization': investigate_low_utilization(df),
            'bottlenecks': identify_bottlenecks(df),
            'allocated_vs_actual': compare_allocated_vs_actual(df)
        }
    
    return report


def get_root_cause_summary(report: dict) -> dict:
    """
    Get summary of root cause analysis.
    
    Args:
        report: Root cause report dictionary
    
    Returns:
        Summary dictionary
    """
    summary = {}
    
    if 'overall' in report:
        ov = report['overall']
        summary['low_utilization_pct'] = ov.get('low_utilization', {}).get('low_utilization_pct', 0)
        summary['bottlenecks'] = ov.get('bottlenecks', {})
    
    if 'by_department' in report:
        dept_summary = {}
        for dept, data in report['by_department'].items():
            dept_summary[dept] = {
                'low_util_pct': data.get('low_utilization', {}).get('low_utilization_pct', 0),
                'bottlenecks': data.get('bottlenecks', {})
            }
        summary['by_department'] = dept_summary
    
    if 'low_utilization_employees' in report:
        summary['affected_employee_count'] = len(report['low_utilization_employees'])
    
    return summary