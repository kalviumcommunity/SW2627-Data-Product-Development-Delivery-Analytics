"""
Interactive Plotly Chart Design Module
Provides functions for creating interactive Plotly visualizations.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any


def create_bar_chart(data: pd.DataFrame, x_col: str, y_col: str, title: str = None, color_col: str = None) -> Dict:
    """
    Create bar chart configuration.
    
    Args:
        data: DataFrame with data
        x_col: Column for x-axis
        y_col: Column for y-axis
        title: Chart title
        color_col: Column for color grouping
    
    Returns:
        Dictionary with chart configuration
    """
    return {
        'type': 'bar',
        'x': data[x_col].tolist(),
        'y': data[y_col].tolist(),
        'title': title or f'{y_col} by {x_col}',
        'x_label': x_col,
        'y_label': y_col,
        'color': color_col,
        'color_values': data[color_col].tolist() if color_col else None
    }


def create_line_chart(data: pd.DataFrame, x_col: str, y_col: str, title: str = None, group_col: str = None) -> Dict:
    """
    Create line chart configuration.
    
    Args:
        data: DataFrame with data
        x_col: Column for x-axis
        y_col: Column for y-axis
        title: Chart title
        group_col: Column for group lines
    
    Returns:
        Dictionary with chart configuration
    """
    config = {
        'type': 'line',
        'x': data[x_col].tolist(),
        'y': data[y_col].tolist(),
        'title': title or f'{y_col} over {x_col}',
        'x_label': x_col,
        'y_label': y_col
    }
    
    if group_col and group_col in data.columns:
        groups = data[group_col].unique()
        config['traces'] = []
        for group in groups:
            group_data = data[data[group_col] == group]
            config['traces'].append({
                'name': str(group),
                'x': group_data[x_col].tolist(),
                'y': group_data[y_col].tolist()
            })
    
    return config


def create_pie_chart(data: pd.DataFrame, labels_col: str, values_col: str, title: str = None) -> Dict:
    """
    Create pie chart configuration.
    
    Args:
        data: DataFrame with data
        labels_col: Column for labels
        values_col: Column for values
        title: Chart title
    
    Returns:
        Dictionary with chart configuration
    """
    return {
        'type': 'pie',
        'labels': data[labels_col].tolist(),
        'values': data[values_col].tolist(),
        'title': title or f'{values_col} Distribution'
    }


def create_scatter_chart(data: pd.DataFrame, x_col: str, y_col: str, title: str = None, size_col: str = None, color_col: str = None) -> Dict:
    """
    Create scatter chart configuration.
    
    Args:
        data: DataFrame with data
        x_col: Column for x-axis
        y_col: Column for y-axis
        title: Chart title
        size_col: Column for bubble size
        color_col: Column for color
    
    Returns:
        Dictionary with chart configuration
    """
    config = {
        'type': 'scatter',
        'x': data[x_col].tolist(),
        'y': data[y_col].tolist(),
        'title': title or f'{y_col} vs {x_col}',
        'x_label': x_col,
        'y_label': y_col,
        'mode': 'markers'
    }
    
    if size_col and size_col in data.columns:
        config['size'] = data[size_col].tolist()
    
    if color_col and color_col in data.columns:
        config['color'] = data[color_col].tolist()
    
    return config


def create_histogram(data: pd.DataFrame, col: str, bins: int = 30, title: str = None) -> Dict:
    """
    Create histogram configuration.
    
    Args:
        data: DataFrame with data
        col: Column to histogram
        bins: Number of bins
        title: Chart title
    
    Returns:
        Dictionary with chart configuration
    """
    return {
        'type': 'histogram',
        'x': data[col].tolist(),
        'title': title or f'{col} Distribution',
        'x_label': col,
        'y_label': 'Frequency',
        'nbinsx': bins
    }


def create_box_plot(data: pd.DataFrame, y_col: str, x_col: str = None, title: str = None) -> Dict:
    """
    Create box plot configuration.
    
    Args:
        data: DataFrame with data
        y_col: Column for y-axis
        x_col: Column for x-axis groups
        title: Chart title
    
    Returns:
        Dictionary with chart configuration
    """
    config = {
        'type': 'box',
        'y': data[y_col].tolist(),
        'title': title or f'{y_col} Distribution',
        'y_label': y_col
    }
    
    if x_col and x_col in data.columns:
        config['x'] = data[x_col].tolist()
        config['x_label'] = x_col
    
    return config


def create_heatmap(data: pd.DataFrame, x_col: str, y_col: str, z_col: str, title: str = None) -> Dict:
    """
    Create heatmap configuration.
    
    Args:
        data: DataFrame with data
        x_col: Column for x-axis
        y_col: Column for y-axis
        z_col: Column for values
        title: Chart title
    
    Returns:
        Dictionary with chart configuration
    """
    pivot = data.pivot_table(index=y_col, columns=x_col, values=z_col, aggfunc='mean')
    
    return {
        'type': 'heatmap',
        'x': pivot.columns.tolist(),
        'y': pivot.index.tolist(),
        'z': pivot.values.tolist(),
        'title': title or f'{z_col} Heatmap',
        'x_label': x_col,
        'y_label': y_col
    }


def create_grouped_bar_chart(data: pd.DataFrame, x_col: str, y_col: str, group_col: str, title: str = None) -> Dict:
    """
    Create grouped bar chart configuration.
    
    Args:
        data: DataFrame with data
        x_col: Column for x-axis
        y_col: Column for y-axis
        group_col: Column for grouping
        title: Chart title
    
    Returns:
        Dictionary with chart configuration
    """
    groups = data[group_col].unique()
    traces = []
    
    for group in groups:
        group_data = data[data[group_col] == group]
        traces.append({
            'name': str(group),
            'x': group_data[x_col].tolist(),
            'y': group_data[y_col].tolist()
        })
    
    return {
        'type': 'grouped_bar',
        'traces': traces,
        'title': title or f'{y_col} by {x_col} and {group_col}',
        'x_label': x_col,
        'y_label': y_col
    }


def get_chart_recommendations(data: pd.DataFrame, metric_col: str, category_col: str = None) -> List[Dict]:
    """
    Get chart recommendations for data.
    
    Args:
        data: DataFrame with data
        metric_col: Column with metric values
        category_col: Column with categories
    
    Returns:
        List of chart recommendations
    """
    recommendations = []
    
    if category_col:
        recommendations.append({
            'chart_type': 'bar',
            'description': f'Compare {metric_col} across {category_col}',
            'config': create_bar_chart(data.groupby(category_col).agg({metric_col: 'sum'}).reset_index(), category_col, metric_col)
        })
        
        recommendations.append({
            'chart_type': 'pie',
            'description': f'Show {metric_col} composition by {category_col}',
            'config': create_pie_chart(data.groupby(category_col).agg({metric_col: 'sum'}).reset_index(), category_col, metric_col)
        })
    
    recommendations.append({
        'chart_type': 'histogram',
        'description': f'Distribution of {metric_col}',
        'config': create_histogram(data, metric_col)
    })
    
    recommendations.append({
        'chart_type': 'box',
        'description': f'Box plot of {metric_col}',
        'config': create_box_plot(data, metric_col)
    })
    
    return recommendations