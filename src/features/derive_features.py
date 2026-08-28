"""
Feature Engineering & Derived Business Columns Module
Provides functions for creating derived business metrics.
"""

import pandas as pd
import numpy as np


def calculate_utilization_rate(billable_hours: pd.Series, total_hours: pd.Series) -> pd.Series:
    """
    Calculate utilization rate from billable and total hours.
    
    Args:
        billable_hours: Series of billable hours
        total_hours: Series of total hours
    
    Returns:
        Series of utilization rates (0-100)
    """
    # Avoid division by zero
    result = np.where(total_hours > 0, (billable_hours / total_hours) * 100, 0)
    return pd.Series(result, index=billable_hours.index)


def calculate_allocation_variance(actual_hours: pd.Series, allocated_hours: pd.Series) -> pd.Series:
    """
    Calculate allocation variance between actual and allocated hours.
    
    Args:
        actual_hours: Series of actual hours worked
        allocated_hours: Series of allocated hours
    
    Returns:
        Series of allocation variance percentages
    """
    # Avoid division by zero
    result = np.where(allocated_hours > 0, ((actual_hours - allocated_hours) / allocated_hours) * 100, 0)
    return pd.Series(result, index=actual_hours.index)


def create_efficiency_score(df: pd.DataFrame) -> pd.Series:
    """
    Create efficiency score based on multiple factors.
    
    Args:
        df: DataFrame with required columns
    
    Returns:
        Series of efficiency scores (0-100)
    """
    score = pd.Series(0.0, index=df.index)
    weights = 0
    
    if 'billable_hours' in df.columns and 'total_hours' in df.columns:
        util_rate = calculate_utilization_rate(df['billable_hours'], df['total_hours'])
        score += util_rate * 0.4
        weights += 0.4
    
    if 'hours_worked' in df.columns and 'allocated_hours' in df.columns:
        alloc_var = calculate_allocation_variance(df['hours_worked'], df['allocated_hours'])
        # Convert variance to score (lower variance = higher score)
        alloc_score = 100 - abs(alloc_var)
        score += alloc_score * 0.3
        weights += 0.3
    
    if 'approval_status' in df.columns:
        # Approval rate as proxy for quality
        approval_rate = (df['approval_status'] == 'Approved').astype(float) * 100
        score += approval_rate * 0.3
        weights += 0.3
    
    # Normalize to 0-100
    if weights > 0:
        score = score / weights
    
    return score


def create_risk_flags(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create risk flags for identifying potential issues.
    
    Args:
        df: DataFrame with required columns
    
    Returns:
        DataFrame with risk flag columns added
    """
    df = df.copy()
    
    # Low utilization flag
    if 'billable_hours' in df.columns and 'total_hours' in df.columns:
        util_rate = calculate_utilization_rate(df['billable_hours'], df['total_hours'])
        df['flag_low_utilization'] = util_rate < 60
    
    # Over allocation flag
    if 'hours_worked' in df.columns and 'allocated_hours' in df.columns:
        alloc_var = calculate_allocation_variance(df['hours_worked'], df['allocated_hours'])
        df['flag_over_allocation'] = alloc_var > 20
    
    # Under allocation flag
    if 'hours_worked' in df.columns and 'allocated_hours' in df.columns:
        alloc_var = calculate_allocation_variance(df['hours_worked'], df['allocated_hours'])
        df['flag_under_allocation'] = alloc_var < -20
    
    # Missing timesheet flag
    if 'hours_worked' in df.columns:
        df['flag_missing_timesheet'] = df['hours_worked'].isna()
    
    # Negative hours flag
    if 'hours_worked' in df.columns:
        df['flag_negative_hours'] = df['hours_worked'] < 0
    
    return df


def segment_by_experience(years: pd.Series) -> pd.Series:
    """
    Segment employees by years of experience.
    
    Args:
        years: Series of years of experience
    
    Returns:
        Series of experience segments
    """
    conditions = [
        years <= 2,
        (years > 2) & (years <= 5),
        (years > 5) & (years <= 10),
        (years > 10) & (years <= 15),
        years > 15
    ]
    choices = ['Junior', 'Mid-Level', 'Senior', 'Lead', 'Principal']
    
    return pd.Series(np.select(conditions, choices, default='Unknown'), index=years.index)


def calculate_revenue_per_hour(billed_amount: pd.Series, billable_hours: pd.Series) -> pd.Series:
    """
    Calculate revenue per billable hour.
    
    Args:
        billed_amount: Series of billed amounts
        billable_hours: Series of billable hours
    
    Returns:
        Series of revenue per hour
    """
    # Avoid division by zero
    result = np.where(billable_hours > 0, billed_amount / billable_hours, 0)
    return pd.Series(result, index=billed_amount.index)


def create_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create all derived columns for analytics.
    
    Args:
        df: DataFrame with raw data
    
    Returns:
        DataFrame with derived columns added
    """
    df = df.copy()
    
    # Utilization rate
    if 'billable_hours' in df.columns and 'total_hours' in df.columns:
        df['utilization_rate'] = calculate_utilization_rate(df['billable_hours'], df['total_hours'])
    
    # Allocation variance
    if 'hours_worked' in df.columns and 'allocated_hours' in df.columns:
        df['allocation_variance'] = calculate_allocation_variance(df['hours_worked'], df['allocated_hours'])
    
    # Efficiency score
    df['efficiency_score'] = create_efficiency_score(df)
    
    # Revenue per hour
    if 'billed_amount' in df.columns and 'billable_hours' in df.columns:
        df['revenue_per_hour'] = calculate_revenue_per_hour(df['billed_amount'], df['billable_hours'])
    
    # Experience segment
    if 'years_of_experience' in df.columns:
        df['experience_segment'] = segment_by_experience(df['years_of_experience'])
    
    # Risk flags
    df = create_risk_flags(df)
    
    return df


def get_feature_summary(df: pd.DataFrame) -> dict:
    """
    Get summary of engineered features.
    
    Args:
        df: DataFrame with engineered features
    
    Returns:
        Dictionary with feature summary
    """
    summary = {
        'total_features': len(df.columns),
        'new_features': [col for col in df.columns if col.startswith(('utilization_', 'allocation_', 'efficiency_', 'revenue_', 'experience_', 'flag_'))]
    }
    
    # Calculate statistics for numeric features
    for col in summary['new_features']:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            summary[col] = {
                'mean': df[col].mean(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max()
            }
    
    return summary
