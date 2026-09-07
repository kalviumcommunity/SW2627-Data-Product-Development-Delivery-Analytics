"""Data handler for Streamlit dashboard — file upload, caching, and session state."""

from __future__ import annotations

import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def _read_csv(uploaded_file) -> pd.DataFrame:
    """Read CSV from UploadedFile object (cached)."""
    return pd.read_csv(uploaded_file)


@st.cache_data(show_spinner=False)
def _read_json(uploaded_file) -> pd.DataFrame:
    """Read JSON from UploadedFile object (cached)."""
    return pd.read_json(uploaded_file)


def load_uploaded_file(uploaded_file) -> pd.DataFrame | None:
    """Load an uploaded CSV or JSON file into a DataFrame.

    Args:
        uploaded_file: Streamlit UploadedFile object.

    Returns:
        DataFrame or None if file cannot be parsed.
    """
    if uploaded_file is None:
        return None

    try:
        name = uploaded_file.name.lower()
        if name.endswith(".csv"):
            return _read_csv(uploaded_file)
        elif name.endswith(".json"):
            return _read_json(uploaded_file)
        else:
            return None
    except Exception:
        return None


def get_dataset_summary(df: pd.DataFrame) -> dict:
    """Return a summary dict for the given DataFrame.

    Args:
        df: The dataset to summarise.

    Returns:
        Dictionary with rows, columns, null info, dtypes, and basic stats.
    """
    total_cells = df.shape[0] * df.shape[1]
    null_cells = int(df.isnull().sum().sum())
    null_pct = round((null_cells / total_cells) * 100, 2) if total_cells > 0 else 0

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "null_cells": null_cells,
        "null_pct": null_pct,
        "dtypes": df.dtypes.value_counts().to_dict(),
        "memory_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
    }


def initialise_session_state() -> None:
    """Set default session state keys if not already present."""
    defaults = {
        "active_page": "overview",
        "period": "This Month",
        "uploaded_df": None,
        "file_name": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def reset_session_state() -> None:
    """Reset all dashboard session state to defaults (for Reset button)."""
    st.session_state["active_page"] = "overview"
    st.session_state["period"] = "This Month"
    st.session_state["uploaded_df"] = None
    st.session_state["file_name"] = None
    if "nav_radio" in st.session_state:
        del st.session_state["nav_radio"]
    if "period_selector" in st.session_state:
        del st.session_state["period_selector"]
