"""Data handler for Streamlit dashboard — file upload, caching, and session state."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.database import connection


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


def _numeric_col(df: pd.DataFrame, col: str) -> pd.Series | None:
    """Return a numeric version of a column, tolerating formatted strings."""
    series = _safe_col(df, col)
    if series is None:
        return None
    return pd.to_numeric(
        series.astype("string").str.replace(",", "", regex=False).str.extract(r"([-+]?\d*\.?\d+)", expand=False),
        errors="coerce",
    ).fillna(0)


def load_database_files() -> dict[str, pd.DataFrame]:
    """Load refreshed analytics source tables for dashboard use."""
    table_files = {
        "employee_source": "employee_master_raw.csv",
        "timesheets": "timesheets_raw.csv",
        "allocations": "allocations_raw.csv",
        "billing": "billing_raw.csv",
    }
    try:
        with connection() as conn:
            available = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
            return {
                filename: pd.read_sql_query(f"SELECT * FROM {table}", conn)
                for table, filename in table_files.items()
                if table in available
            }
    except Exception:
        return {}
def filter_dataset(
    df: pd.DataFrame,
    period: str = "This Month",
    search: str = "",
    start_date=None,
    end_date=None,
) -> pd.DataFrame:
    """Filter a dataset by the selected period and a case-insensitive search."""
    filtered = df.copy()

    if search.strip():
        query = search.strip().casefold()
        text_values = filtered.astype("string").fillna("")
        matches = text_values.apply(
            lambda column: column.str.casefold().str.contains(query, regex=False, na=False)
        ).any(axis=1)
        filtered = filtered.loc[matches]

    date_column = next(
        (name for name in ("work_date", "date", "timesheet_date", "entry_date", "allocation_start_date", "billing_date") if name in filtered.columns),
        None,
    )
    if date_column is None:
        return filtered

    parsed_dates = pd.to_datetime(filtered[date_column], errors="coerce")
    if parsed_dates.notna().sum() == 0:
        return filtered

    if period == "Custom" and start_date and end_date:
        start = pd.Timestamp(start_date)
        end = pd.Timestamp(end_date) + pd.Timedelta(days=1)
        return filtered.loc[parsed_dates.between(start, end, inclusive="left").fillna(False)]

    if period not in {"This Week", "This Month", "This Quarter"}:
        return filtered

    anchor = parsed_dates.max().normalize()
    if period == "This Week":
        start = anchor - pd.Timedelta(days=anchor.weekday())
        mask = parsed_dates.between(start, anchor + pd.Timedelta(days=1), inclusive="left")
    elif period == "This Month":
        mask = parsed_dates.dt.to_period("M") == anchor.to_period("M")
    else:
        mask = parsed_dates.dt.to_period("Q") == anchor.to_period("Q")
    return filtered.loc[mask.fillna(False)]


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
    hours_col = _numeric_col(df, "hours_logged")
    billable_col = _numeric_col(df, "billable_hours")

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
    alloc_hours_col = _numeric_col(df, "allocated_hours")
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
    capacity_col = _numeric_col(df, "capacity_hours_monthly")
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
    hours_col = _numeric_col(df, "hours_logged")
    if cat_col is not None and hours_col is not None:
        category_hours = pd.DataFrame({"category": cat_col, "hours": hours_col})
        charts["hours_by_category"] = category_hours.groupby("category")["hours"].sum().sort_values(ascending=False).head(8)

    # ── Utilization by department ──────────────────────────────────────
    dept_col2 = _safe_col(df, "department")
    billable_col = _numeric_col(df, "billable_hours")
    hours_col2 = _numeric_col(df, "hours_logged")
    if dept_col2 is not None and billable_col is not None and hours_col2 is not None:
        department_hours = pd.DataFrame({"department": dept_col2, "billable": billable_col, "hours": hours_col2})
        dept_util = department_hours.groupby("department").sum(numeric_only=True)
        dept_util["utilization"] = (dept_util["billable"] / dept_util["hours"].replace(0, pd.NA) * 100).fillna(0).round(1)
        charts["utilization_by_dept"] = dept_util["utilization"].sort_values(ascending=False)

    # ── Experience distribution ────────────────────────────────────────
    exp_col = _safe_col(df, "experience_years")
    if exp_col is not None:
        charts["experience_dist"] = exp_col.value_counts().sort_index()

    # ── Top projects by hours ──────────────────────────────────────────
    proj_col = _safe_col(df, "project_id")
    hours_col3 = _numeric_col(df, "hours_logged")
    if proj_col is not None and hours_col3 is not None:
        project_hours = pd.DataFrame({"project": proj_col, "hours": hours_col3})
        charts["top_projects"] = project_hours.groupby("project")["hours"].sum().sort_values(ascending=False).head(8)

    return charts


def calculate_capacity_metrics(
    files: dict[str, pd.DataFrame],
    period: str = "This Month",
    start_date=None,
    end_date=None,
) -> pd.DataFrame:
    """Combine uploaded employee, allocation, and timesheet data for capacity views."""
    employee_df = next(
        (frame for frame in files.values() if {"employee_id", "capacity_hours_monthly"} <= set(frame.columns)),
        None,
    )
    if employee_df is None:
        return pd.DataFrame()

    result = employee_df.copy()
    numeric = ["capacity_hours_monthly"]
    for column in numeric:
        result[column] = pd.to_numeric(result[column], errors="coerce").fillna(0)

    def aggregate(columns: set[str], value: str, output: str) -> None:
        source = next((frame for frame in files.values() if columns <= set(frame.columns)), None)
        if source is None:
            result[output] = 0.0
            return
        filtered = filter_dataset(source, period, "", start_date, end_date)
        values = pd.to_numeric(filtered[value], errors="coerce").fillna(0)
        grouped = pd.DataFrame({"employee_id": filtered["employee_id"], output: values}).groupby("employee_id")[output].sum()
        result[output] = result["employee_id"].map(grouped).fillna(0)

    aggregate({"employee_id", "allocated_hours", "allocation_start_date"}, "allocated_hours", "allocated_hours")
    aggregate({"employee_id", "hours_logged", "work_date"}, "hours_logged", "hours_logged")
    aggregate({"employee_id", "billable_hours", "work_date"}, "billable_hours", "billable_hours")
    result["capacity_load_pct"] = (result["allocated_hours"] / result["capacity_hours_monthly"].replace(0, pd.NA) * 100).fillna(0).round(1)
    result["utilization_pct"] = (result["billable_hours"] / result["hours_logged"].replace(0, pd.NA) * 100).fillna(0).round(1)
    result["capacity_variance_hours"] = (result["capacity_hours_monthly"] - result["allocated_hours"]).round(1)
    result["capacity_status"] = result["capacity_load_pct"].map(
        lambda value: "Overloaded" if value > 100 else "On target" if value >= 70 else "Available"
    )
    return result


def generate_insights(metrics: pd.DataFrame, assignments: list[dict] | None = None) -> pd.DataFrame:
    """Generate explainable workforce alerts from capacity and assignment data."""
    alerts: list[dict] = []
    if not metrics.empty:
        for row in metrics.itertuples(index=False):
            if row.capacity_load_pct > 100:
                alerts.append({
                    "severity": "Critical",
                    "type": "Overloaded",
                    "subject": row.employee_name,
                    "evidence": f"Allocated {row.allocated_hours:.1f}h against {row.capacity_hours_monthly:.1f}h capacity ({row.capacity_load_pct:.1f}%).",
                    "recommendation": "Review allocations and move work to available capacity.",
                })
            elif row.utilization_pct < 70 and row.hours_logged > 0:
                alerts.append({
                    "severity": "Warning",
                    "type": "Under-utilized",
                    "subject": row.employee_name,
                    "evidence": f"Billable utilization is {row.utilization_pct:.1f}%, below the 70% target.",
                    "recommendation": "Review upcoming work and identify billable assignments.",
                })
            if row.capacity_load_pct < 50 and row.capacity_hours_monthly > 0:
                alerts.append({
                    "severity": "Info",
                    "type": "Unused capacity",
                    "subject": row.employee_name,
                    "evidence": f"Only {row.capacity_load_pct:.1f}% of monthly capacity is allocated.",
                    "recommendation": "Consider this employee for available project work.",
                })

    if assignments:
        grouped: dict[tuple[str, str], list[dict]] = {}
        for assignment in assignments:
            grouped.setdefault((assignment["employee_id"], assignment["work_date"]), []).append(assignment)
        for (employee_id, work_date), items in grouped.items():
            ordered = sorted(items, key=lambda item: item["start_time"])
            for previous, current in zip(ordered, ordered[1:]):
                from datetime import datetime, timedelta

                previous_start = datetime.fromisoformat(f"{work_date}T{previous['start_time']}")
                previous_end = previous_start + timedelta(hours=previous["duration_hours"])
                current_start = datetime.fromisoformat(f"{work_date}T{current['start_time']}")
                if current_start < previous_end:
                    alerts.append({
                        "severity": "Warning",
                        "type": "Assignment conflict",
                        "subject": employee_id,
                        "evidence": f"'{previous['title']}' overlaps '{current['title']}' on {work_date}.",
                        "recommendation": "Adjust one assignment or confirm the overlap is intentional.",
                    })
    return pd.DataFrame(alerts, columns=["severity", "type", "subject", "evidence", "recommendation"])


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
        "uploaded_files": {},
        "selected_file": None,
        "planning_items": [],
        "uploader_version": 0,
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
    st.session_state["uploaded_files"] = {}
    st.session_state["selected_file"] = None
    st.session_state["planning_items"] = []
    st.session_state["uploader_version"] = st.session_state.get("uploader_version", 0) + 1
    for key in (
        "nav_radio",
        "period_selector",
        "global_search",
        "workforce_search",
        "workforce_dept",
        "workforce_status",
        "workforce_team",
        "custom_start_date",
        "custom_end_date",
        "custom_date_range",
    ):
        if key in st.session_state:
            del st.session_state[key]
