"""
Time-Series Trend & Rolling Metrics Module
Provides functions for time-series analysis and rolling metrics.
"""

import pandas as pd
import numpy as np


def parse_date_column(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    """
    Parse date column to datetime.
    
    Args:
        df: pandas DataFrame
        date_column: Name of date column
    
    Returns:
        DataFrame with parsed date column
    """
    df = df.copy()
    if date_column in df.columns:
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    return df


def set_time_index(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    """
    Set date column as index and sort.
    
    Args:
        df: pandas DataFrame
        date_column: Name of date column
    
    Returns:
        DataFrame with datetime index
    """
    df = parse_date_column(df, date_column)
    if date_column in df.columns:
        df = df.set_index(date_column).sort_index()
    return df


def calculate_rolling_mean(df: pd.DataFrame, value_column: str, window: int = 7) -> pd.Series:
    """
    Calculate rolling mean.
    
    Args:
        df: pandas DataFrame with datetime index
        value_column: Column to calculate rolling mean
        window: Rolling window size
    
    Returns:
        Series with rolling mean
    """
    if value_column in df.columns:
        return df[value_column].rolling(window=window, min_periods=1).mean()
    return pd.Series()


def calculate_rolling_std(df: pd.DataFrame, value_column: str, window: int = 7) -> pd.Series:
    """
    Calculate rolling standard deviation.
    
    Args:
        df: pandas DataFrame with datetime index
        value_column: Column to calculate rolling std
        window: Rolling window size
    
    Returns:
        Series with rolling std
    """
    if value_column in df.columns:
        return df[value_column].rolling(window=window, min_periods=1).std()
    return pd.Series()


def calculate_rolling_sum(df: pd.DataFrame, value_column: str, window: int = 7) -> pd.Series:
    """
    Calculate rolling sum.
    
    Args:
        df: pandas DataFrame with datetime index
        value_column: Column to calculate rolling sum
        window: Rolling window size
    
    Returns:
        Series with rolling sum
    """
    if value_column in df.columns:
        return df[value_column].rolling(window=window, min_periods=1).sum()
    return pd.Series()


def calculate_ewm(df: pd.DataFrame, value_column: str, span: int = 7) -> pd.Series:
    """
    Calculate exponential weighted moving average.
    
    Args:
        df: pandas DataFrame with datetime index
        value_column: Column to calculate EWM
        span: Span for EWM
    
    Returns:
        Series with EWM
    """
    if value_column in df.columns:
        return df[value_column].ewm(span=span, adjust=False).mean()
    return pd.Series()


def resample_time_series(df: pd.DataFrame, value_column: str, freq: str = 'D', agg_func: str = 'sum') -> pd.Series:
    """
    Resample time series to different frequency.
    
    Args:
        df: pandas DataFrame with datetime index
        value_column: Column to resample
        freq: Resample frequency ('D', 'W', 'M', 'Q')
        agg_func: Aggregation function ('sum', 'mean', 'count')
    
    Returns:
        Resampled Series
    """
    if value_column in df.columns:
        return getattr(df[value_column].resample(freq), agg_func)()
    return pd.Series()


def calculate_monthly_trend(df: pd.DataFrame, value_column: str, date_column: str = None) -> pd.DataFrame:
    """
    Calculate monthly trend with statistics.
    
    Args:
        df: pandas DataFrame
        value_column: Column to analyze
        date_column: Date column (if not index)
    
    Returns:
        DataFrame with monthly statistics
    """
    df = df.copy()
    if date_column and date_column in df.columns:
        df = set_time_index(df, date_column)
    elif not isinstance(df.index, pd.DatetimeIndex):
        return pd.DataFrame()
    
    monthly = df[value_column].resample('ME').agg(['sum', 'mean', 'count', 'std', 'min', 'max']).round(2)
    monthly.columns = ['total', 'avg', 'count', 'std', 'min', 'max']
    
    # Add month-over-month change
    monthly['mom_change_pct'] = monthly['total'].pct_change() * 100
    
    return monthly


def calculate_weekly_trend(df: pd.DataFrame, value_column: str, date_column: str = None) -> pd.DataFrame:
    """
    Calculate weekly trend with statistics.
    
    Args:
        df: pandas DataFrame
        value_column: Column to analyze
        date_column: Date column (if not index)
    
    Returns:
        DataFrame with weekly statistics
    """
    df = df.copy()
    if date_column and date_column in df.columns:
        df = set_time_index(df, date_column)
    elif not isinstance(df.index, pd.DatetimeIndex):
        return pd.DataFrame()
    
    weekly = df[value_column].resample('W').agg(['sum', 'mean', 'count', 'std', 'min', 'max']).round(2)
    weekly.columns = ['total', 'avg', 'count', 'std', 'min', 'max']
    
    weekly['wow_change_pct'] = weekly['total'].pct_change() * 100
    
    return weekly


def detect_trend_direction(series: pd.Series) -> str:
    """
    Detect trend direction using linear regression slope.
    
    Args:
        series: Time series data
    
    Returns:
        Trend direction ('increasing', 'decreasing', 'stable')
    """
    if len(series) < 2:
        return 'stable'
    
    x = np.arange(len(series))
    y = series.dropna().values
    
    if len(y) < 2:
        return 'stable'
    
    slope = np.polyfit(x[:len(y)], y, 1)[0]
    
    if slope > 0.01:
        return 'increasing'
    elif slope < -0.01:
        return 'decreasing'
    return 'stable'


def calculate_seasonal_decomposition(df: pd.DataFrame, value_column: str, date_column: str = None, period: int = 7) -> dict:
    """
    Calculate simple seasonal decomposition.
    
    Args:
        df: pandas DataFrame
        value_column: Column to decompose
        date_column: Date column (if not index)
        period: Seasonal period
    
    Returns:
        Dictionary with trend, seasonal, residual
    """
    df = df.copy()
    if date_column and date_column in df.columns:
        df = set_time_index(df, date_column)
    elif not isinstance(df.index, pd.DatetimeIndex):
        return {}
    
    series = df[value_column].dropna()
    
    if len(series) < period * 2:
        return {}
    
    # Simple moving average for trend
    trend = series.rolling(window=period, center=True, min_periods=1).mean()
    
    # Detrended
    detrended = series - trend
    
    # Seasonal (average for each period position)
    seasonal_idx = np.arange(len(detrended)) % period
    seasonal = detrended.groupby(seasonal_idx).transform('mean')
    
    # Residual
    residual = detrended - seasonal
    
    return {
        'trend': trend,
        'seasonal': seasonal,
        'residual': residual
    }


def get_time_series_summary(df: pd.DataFrame, date_column: str, value_column: str) -> dict:
    """
    Get comprehensive time series summary.
    
    Args:
        df: pandas DataFrame
        date_column: Date column name
        value_column: Value column name
    
    Returns:
        Dictionary with time series summary
    """
    df = set_time_index(df, date_column)
    
    if date_column not in df.columns and not isinstance(df.index, pd.DatetimeIndex):
        return {'error': 'No valid date column'}
    
    series = df[value_column].dropna() if value_column in df.columns else pd.Series()
    
    return {
        'date_range': {
            'start': str(df.index.min()) if len(df) > 0 else None,
            'end': str(df.index.max()) if len(df) > 0 else None
        },
        'total_points': len(series),
        'missing_count': df[value_column].isna().sum() if value_column in df.columns else 0,
        'value_stats': {
            'mean': series.mean(),
            'std': series.std(),
            'min': series.min(),
            'max': series.max()
        },
        'trend_direction': detect_trend_direction(series)
    }