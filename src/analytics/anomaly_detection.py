"""
Anomaly Detection & Risk Identification Module
Provides functions for detecting outliers and identifying risks in employee data.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional


def detect_outliers_iqr(series: pd.Series, multiplier: float = 1.5) -> pd.Series:
    """
    Detect outliers using IQR method.
    
    Args:
        series: Numeric series to analyze
        multiplier: IQR multiplier (default 1.5)
    
    Returns:
        Boolean series where True indicates outlier
    """
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - (iqr * multiplier)
    upper_bound = q3 + (iqr * multiplier)
    return (series < lower_bound) | (series > upper_bound)


def detect_outliers_zscore(series: pd.Series, threshold: float = 3.0) -> pd.Series:
    """
    Detect outliers using Z-score method.
    
    Args:
        series: Numeric series to analyze
        threshold: Z-score threshold (default 3.0)
    
    Returns:
        Boolean series where True indicates outlier
    """
    mean = series.mean()
    std = series.std()
    z_scores = np.abs((series - mean) / std)
    return z_scores > threshold


def detect_anomalies(df: pd.DataFrame, columns: List[str] = None, method: str = 'iqr') -> Dict:
    """
    Detect anomalies across multiple columns.
    
    Args:
        df: DataFrame to analyze
        columns: Columns to check (None for numeric columns)
        method: Detection method ('iqr' or 'zscore')
    
    Returns:
        Dictionary with anomaly detection results
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    results = {
        'total_rows': len(df),
        'columns_analyzed': columns,
        'anomalies': {}
    }
    
    for col in columns:
        if col not in df.columns:
            continue
        
        series = df[col].dropna()
        if len(series) == 0:
            continue
        
        if method == 'iqr':
            outliers = detect_outliers_iqr(series)
        else:
            outliers = detect_outliers_zscore(series)
        
        results['anomalies'][col] = {
            'count': int(outliers.sum()),
            'percentage': round(outliers.sum() / len(series) * 100, 2),
            'indices': outliers[outliers].index.tolist()[:10]
        }
    
    return results


def detect_utilization_anomalies(df: pd.DataFrame) -> Dict:
    """
    Detect anomalies in utilization-related metrics.
    
    Args:
        df: DataFrame with utilization data
    
    Returns:
        Dictionary with utilization anomaly results
    """
    results = {}
    
    if 'billable_hours' in df.columns:
        outliers = detect_outliers_iqr(df['billable_hours'])
        results['billable_hours'] = {
            'outlier_count': int(outliers.sum()),
            'percentage': round(outliers.sum() / len(df) * 100, 2)
        }
    
    if 'non_billable_hours' in df.columns:
        outliers = detect_outliers_iqr(df['non_billable_hours'])
        results['non_billable_hours'] = {
            'outlier_count': int(outliers.sum()),
            'percentage': round(outliers.sum() / len(df) * 100, 2)
        }
    
    if 'overtime_hours' in df.columns:
        outliers = detect_outliers_iqr(df['overtime_hours'])
        results['overtime_hours'] = {
            'outlier_count': int(outliers.sum()),
            'percentage': round(outliers.sum() / len(df) * 100, 2)
        }
    
    return results


def calculate_risk_score(row: pd.Series) -> float:
    """
    Calculate risk score for a single record.
    
    Args:
        row: DataFrame row to score
    
    Returns:
        Risk score (0-100)
    """
    score = 0
    
    if 'billable_hours' in row.index and row['billable_hours'] < 20:
        score += 25
    if 'non_billable_hours' in row.index and row['non_billable_hours'] > 30:
        score += 20
    if 'overtime_hours' in row.index and row['overtime_hours'] > 20:
        score += 15
    if 'kpi_billable_utilization_rate' in row.index and row['kpi_billable_utilization_rate'] < 60:
        score += 30
    if 'kpi_writeoff_rate' in row.index and row['kpi_writeoff_rate'] > 10:
        score += 10
    
    return min(score, 100)


def calculate_risk_scores(df: pd.DataFrame) -> pd.Series:
    """
    Calculate risk scores for all records.
    
    Args:
        df: DataFrame with risk-related columns
    
    Returns:
        Series with risk scores
    """
    return df.apply(calculate_risk_score, axis=1)


def identify_high_risk_records(df: pd.DataFrame, threshold: float = 60) -> pd.DataFrame:
    """
    Identify records with high risk scores.
    
    Args:
        df: DataFrame with risk-related columns
        threshold: Risk score threshold (default 60)
    
    Returns:
        DataFrame with high-risk records
    """
    df = df.copy()
    df['risk_score'] = calculate_risk_scores(df)
    return df[df['risk_score'] >= threshold]


def classify_risk_level(score: float) -> str:
    """
    Classify risk level based on score.
    
    Args:
        score: Risk score (0-100)
    
    Returns:
        Risk level string
    """
    if score >= 80:
        return 'CRITICAL'
    elif score >= 60:
        return 'HIGH'
    elif score >= 40:
        return 'MEDIUM'
    elif score >= 20:
        return 'LOW'
    else:
        return 'MINIMAL'


def get_risk_summary(df: pd.DataFrame) -> Dict:
    """
    Generate risk summary for the dataset.
    
    Args:
        df: DataFrame with risk-related columns
    
    Returns:
        Dictionary with risk summary
    """
    df = df.copy()
    df['risk_score'] = calculate_risk_scores(df)
    
    summary = {
        'total_records': len(df),
        'avg_risk_score': round(df['risk_score'].mean(), 2),
        'max_risk_score': round(df['risk_score'].max(), 2),
        'high_risk_count': int((df['risk_score'] >= 60).sum()),
        'critical_risk_count': int((df['risk_score'] >= 80).sum()),
        'risk_distribution': {
            'CRITICAL': int((df['risk_score'] >= 80).sum()),
            'HIGH': int(((df['risk_score'] >= 60) & (df['risk_score'] < 80)).sum()),
            'MEDIUM': int(((df['risk_score'] >= 40) & (df['risk_score'] < 60)).sum()),
            'LOW': int(((df['risk_score'] >= 20) & (df['risk_score'] < 40)).sum()),
            'MINIMAL': int((df['risk_score'] < 20).sum())
        }
    }
    
    return summary