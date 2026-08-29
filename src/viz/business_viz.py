"""
Business Visualisation Principles Module
Provides functions for creating business visualizations following best practices.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple


def get_color_palette() -> Dict[str, str]:
    """
    Get standard business color palette.
    
    Returns:
        Dictionary with color names and hex codes
    """
    return {
        'primary': '#2E86AB',
        'secondary': '#A23B72',
        'accent': '#F18F01',
        'success': '#28A745',
        'warning': '#FFC107',
        'danger': '#DC3545',
        'info': '#17A2B8',
        'light': '#F8F9FA',
        'dark': '#343A40',
        'blue_shades': ['#2E86AB', '#3A9BB5', '#46AFC0', '#52C3CB', '#5ED7D6'],
        'red_shades': ['#A23B72', '#B54485', '#C84D98', '#DB56AB', '#EE5FBE'],
        'orange_shades': ['#F18F01', '#F29A1A', '#F3A533', '#F4B04C', '#F5BB65']
    }


def get_chart_type_recommendation(data_type: str, analysis_type: str) -> str:
    """
    Get chart type recommendation based on data and analysis type.
    
    Args:
        data_type: Type of data ('categorical', 'numeric', 'time_series')
        analysis_type: Type of analysis ('comparison', 'distribution', 'trend', 'composition')
    
    Returns:
        Recommended chart type
    """
    recommendations = {
        ('categorical', 'comparison'): 'Bar Chart',
        ('categorical', 'distribution'): 'Pie Chart or Donut Chart',
        ('categorical', 'composition'): 'Stacked Bar Chart',
        ('numeric', 'comparison'): 'Bar Chart or Box Plot',
        ('numeric', 'distribution'): 'Histogram or Density Plot',
        ('numeric', 'trend'): 'Line Chart',
        ('time_series', 'trend'): 'Line Chart',
        ('time_series', 'comparison'): 'Multi-Line Chart',
        ('time_series', 'composition'): 'Stacked Area Chart'
    }
    return recommendations.get((data_type, analysis_type), 'Bar Chart')


def apply_business_chart_style(fig, title: str = None, xlabel: str = None, ylabel: str = None) -> None:
    """
    Apply business chart styling to a matplotlib figure.
    
    Args:
        fig: Matplotlib figure object
        title: Chart title
        xlabel: X-axis label
        ylabel: Y-axis label
    """
    import matplotlib.pyplot as plt
    
    if title:
        fig.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
    if xlabel:
        fig.xlabel(xlabel, fontsize=10)
    if ylabel:
        fig.ylabel(ylabel, fontsize=10)
    
    fig.tick_params(labelsize=9)
    fig.grid(axis='y', alpha=0.3, linestyle='--')
    fig.spines['top'].set_visible(False)
    fig.spines['right'].set_visible(False)


def format_number(value: float, format_type: str = 'general') -> str:
    """
    Format numbers for business display.
    
    Args:
        value: Number to format
        format_type: Type of format ('currency', 'percentage', 'general')
    
    Returns:
        Formatted string
    """
    if format_type == 'currency':
        if abs(value) >= 1000000:
            return f'${value/1000000:,.1f}M'
        elif abs(value) >= 1000:
            return f'${value/1000:,.1f}K'
        else:
            return f'${value:,.2f}'
    elif format_type == 'percentage':
        return f'{value:.1f}%'
    else:
        if abs(value) >= 1000000:
            return f'{value/1000000:,.1f}M'
        elif abs(value) >= 1000:
            return f'{value/1000:,.1f}K'
        else:
            return f'{value:,.1f}'


def create_kpi_card_data(value: float, label: str, format_type: str = 'general') -> Dict:
    """
    Create KPI card data structure.
    
    Args:
        value: KPI value
        label: KPI label
        format_type: Type of format
    
    Returns:
        Dictionary with KPI card data
    """
    return {
        'value': value,
        'formatted_value': format_number(value, format_type),
        'label': label,
        'format_type': format_type
    }


def get_chart_title(data_context: str, analysis_type: str) -> str:
    """
    Generate business chart title.
    
    Args:
        data_context: Context of the data (e.g., 'Employee Utilization')
        analysis_type: Type of analysis (e.g., 'by Department')
    
    Returns:
        Generated chart title
    """
    return f'{data_context} {analysis_type}'


def validate_data_for_visualization(df: pd.DataFrame, required_columns: List[str]) -> Dict:
    """
    Validate data is ready for visualization.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required columns
    
    Returns:
        Dictionary with validation results
    """
    missing_cols = [col for col in required_columns if col not in df.columns]
    
    return {
        'valid': len(missing_cols) == 0,
        'missing_columns': missing_cols,
        'row_count': len(df),
        'column_count': len(df.columns)
    }


def get_business_insights_from_data(df: pd.DataFrame, metric_col: str, group_col: str = None) -> Dict:
    """
    Extract business insights from data for visualization context.
    
    Args:
        df: DataFrame with data
        metric_col: Column with metric values
        group_col: Column to group by (optional)
    
    Returns:
        Dictionary with business insights
    """
    metric_data = pd.to_numeric(df[metric_col], errors='coerce').dropna()
    
    insights = {
        'metric': metric_col,
        'total': round(float(metric_data.sum()), 2),
        'average': round(float(metric_data.mean()), 2),
        'median': round(float(metric_data.median()), 2),
        'std': round(float(metric_data.std()), 2),
        'min': round(float(metric_data.min()), 2),
        'max': round(float(metric_data.max()), 2)
    }
    
    if group_col and group_col in df.columns:
        group_stats = df.groupby(group_col)[metric_col].agg(['sum', 'mean', 'count']).round(2)
        insights['by_group'] = group_stats.to_dict()
    
    return insights