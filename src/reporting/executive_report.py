"""
Executive Reporting & Stakeholder Communication Module
Provides functions for creating executive reports and stakeholder communication materials.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional


def generate_executive_summary(df: pd.DataFrame, metric_col: str, group_col: str = None) -> Dict:
    """
    Generate an executive summary for stakeholder reporting.
    
    Args:
        df: DataFrame with data
        metric_col: Column with metric values
        group_col: Column to group by (optional)
    
    Returns:
        Dictionary with executive summary structure
    """
    metric_data = pd.to_numeric(df[metric_col], errors='coerce').dropna()
    
    total = float(metric_data.sum())
    average = float(metric_data.mean())
    median = float(metric_data.median())
    minimum = float(metric_data.min())
    maximum = float(metric_data.max())
    std_dev = float(metric_data.std())
    count = int(metric_data.count())
    
    # Determine trend direction
    trend = "STABLE"
    if count > 1:
        first_half = metric_data.iloc[:len(metric_data)//2].mean()
        second_half = metric_data.iloc[len(metric_data)//2:].mean()
        if second_half > first_half * 1.05:
            trend = "IMPROVING"
        elif second_half < first_half * 0.95:
            trend = "DECLINING"
    
    # Determine status
    status = "EXCEEDING" if average >= 65 else "WARNING" if average >= 60 else "CRITICAL"
    
    # Build summary
    summary = {
        'metric': metric_col,
        'total': total,
        'average': average,
        'median': median,
        'minimum': minimum,
        'maximum': maximum,
        'std_dev': std_dev,
        'count': count,
        'trend': trend,
        'status': status,
        'executive_summary': f"""
Executive Summary: {metric_col} Analysis

Key Performance Indicators:
- Current Rate: {average:.1f}%
- Target Rate: 65%
- Status: {status}
- Total Records: {count:,}
- Trend Direction: {trend}

Recommendations:
- Monitor {metric_col} closely if status is WARNING or CRITICAL
- Investigate factors contributing to {trend.lower()} trend
- Implement improvement strategies if needed
- Regular reporting recommended for stakeholder awareness
"""
    }
    
    return summary


def generate_stakeholder_report(df: pd.DataFrame, metric_col: str, group_col: str = None, 
                                include_chart_recs: bool = True) -> Dict:
    """
    Generate a comprehensive stakeholder report.
    
    Args:
        df: DataFrame with data
        metric_col: Column with metric values
        group_col: Column to group by (optional)
        include_chart_recs: Whether to include chart recommendations
    
    Returns:
        Dictionary with stakeholder report structure
    """
    metric_data = pd.to_numeric(df[metric_col], errors='coerce').dropna()
    
    total = float(metric_data.sum())
    average = float(metric_data.mean())
    count = int(metric_data.count())
    
    # Group analysis if group_col provided
    group_analysis = {}
    if group_col and group_col in df.columns:
        grouped = df.groupby(group_col).size().to_frame('count')
        grouped['sum'] = pd.to_numeric(df[metric_col], errors='coerce').groupby(df[group_col]).sum()
        grouped['mean'] = pd.to_numeric(df[metric_col], errors='coerce').groupby(df[group_col]).mean()
        grouped = grouped.reset_index()
        group_analysis = {
            str(k): {
                'total': float(row['sum']) if pd.notna(row['sum']) else 0,
                'average': float(row['mean']) if pd.notna(row['mean']) else 0,
                'count': int(row['count'])
            }
            for k, row in grouped.iterrows()
        }
    
    # Determine key insights
    insights = []
    if average >= 70:
        insights.append("Performance is strong; maintain current strategies")
    elif average >= 65:
        insights.append("Performance is acceptable; minor improvements recommended")
    elif average >= 60:
        insights.append("Performance needs attention; targeted improvements suggested")
    else:
        insights.append("Performance requires immediate intervention")
    
    # Chart recommendations
    chart_recs = []
    if include_chart_recs:
        if group_col and group_col in df.columns:
            chart_recs = ["bar chart for group comparison", "pie chart for distribution"]
        else:
            chart_recs = ["bar chart for trend analysis", "line chart for time series"]
    
    report = {
        'metric': metric_col,
        'total': total,
        'average': average,
        'count': count,
        'status': "EXCEEDING" if average >= 70 else "WARNING" if average >= 60 else "CRITICAL",
        'group_analysis': group_analysis,
        'insights': insights,
        'chart_recommendations': chart_recs,
        'executive_summary': generate_executive_summary(df, metric_col, group_col)['executive_summary']
    }
    
    return report


def format_report_for_presentation(report: Dict, max_sections: int = 5) -> str:
    """
    Format a report for presentation to stakeholders.
    
    Args:
        report: Report dictionary
        max_sections: Maximum number of sections to include
    
    Returns:
        Formatted report string
    """
    lines = [
        f"=== EXECUTIVE REPORT: {report['metric'].upper()} ===",
        f"Status: {report['status']}",
        f"Total: {report['total']:,.2f}",
        f"Average: {report['average']:,.2f}",
        f"Records Analyzed: {report['count']:,}",
        "",
        "Key Insights:",
    ]
    
    for i, insight in enumerate(report['insights'][:max_sections], 1):
        lines.append(f"  {i}. {insight}")
    
    if report['group_analysis']:
        lines.append("")
        lines.append("Performance by Group:")
        for group, data in list(report['group_analysis'].items())[:3]:
            lines.append(f"  - {group}: avg {data['average']:,.2f} ({data['count']:,} records)")
    
    lines.extend([
        "",
        "Recommendations:",
        *report['chart_recommendations'],
        "",
        report['executive_summary']
    ])
    
    return "\n".join(lines)


def validate_report_data(df: pd.DataFrame, required_columns: List[str], min_rows: int = 10) -> Dict:
    """
    Validate data quality for executive reporting.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required columns
        min_rows: Minimum number of rows required for executive report
    
    Returns:
        Dictionary with validation results
    """
    missing = [col for col in required_columns if col not in df.columns]
    null_count = df[required_columns].isnull().sum().sum() if all(col in df.columns for col in required_columns) else 0
    row_count = len(df)
    
    # Calculate data quality score
    quality_deductions = 0
    if missing:
        quality_deductions += len(missing) * 15
    if null_count > 0:
        quality_deductions += min(null_count, 50) * 2
    
    quality_score = max(0, 100 - quality_deductions)
    
    return {
        'valid': len(missing) == 0 and row_count >= min_rows,
        'missing_columns': missing,
        'null_count': int(null_count),
        'row_count': row_count,
        'meets_minimum': row_count >= min_rows,
        'data_quality_score': quality_score
    }


def get_reporting_recommendations(df: pd.DataFrame, metric_col: str, group_col: str = None) -> Dict:
    """
    Get reporting recommendations based on data characteristics.
    
    Args:
        df: DataFrame with data
        metric_col: Column with metric values
        group_col: Column to group by (optional)
    
    Returns:
        Dictionary with reporting recommendations
    """
    metric_data = pd.to_numeric(df[metric_col], errors='coerce').dropna()
    avg = float(metric_data.mean())
    count = int(metric_data.count())
    
    return {
        'recommended_frequency': 'weekly' if count > 1000 else 'monthly',
        'recommended_format': 'executive summary' if avg >= 65 else 'detailed analysis',
        'stakeholder_level': 'C-level' if avg >= 70 else 'management',
        'alert_threshold': 60,
        'success_criteria': 'average >= 65%',
        'improvement_focus': 'targeted training' if avg < 65 else 'best practice sharing'
    }