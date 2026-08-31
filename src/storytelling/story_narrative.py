"""
Data Storytelling & Insight Narrative Module
Provides functions for creating compelling data stories and insight narratives.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional


def generate_insight_narrative(df: pd.DataFrame, metric_col: str, group_col: str = None) -> str:
    """
    Generate a comprehensive insight narrative from data.
    
    Args:
        df: DataFrame with data
        metric_col: Column with metric values
        group_col: Column to group by (optional)
    
    Returns:
        String with formatted insight narrative
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
    if count > 1:
        first_half = metric_data.iloc[:len(metric_data)//2].mean()
        second_half = metric_data.iloc[len(metric_data)//2:].mean()
        trend = 'IMPROVING' if second_half > first_half else 'DECLINING' if second_half < first_half else 'STABLE'
    else:
        trend = 'INSUFFICIENT DATA'
    
    # Build narrative
    narrative = f"""
Data Story: {metric_col} Analysis

Key Metrics:
- Total: {total:,.2f}
- Average: {average:,.2f}
- Median: {median:,.2f}
- Range: {minimum:,.2f} to {maximum:,.2f}
- Standard Deviation: {std_dev:,.2f}
- Sample Size: {count:,}

Distribution Analysis:
- The data shows {maximum - minimum:,.2f} units of variation.
- Most values cluster around the median of {median:,.2f}.
- {count:,} data points were analyzed.

Trend Analysis:
- Overall trend: {trend}
- The {trend.lower()} trend suggests {'positive momentum' if trend == 'IMPROVING' else 'areas for improvement'}.

Key Insights:
- High performers exceed {maximum:,.2f}, indicating {'significant achievement' if maximum > average * 1.5 else 'potential outliers'}.
- Low performers fall below {minimum:,.2f}, suggesting {'underperformance that needs attention' if minimum < average * 0.5 else 'consistent performance'}.
"""
    
    return narrative.strip()


def create_story_structure(title: str, sections: List[str], conclusion: str) -> Dict:
    """
    Create a story structure for data presentations.
    
    Args:
        title: Story title
        sections: List of section titles
        conclusion: Conclusion text
    
    Returns:
        Dictionary with story structure
    """
    return {
        'title': title,
        'sections': sections,
        'conclusion': conclusion,
        'total_sections': len(sections),
        'has_conclusion': conclusion is not None and len(str(conclusion)) > 0
    }


def get_business_context(metric_name: str, industry: str = 'General') -> str:
    """
    Get business context for a metric.
    
    Args:
        metric_name: Name of the metric
        industry: Industry context
    
    Returns:
        Business context string
    """
    contexts = {
        'utilization': f'In {industry}, utilization rate measures the percentage of available billable hours that are actually utilized. Typical rates range from 60-80% for healthy operations.',
        'revenue': f'In {industry}, revenue represents the total income generated from services or products. Growth trends indicate market demand and operational efficiency.',
        'allocation': f'In {industry}, allocation efficiency measures how effectively resources are deployed against planned objectives. Efficiency above 80% is typically considered optimal.',
        'default': f'The {metric_name} metric provides insights into business performance and operational effectiveness.'
    }
    
    return contexts.get(metric_name.lower(), contexts['default'])


def validate_story_data(df: pd.DataFrame, required_columns: List[str], min_rows: int = 5) -> Dict:
    """
    Validate data quality for storytelling.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required columns
        min_rows: Minimum number of rows required
    
    Returns:
        Dictionary with validation results
    """
    missing = [col for col in required_columns if col not in df.columns]
    null_count = df[required_columns].isnull().sum().sum() if all(col in df.columns for col in required_columns) else 0
    row_count = len(df)
    
    return {
        'valid': len(missing) == 0 and row_count >= min_rows,
        'missing_columns': missing,
        'null_count': int(null_count),
        'row_count': row_count,
        'meets_minimum': row_count >= min_rows,
        'data_quality_score': round(max(0, 100 - (len(missing) * 10 + int(null_count) * 2)), 2)
    }


def extract_key_insights(df: pd.DataFrame, metric_col: str, group_col: str = None, top_n: int = 3) -> List[Dict]:
    """
    Extract key insights from data for storytelling.
    
    Args:
        df: DataFrame with data
        metric_col: Column with metric values
        group_col: Column to group by
        top_n: Number of top insights to extract
    
    Returns:
        List of insight dictionaries
    """
    metric_data = pd.to_numeric(df[metric_col], errors='coerce').dropna()
    
    insights = []
    
    if group_col and group_col in df.columns:
        grouped = df.groupby(group_col).size().sort_values(ascending=False)
        sorted_groups = grouped.head(top_n)
        
        for i, (group, count) in enumerate(sorted_groups.items()):
            insights.append({
                'rank': i + 1,
                'group': str(group),
                'value': int(count),
                'insight': f'{group} has {int(count)} records {"above" if int(count) > len(metric_data) / 3 else "below"} average activity',
                'rank_change': '' if i == 0 else f'Rank {i+1}'
            })
    else:
        sorted_data = metric_data.sort_values(ascending=False).head(top_n)
        for i, value in enumerate(sorted_data.items()):
            insights.append({
                'rank': i + 1,
                'value': round(float(value[1]), 2),
                'insight': f'Top value: {float(value[1]):.2f}'
            })
    
    return insights


def format_narrative_text(text: str, max_length: int = None) -> str:
    """
    Format narrative text for presentation.
    
    Args:
        text: Narrative text
        max_length: Maximum length in characters
    
    Returns:
        Formatted narrative text
    """
    if max_length and len(text) > max_length:
        text = text[:max_length] + '...'
    
    # Clean up whitespace
    text = ' '.join(text.split())
    
    return text


def get_storytelling_recommendations(df: pd.DataFrame, metric_col: str, group_col: str = None) -> Dict:
    """
    Get storytelling recommendations based on data.
    
    Args:
        df: DataFrame with data
        metric_col: Column with metric values
        group_col: Column to group by
    
    Returns:
        Dictionary with recommendations
    """
    return {
        'has_trend': len(df) > 1,
        'has_groups': group_col and group_col in df.columns,
        'recommended_structure': 'problem-solution-result' if len(df) > 10 else 'key-insights',
        'suggested_visualizations': ['bar', 'line', 'pie'] if group_col else ['bar', 'pie'],
        'key_message': f'{metric_col} performance {"varies across groups" if group_col else "shows overall trend"}'
    }