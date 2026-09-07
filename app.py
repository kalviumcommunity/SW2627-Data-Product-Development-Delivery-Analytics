"""Workforce Utilization Platform — Streamlit entry point.

Run with:  streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from src.dashboard import (
    inject_global_css,
    NAV_ITEMS,
    render_sidebar,
    render_top_header,
    render_page_header,
    render_kpi_card,
    render_section_card_open,
    close_section_card,
    render_placeholder,
    initialise_session_state,
    get_dataset_summary,
    calculate_kpis,
    get_chart_data,
)


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Workforce Utilization Platform",
    page_icon="\U0001f4ca",
    layout="wide",
)


# ---------------------------------------------------------------------------
# Inject dark theme CSS
# ---------------------------------------------------------------------------
inject_global_css()


# ---------------------------------------------------------------------------
# Initialise session state
# ---------------------------------------------------------------------------
initialise_session_state()


# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
active_key = render_sidebar()


# ---------------------------------------------------------------------------
# Map key → label for header
# ---------------------------------------------------------------------------
page_label = next(
    (item["label"] for item in NAV_ITEMS if item["key"] == active_key),
    "Overview",
)


# ---------------------------------------------------------------------------
# Top header (period selector is functional — stored in session_state)
# ---------------------------------------------------------------------------
render_top_header(page_label)


# ===========================================================================
# Page renderers
# ===========================================================================

def render_dataset_info() -> None:
    """Show dataset info panel when a file has been uploaded."""
    df = st.session_state.get("uploaded_df")
    fname = st.session_state.get("file_name")
    if df is None:
        return

    render_section_card_open("Uploaded Dataset", fname)
    summary = get_dataset_summary(df)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", f"{summary['rows']:,}")
    c2.metric("Columns", summary["columns"])
    c3.metric("Null %", f"{summary['null_pct']}%")
    c4.metric("Memory", f"{summary['memory_mb']} MB")

    st.markdown("**Column Types**")
    st.json({str(k): int(v) for k, v in summary["dtypes"].items()})

    st.markdown("**First 10 Rows**")
    st.dataframe(df.head(10), use_container_width=True)

    st.markdown("**Basic Statistics**")
    st.dataframe(df.describe(include="all"), use_container_width=True)
    close_section_card()


def render_overview() -> None:
    """Render the Overview dashboard with KPI cards and chart placeholders."""
    render_page_header(
        "Workforce Overview",
        "Understand workforce capacity, planned workload and utilization across the organization.",
    )

    # ── Dataset info (if uploaded) ─────────────────────────────────────
    render_dataset_info()

    # ── KPI cards row (dynamic or placeholder) ─────────────────────────
    df = st.session_state.get("uploaded_df")
    kpi_cols = st.columns(6)

    if df is not None:
        kpi_data = calculate_kpis(df)
        kpis = kpi_data["kpis"]
    else:
        # Placeholder KPIs when no data uploaded
        kpis = [
            ("Total Records", "--", "\U0001f4ca", None, None),
            ("Columns", "--", "\U0001f4c8", None, None),
            ("Total Employees", "--", "\U0001f465", None, None),
            ("Total Hours", "--", "\U0001f551", None, None),
            ("Billable Hours", "--", "\U0001f512", None, None),
            ("Utilization Rate", "--", "\U0001f4c8", None, None),
        ]

    for col, kpi in zip(kpi_cols, kpis):
        render_kpi_card(
            col,
            kpi["label"],
            kpi["value"],
            kpi["icon"],
            delta=kpi.get("delta"),
            icon_color=kpi.get("icon_color"),
        )

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    # ── Charts row ─────────────────────────────────────────────────────
    chart_left, chart_right = st.columns([2, 1])

    with chart_left:
        render_section_card_open("Data Distribution", "Breakdown of uploaded dataset")

        if df is not None:
            charts = get_chart_data(df)

            if "department_dist" in charts:
                import plotly.express as px
                fig = px.bar(
                    x=charts["department_dist"].values,
                    y=charts["department_dist"].index,
                    orientation="h",
                    labels={"x": "Count", "y": "Department"},
                    color_discrete_sequence=["#06B6D4"],
                )
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    height=280,
                    margin=dict(l=0, r=0, t=10, b=0),
                )
                st.plotly_chart(fig, use_container_width=True)
            elif "hours_by_category" in charts:
                import plotly.express as px
                fig = px.pie(
                    values=charts["hours_by_category"].values,
                    names=charts["hours_by_category"].index,
                    color_discrete_sequence=["#06B6D4", "#3B82F6", "#8B5CF6", "#F59E0B", "#EF4444"],
                )
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    height=280,
                    margin=dict(l=0, r=0, t=10, b=0),
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                render_placeholder("No categorical data for chart", height=280)
        else:
            render_placeholder("Upload a dataset to see charts", height=280)

        close_section_card()

    with chart_right:
        render_section_card_open("Quick Stats")

        if df is not None:
            st.metric("Total Rows", f"{df.shape[0]:,}")
            st.metric("Total Columns", df.shape[1])

            null_pct = round(df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100, 2)
            st.metric("Null %", f"{null_pct}%")

            mem = round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
            st.metric("Memory", f"{mem} MB")
        else:
            render_placeholder("Upload data to see stats", height=200)

        close_section_card()

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    # ── Second row ─────────────────────────────────────────────────────
    trend_left, dist_right = st.columns([2, 1])

    with trend_left:
        render_section_card_open("Utilization by Department", "Billable vs total hours")

        if df is not None and "utilization_by_dept" in charts:
            import plotly.express as px
            util_data = charts["utilization_by_dept"]
            fig = px.bar(
                x=util_data.index,
                y=util_data.values,
                labels={"x": "Department", "y": "Utilization %"},
                color_discrete_sequence=["#3B82F6"],
            )
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=280,
                margin=dict(l=0, r=0, t=10, b=0),
            )
            fig.add_hline(y=70, line_dash="dash", line_color="#10B981", annotation_text="70% target")
            st.plotly_chart(fig, use_container_width=True)
        else:
            render_placeholder("Upload timesheet data to see utilization", height=280)

        close_section_card()

    with dist_right:
        render_section_card_open("Experience Distribution")

        if df is not None and "experience_dist" in charts:
            import plotly.express as px
            exp_data = charts["experience_dist"]
            fig = px.pie(
                values=exp_data.values,
                names=[f"{x} yrs" for x in exp_data.index],
                color_discrete_sequence=["#06B6D4", "#3B82F6", "#8B5CF6", "#F59E0B", "#10B981"],
            )
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                height=200,
                margin=dict(l=0, r=0, t=10, b=0),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            render_placeholder("Upload employee data to see experience", height=200)

        close_section_card()


def render_workforce() -> None:
    """Render the Workforce page with employee table."""
    render_page_header(
        "Workforce",
        "View employee capacity, workload and utilization.",
    )

    df = st.session_state.get("uploaded_df")
    if df is None:
        render_placeholder("Upload a dataset to view workforce data", height=400)
        return

    # Search and filter row
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

    with col1:
        search = st.text_input("Search employees...", key="workforce_search")

    with col2:
        if "department" in df.columns:
            depts = ["All"] + sorted(df["department"].dropna().unique().tolist())
            dept_filter = st.selectbox("Department", depts, key="workforce_dept")
        else:
            dept_filter = "All"

    with col3:
        if "employment_status" in df.columns:
            statuses = ["All"] + sorted(df["employment_status"].dropna().unique().tolist())
            status_filter = st.selectbox("Status", statuses, key="workforce_status")
        else:
            status_filter = "All"

    with col4:
        if "team" in df.columns:
            teams = ["All"] + sorted(df["team"].dropna().unique().tolist())
            team_filter = st.selectbox("Team", teams, key="workforce_team")
        else:
            team_filter = "All"

    # Apply filters
    filtered = df.copy()

    if search and "employee_name" in df.columns:
        filtered = filtered[filtered["employee_name"].str.contains(search, case=False, na=False)]

    if dept_filter != "All" and "department" in df.columns:
        filtered = filtered[filtered["department"] == dept_filter]

    if status_filter != "All" and "employment_status" in df.columns:
        filtered = filtered[filtered["employment_status"] == status_filter]

    if team_filter != "All" and "team" in df.columns:
        filtered = filtered[filtered["team"] == team_filter]

    st.markdown(f"**Showing {len(filtered)} of {len(df)} records**")

    # Show table
    st.dataframe(filtered, use_container_width=True, height=400)


def render_work_planning() -> None:
    """Render the Work Planning page (placeholder for future LU)."""
    render_page_header(
        "Work Planning",
        "Plan employee work and understand remaining capacity.",
    )
    render_placeholder("Weekly calendar view with team assignments — future LU", height=400)


def render_capacity() -> None:
    """Render the Capacity & Utilization page (placeholder for future LU)."""
    render_page_header(
        "Capacity Analytics",
        "Review organization-wide utilization and resource availability for current planning period.",
    )
    render_placeholder("Capacity KPIs, trends, and distribution — future LU", height=400)


def render_team_analytics() -> None:
    """Render the Team Analytics page (placeholder for future LU)."""
    render_page_header(
        "Team Analytics",
        "Deep dive into capacity and utilization metrics.",
    )
    render_placeholder("Team breakdown, overload alerts, bandwidth — future LU", height=400)


def render_insights() -> None:
    """Render the Insights / Alerts page (placeholder for future LU)."""
    render_page_header(
        "Insights & Alerts",
        "System-generated intelligence indicating workforce conditions requiring attention.",
    )
    render_placeholder("Overload alerts, unused capacity, meeting trends — future LU", height=400)


def render_reports() -> None:
    """Render the Reports page (placeholder for future LU)."""
    render_page_header(
        "Report Generator",
        "Configure and export workforce analytics data.",
    )
    render_placeholder("Report type selection, filters, export — future LU", height=400)


# ---------------------------------------------------------------------------
# Page routing
# ---------------------------------------------------------------------------
PAGE_RENDERERS = {
    "overview":       render_overview,
    "workforce":      render_workforce,
    "work_planning":  render_work_planning,
    "capacity":       render_capacity,
    "team_analytics": render_team_analytics,
    "insights":       render_insights,
    "reports":        render_reports,
}

renderer = PAGE_RENDERERS.get(active_key, render_overview)
renderer()
