"""Data handler for Streamlit dashboard — file upload, caching, and session state."""

from __future__ import annotations

import pandas as pd
import streamlit as st


# ---------------------------------------------------------------------------
# File loading
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# Dataset summary
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# Dynamic KPI calculation
# ---------------------------------------------------------------------------
def _safe_col(df: pd.DataFrame, col: str) -> pd.Series | None:
    """Return a column as Series if it exists, else None."""
    return df[col] if col in df.columns else None


def calculate_kpis(df: pd.DataFrame) -> dict:
    """Calculate KPIs dynamically from the uploaded DataFrame.

    Supports multiple dataset types:
    - Employee master data
    - Timesheet data
    - Allocation data
    - Generic data (fallback to row/column counts)

    Returns:
        Dictionary with KPI label, value, icon, delta, and icon_color.
    """
    kpis = []

    # ── Generic KPIs (always shown) ────────────────────────────────────
    kpis.append({
        "label": "Total Records",
        "value": f"{df.shape[0]:,}",
        "icon": "\U0001f4ca",
        "delta": None,
        "icon_color": None,
    })

    kpis.append({
        "label": "Columns",
        "value": str(df.shape[1]),
        "icon": "\U0001f4c8",
        "delta": None,
        "icon_color": None,
    })

    # ── Employee-specific KPIs ─────────────────────────────────────────
    emp_col = _safe_col(df, "employee_id")
    if emp_col is not None:
        unique_employees = emp_col.nunique()
        kpis.append({
            "label": "Total Employees",
            "value": f"{unique_employees:,}",
            "icon": "\U0001f465",
            "delta": None,
            "icon_color": None,
        })

    # Department count
    dept_col = _safe_col(df, "department")
    if dept_col is not None:
        dept_count = dept_col.nunique()
        kpis.append({
            "label": "Departments",
            "value": str(dept_count),
            "icon": "\U0001f3e2",
            "delta": None,
            "icon_color": None,
        })

    # ── Timesheet-specific KPIs ────────────────────────────────────────
    hours_col = _safe_col(df, "hours_logged")
    billable_col = _safe_col(df, "billable_hours")

    if hours_col is not None:
        total_hours = hours_col.sum()
        kpis.append({
            "label": "Total Hours",
            "value": f"{total_hours:,.0f} hrs",
            "icon": "\U0001f551",
            "delta": None,
            "icon_color": None,
        })

    if billable_col is not None:
        total_billable = billable_col.sum()
        kpis.append({
            "label": "Billable Hours",
            "value": f"{total_billable:,.0f} hrs",
            "icon": "\U0001f512",
            "delta": None,
            "icon_color": None,
        })

        # Utilization rate
        if hours_col is not None:
            util_rate = (total_billable / total_hours * 100) if total_hours > 0 else 0
            color = "\U0001f7e2" if util_rate >= 70 else "\U0001f534"
            kpis.append({
                "label": "Utilization Rate",
                "value": f"{util_rate:.1f}%",
                "icon": "\U0001f4c8",
                "delta": None,
                "icon_color": None,
            })

    # ── Allocation-specific KPIs ───────────────────────────────────────
    alloc_hours_col = _safe_col(df, "allocated_hours")
    if alloc_hours_col is not None:
        total_alloc = alloc_hours_col.sum()
        kpis.append({
            "label": "Allocated Hours",
            "value": f"{total_alloc:,.0f} hrs",
            "icon": "\u26a1",
            "delta": None,
            "icon_color": None,
        })

    # ── Capacity KPI ───────────────────────────────────────────────────
    capacity_col = _safe_col(df, "capacity_hours_monthly")
    if capacity_col is not None:
        total_capacity = capacity_col.sum()
        kpis.append({
            "label": "Monthly Capacity",
            "value": f"{total_capacity:,.0f} hrs",
            "icon": "\U0001f4aa",
            "delta": None,
            "icon_color": None,
        })

    # ── At-risk / Overloaded ───────────────────────────────────────────
    status_col = _safe_col(df, "employment_status")
    if status_col is not None:
        active = (status_col == "Active").sum()
        inactive = df.shape[0] - active
        kpis.append({
            "label": "Active Employees",
            "value": f"{active:,}",
            "icon": "\u2705",
            "delta": None,
            "icon_color": None,
        })
        if inactive > 0:
            kpis.append({
                "label": "Inactive",
                "value": f"{inactive:,}",
                "icon": "\u26a0\ufe0f",
                "delta": None,
                "icon_color": "accent_red",
            })

    # Ensure we always have exactly 6 KPIs (pad or trim)
    while len(kpis) < 6:
        kpis.append({
            "label": "N/A",
            "value": "--",
            "icon": "\u2753",
            "delta": None,
            "icon_color": None,
        })
    kpis = kpis[:6]

    return {
        "kpis": kpis,
        "summary": get_dataset_summary(df),
    }


def get_chart_data(df: pd.DataFrame) -> dict:
    """Extract data for charts based on available columns.

    Returns:
        Dictionary with chart-ready dataframes/series.
    """
    charts = {}

    # ── Department distribution ────────────────────────────────────────
    dept_col = _safe_col(df, "department")
    if dept_col is not None:
        charts["department_dist"] = dept_col.value_counts().head(10)

    # ── Hours by category (timesheet) ─────────────────────────────────
    cat_col = _safe_col(df, "task_category")
    hours_col = _safe_col(df, "hours_logged")
    if cat_col is not None and hours_col is not None:
        charts["hours_by_category"] = df.groupby(cat_col)[hours_col].sum().sort_values(ascending=False).head(8)

    # ── Utilization by department ──────────────────────────────────────
    dept_col2 = _safe_col(df, "department")
    billable_col = _safe_col(df, "billable_hours")
    hours_col2 = _safe_col(df, "hours_logged")
    if dept_col2 is not None and billable_col is not None and hours_col2 is not None:
        dept_util = df.groupby(dept_col2).agg({billable_col: "sum", hours_col2: "sum"})
        dept_util["utilization"] = (dept_util[billable_col] / dept_util[hours_col2] * 100).round(1)
        charts["utilization_by_dept"] = dept_util["utilization"].sort_values(ascending=False)

    # ── Experience distribution ────────────────────────────────────────
    exp_col = _safe_col(df, "experience_years")
    if exp_col is not None:
        charts["experience_dist"] = exp_col.value_counts().sort_index()

    # ── Top projects by hours ──────────────────────────────────────────
    proj_col = _safe_col(df, "project_id")
    hours_col3 = _safe_col(df, "hours_logged")
    if proj_col is not None and hours_col3 is not None:
        charts["top_projects"] = df.groupby(proj_col)[hours_col3].sum().sort_values(ascending=False).head(8)

    return charts


# ---------------------------------------------------------------------------
# Session state management
# ---------------------------------------------------------------------------
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
