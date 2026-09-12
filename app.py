"""Workforce Utilization Platform — Streamlit entry point.

Run with:  streamlit run app.py
"""

from __future__ import annotations

import streamlit as st
import pandas as pd
from src.config import DATABASE_PATH

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
    load_database_files,
    filter_dataset,
    calculate_capacity_metrics,
    generate_insights,
    enrich_with_employee_dimensions,
)
from src.dashboard.api_client import create_assignment, delete_assignment, get_assignments, get_employees, update_assignment
from src.dashboard.auth import render_login


st.set_page_config(
    page_title="Workforce Utilization Platform",
    page_icon="\U0001f4ca",
    layout="wide",
)


inject_global_css()


initialise_session_state()


if not render_login():
    st.stop()

if not st.session_state.get("uploaded_files"):
    with st.spinner("Loading dashboard data..."):
        database_files = load_database_files()
    if database_files:
        st.session_state["uploaded_files"] = database_files
        st.session_state["using_database_files"] = True
        st.session_state["selected_file"] = next(iter(database_files))


@st.fragment(run_every="5s")
def refresh_database_snapshot() -> None:
    current_signature = DATABASE_PATH.stat().st_mtime_ns if DATABASE_PATH.exists() else None
    previous_signature = st.session_state.get("database_signature")
    st.session_state["database_signature"] = current_signature
    if previous_signature is None or previous_signature == current_signature:
        return
    if not st.session_state.get("using_database_files", True):
        return
    load_database_files.clear()
    database_files = load_database_files()
    if database_files:
        st.session_state["uploaded_files"] = database_files
        st.session_state["selected_file"] = next(iter(database_files))
    st.rerun(scope="app")


refresh_database_snapshot()

active_key = render_sidebar()


page_label = next(
    (item["label"] for item in NAV_ITEMS if item["key"] == active_key),
    "Overview",
)


render_top_header(page_label)



def render_dataset_info() -> None:
    """Show dataset info panel when a file has been uploaded."""
    raw_df = st.session_state.get("uploaded_df")
    fname = st.session_state.get("file_name")
    if raw_df is None:
        return
    df = filter_dataset(
        raw_df,
        st.session_state.get("period", "This Month"),
        st.session_state.get("global_search", ""),
        st.session_state.get("custom_start_date"),
        st.session_state.get("custom_end_date"),
    )

    render_section_card_open("Uploaded Dataset", fname)
    summary = get_dataset_summary(df)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", f"{summary['rows']:,}")
    c2.metric("Columns", summary["columns"])
    c3.metric(
        "Null %",
        f"{summary['null_pct']}%",
        help="Percentage of cells without a value. Useful for spotting incomplete source data.",
    )
    c4.metric(
        "Memory",
        f"{summary['memory_mb']} MB",
        help="Approximate in-memory size of the filtered DataFrame, useful for monitoring large uploads.",
    )

    preview_rows = st.number_input(
        "Rows to preview",
        min_value=1,
        max_value=max(1, len(df)),
        value=min(10, max(1, len(df))),
        step=10,
        key="dataset_preview_rows",
        help="Choose how many rows to display. This changes the preview only, not the dataset.",
    )
    st.markdown(f"**Data Preview ({int(preview_rows):,} of {len(df):,} rows)**")
    st.dataframe(df.head(int(preview_rows)), use_container_width=True)

    with st.expander("Basic Statistics", expanded=False):
        st.caption("Descriptive statistics help identify distributions, ranges, and data-quality issues before interpreting workforce metrics.")
        st.dataframe(df.describe(include="all"), use_container_width=True)
    close_section_card()


def render_overview() -> None:
    """Render the Overview dashboard with KPI cards and chart placeholders."""
    render_page_header(
        "Workforce Overview",
        "Understand workforce capacity, planned workload and utilization across the organization.",
    )

    raw_df = st.session_state.get("uploaded_df")
    files = st.session_state.get("uploaded_files", {})
    df = (
        filter_dataset(
            raw_df,
            st.session_state.get("period", "This Month"),
            st.session_state.get("global_search", ""),
            st.session_state.get("custom_start_date"),
            st.session_state.get("custom_end_date"),
        )
        if raw_df is not None else None
    )
    analysis_df = enrich_with_employee_dimensions(df, files) if df is not None else None

    render_dataset_info()

    kpi_cols = st.columns(6)

    if df is not None:
        kpi_data = calculate_kpis(df)
        kpis = kpi_data["kpis"]
    else:
        kpis = [
            {"label": "Total Records", "value": "--", "icon": "\U0001f4ca", "delta": None, "icon_color": None},
            {"label": "Columns", "value": "--", "icon": "\U0001f4c8", "delta": None, "icon_color": None},
            {"label": "Total Employees", "value": "--", "icon": "\U0001f465", "delta": None, "icon_color": None},
            {"label": "Total Hours", "value": "--", "icon": "\U0001f551", "delta": None, "icon_color": None},
            {"label": "Billable Hours", "value": "--", "icon": "\U0001f512", "delta": None, "icon_color": None},
            {"label": "Utilization Rate", "value": "--", "icon": "\U0001f4c8", "delta": None, "icon_color": None},
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

    chart_left, chart_right = st.columns([2, 1])

    with chart_left:
        render_section_card_open("Data Distribution", "Breakdown of uploaded dataset")

        if df is not None:
            charts = get_chart_data(analysis_df)

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
                fig.update_traces(hovertemplate="%{label}<br>%{value:.1f} hours<extra></extra>")
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
            fig.update_traces(hovertemplate="%{label}<br>%{value} employees<extra></extra>")
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

    raw_df = st.session_state.get("uploaded_df")
    if raw_df is None:
        render_placeholder("Upload a dataset to view workforce data", height=400)
        return

    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

    with col1:
        local_search = st.text_input("Search employees...", key="workforce_search")

    search = local_search or st.session_state.get("global_search", "")
    df = filter_dataset(
        raw_df,
        st.session_state.get("period", "This Month"),
        search,
        st.session_state.get("custom_start_date"),
        st.session_state.get("custom_end_date"),
    )

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

    filtered = df.copy()

    if dept_filter != "All" and "department" in df.columns:
        filtered = filtered[filtered["department"] == dept_filter]

    if status_filter != "All" and "employment_status" in df.columns:
        filtered = filtered[filtered["employment_status"] == status_filter]

    if team_filter != "All" and "team" in df.columns:
        filtered = filtered[filtered["team"] == team_filter]

    st.markdown(f"**Showing {len(filtered)} of {len(df)} records**")

    st.dataframe(filtered, use_container_width=True, height=400)


def render_work_planning() -> None:
    """Render the database-backed weekly assignment planner."""
    from datetime import date, time, timedelta

    render_page_header(
        "Work Planning",
        "Assign work to people across a clear weekly schedule.",
    )

    token = st.session_state["access_token"]
    current_user = st.session_state.get("current_user", {})
    if notice := st.session_state.pop("planning_notice", None):
        st.success(notice)

    def format_duration(hours: float) -> str:
        value = float(hours)
        number = f"{value:g}"
        return f"{number} hour" if value == 1 else f"{number} hours"

    try:
        employees = get_employees(token)
        assignments = get_assignments(
            token,
            st.session_state.get("custom_start_date").isoformat()
            if st.session_state.get("period") == "Custom" and st.session_state.get("custom_start_date") else None,
            st.session_state.get("custom_end_date").isoformat()
            if st.session_state.get("period") == "Custom" and st.session_state.get("custom_end_date") else None,
        )
    except Exception as exc:
        st.error(f"Could not load Work Planning data: {exc}")
        return

    employee_options = {employee["employee_name"]: employee["employee_id"] for employee in employees}
    with st.expander("+ Assign work", expanded=True):
        with st.form("planning_form", clear_on_submit=True, enter_to_submit=False):
            form_cols = st.columns([2, 1, 1, 1, 1])
            with form_cols[0]:
                title = st.text_input("Work title", placeholder="e.g. Client discovery")
            with form_cols[1]:
                assignee_name = st.selectbox("Assignee", list(employee_options) or ["No employees loaded"])
            with form_cols[2]:
                work_date = st.date_input("Date", value=date.today())
            with form_cols[3]:
                start_time = st.time_input("Starts", value=time(9, 0))
            with form_cols[4]:
                duration = st.number_input("Hours", min_value=0.5, max_value=12.0, value=1.0, step=0.5)
            submitted = st.form_submit_button("Add to calendar", type="primary")

        if submitted:
            if title.strip() and employee_options:
                created = create_assignment(token, {
                    "title": title.strip(),
                    "employee_id": employee_options[assignee_name],
                    "work_date": work_date.isoformat(),
                    "start_time": start_time.isoformat(),
                    "duration_hours": duration,
                })
                for warning in created.get("warnings", []):
                    st.warning(warning)
                st.session_state["planning_notice"] = "Assignment created successfully."
                st.rerun()
            else:
                st.warning("Add a work title and load at least one employee before saving.")

    week_start = date.today() - timedelta(days=date.today().weekday())
    week = [week_start + timedelta(days=i) for i in range(7)]
    employee_names = {employee["employee_id"]: employee["employee_name"] for employee in employees}
    employee_rows = sorted({item["employee_id"] for item in assignments}) or ["Unassigned"]
    calendar_cols = st.columns([1.4] + [1] * 7)
    calendar_cols[0].markdown("**Team**")
    for col, day in zip(calendar_cols[1:], week):
        col.markdown(f"**{day.strftime('%a')}**<br><small>{day.strftime('%d %b')}</small>", unsafe_allow_html=True)

    for employee_id in employee_rows:
        row = st.columns([1.4] + [1] * 7)
        row[0].markdown(f"**{employee_names.get(employee_id, employee_id)}**")
        for index, day in enumerate(week):
            day_items = [item for item in assignments if item["employee_id"] == employee_id and item["work_date"] == day.isoformat()]
            if day_items:
                content = "<br>".join(
                    f"<span class='calendar-item'><b>{item['title']}</b><br>{format_duration(item['duration_hours'])}</span>"
                    for item in day_items
                )
                row[index + 1].markdown(content, unsafe_allow_html=True)
            else:
                row[index + 1].markdown("<div class='calendar-empty'>&nbsp;</div>", unsafe_allow_html=True)

    if assignments and current_user.get("role") in {"admin", "manager"}:
        st.markdown("### Manage assignments")
        assignment_labels = {
            item["id"]: f"{item['work_date']} {item['start_time']} | {item['title']} | {item['employee_name']}"
            for item in assignments
        }
        selected_id = st.selectbox("Assignment to edit", list(assignment_labels), format_func=assignment_labels.get)
        selected = next(item for item in assignments if item["id"] == selected_id)
        with st.form("edit_assignment_form", enter_to_submit=False):
            edit_title = st.text_input("Title", value=selected["title"])
            edit_employee = st.selectbox(
                "Assignee",
                list(employee_options),
                index=list(employee_options.values()).index(selected["employee_id"])
                if selected["employee_id"] in employee_options.values() else 0,
            )
            edit_date = st.date_input("Date", value=date.fromisoformat(selected["work_date"]))
            edit_start = st.time_input("Starts", value=time.fromisoformat(selected["start_time"]))
            edit_duration = st.number_input("Hours", min_value=0.5, max_value=24.0, value=float(selected["duration_hours"]), step=0.5)
            if st.form_submit_button("Save changes", type="primary"):
                updated = update_assignment(token, selected_id, {
                    "title": edit_title.strip(),
                    "employee_id": employee_options[edit_employee],
                    "work_date": edit_date.isoformat(),
                    "start_time": edit_start.isoformat(),
                    "duration_hours": edit_duration,
                })
                for warning in updated.get("warnings", []):
                    st.warning(warning)
                st.session_state["planning_notice"] = "Assignment updated successfully."
                st.rerun()

        for item in assignments:
            edit_col, delete_col = st.columns([5, 1])
            edit_col.write(f"{item['work_date']} {item['start_time']} | {item['title']} | {item['employee_name']}")
            if delete_col.button("Delete", key=f"delete_assignment_{item['id']}"):
                delete_assignment(token, item["id"])
                st.session_state["planning_notice"] = "Assignment deleted successfully."
                st.rerun()


def render_capacity() -> None:
    """Render capacity load, utilization, and availability analytics."""
    render_page_header(
        "Capacity & Utilization",
        "Review capacity load, billable utilization, and available workforce bandwidth.",
    )
    files = st.session_state.get("uploaded_files", {})
    metrics = calculate_capacity_metrics(
        files,
        st.session_state.get("period", "This Month"),
        st.session_state.get("custom_start_date"),
        st.session_state.get("custom_end_date"),
    )
    if metrics.empty:
        render_placeholder("Upload employee, allocation, and timesheet datasets to see capacity analytics", height=300)
        return

    total_capacity = metrics["capacity_hours_monthly"].sum()
    total_allocated = metrics["allocated_hours"].sum()
    total_logged = metrics["hours_logged"].sum()
    total_billable = metrics["billable_hours"].sum()
    kpis = st.columns(5)
    kpis[0].metric("Employees", f"{len(metrics):,}")
    kpis[1].metric("Monthly Capacity", f"{total_capacity:,.0f} hrs")
    kpis[2].metric("Allocated", f"{total_allocated:,.0f} hrs")
    kpis[3].metric("Capacity Load", f"{(total_allocated / total_capacity * 100) if total_capacity else 0:.1f}%")
    kpis[4].metric("Billable Utilization", f"{(total_billable / total_logged * 100) if total_logged else 0:.1f}%")

    import plotly.express as px
    left, right = st.columns(2)
    with left:
        grouped = metrics.groupby("department", dropna=False)[["capacity_hours_monthly", "allocated_hours"]].sum().reset_index()
        grouped["capacity_load_pct"] = (grouped["allocated_hours"] / grouped["capacity_hours_monthly"].replace(0, pd.NA) * 100).fillna(0).round(1)
        fig = px.bar(grouped, x="department", y="capacity_load_pct", color="capacity_load_pct", color_continuous_scale="Blues", labels={"capacity_load_pct": "Capacity Load %"})
        fig.add_hline(y=100, line_dash="dash", line_color="#EF4444")
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=320)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        status_counts = metrics["capacity_status"].value_counts().rename_axis("status").reset_index(name="employees")
        fig = px.pie(status_counts, names="status", values="employees", color="status", color_discrete_map={"Overloaded": "#EF4444", "On target": "#10B981", "Available": "#F59E0B"})
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", height=320)
        fig.update_traces(hovertemplate="%{label}<br>%{value} employees<extra></extra>")
        st.plotly_chart(fig, use_container_width=True)

    display_columns = ["employee_id", "employee_name", "department", "team", "capacity_hours_monthly", "allocated_hours", "hours_logged", "billable_hours", "capacity_load_pct", "utilization_pct", "capacity_variance_hours", "capacity_status"]
    st.dataframe(metrics[display_columns].sort_values("capacity_load_pct", ascending=False), use_container_width=True, hide_index=True)


def render_team_analytics() -> None:
    """Render department, team, employee, and project comparisons."""
    render_page_header(
        "Team Analytics",
        "Compare workload, capacity, and utilization across organizational levels.",
    )
    files = st.session_state.get("uploaded_files", {})
    metrics = calculate_capacity_metrics(
        files,
        st.session_state.get("period", "This Month"),
        st.session_state.get("custom_start_date"),
        st.session_state.get("custom_end_date"),
    )
    if metrics.empty:
        render_placeholder("Upload employee, allocation, and timesheet datasets to see team analytics", height=300)
        return

    filter_cols = st.columns(3)
    with filter_cols[0]:
        departments = ["All"] + sorted(metrics["department"].dropna().unique().tolist())
        department = st.selectbox("Department", departments, key="team_analytics_department")
    scoped = metrics if department == "All" else metrics[metrics["department"] == department]
    with filter_cols[1]:
        teams = ["All"] + sorted(scoped["team"].dropna().unique().tolist())
        team = st.selectbox("Team", teams, key="team_analytics_team")
    scoped = scoped if team == "All" else scoped[scoped["team"] == team]
    with filter_cols[2]:
        employees = ["All"] + sorted(scoped["employee_name"].dropna().unique().tolist())
        employee = st.selectbox("Employee", employees, key="team_analytics_employee")
    scoped = scoped if employee == "All" else scoped[scoped["employee_name"] == employee]

    kpis = st.columns(4)
    capacity = scoped["capacity_hours_monthly"].sum()
    allocated = scoped["allocated_hours"].sum()
    logged = scoped["hours_logged"].sum()
    billable = scoped["billable_hours"].sum()
    kpis[0].metric("People", f"{len(scoped):,}")
    kpis[1].metric("Capacity Load", f"{allocated / capacity * 100 if capacity else 0:.1f}%")
    kpis[2].metric("Utilization", f"{billable / logged * 100 if logged else 0:.1f}%")
    kpis[3].metric("Available Hours", f"{(capacity - allocated):,.0f}")

    import plotly.express as px
    left, right = st.columns(2)
    with left:
        grouped = scoped.groupby("team", dropna=False)[["capacity_hours_monthly", "allocated_hours", "billable_hours", "hours_logged"]].sum().reset_index()
        grouped["capacity_load_pct"] = (grouped["allocated_hours"] / grouped["capacity_hours_monthly"].replace(0, pd.NA) * 100).fillna(0).round(1)
        fig = px.bar(grouped, x="team", y="capacity_load_pct", color="capacity_load_pct", color_continuous_scale="Blues", labels={"capacity_load_pct": "Capacity Load %"})
        fig.add_hline(y=100, line_dash="dash", line_color="#EF4444")
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=320)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        grouped["utilization_pct"] = (grouped["billable_hours"] / grouped["hours_logged"].replace(0, pd.NA) * 100).fillna(0).round(1)
        fig = px.bar(grouped, x="team", y="utilization_pct", color="utilization_pct", color_continuous_scale="Teal", labels={"utilization_pct": "Billable Utilization %"})
        fig.add_hline(y=70, line_dash="dash", line_color="#10B981")
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=320)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Employee drill-down")
    employee_columns = ["employee_id", "employee_name", "department", "team", "capacity_hours_monthly", "allocated_hours", "hours_logged", "billable_hours", "capacity_load_pct", "utilization_pct", "capacity_status"]
    st.dataframe(scoped[employee_columns].sort_values("capacity_load_pct", ascending=False), use_container_width=True, hide_index=True)

    allocation = next((frame for frame in files.values() if {"project_id", "employee_id", "allocated_hours"} <= set(frame.columns)), None)
    if allocation is not None:
        allocation = filter_dataset(allocation, st.session_state.get("period", "This Month"), "", st.session_state.get("custom_start_date"), st.session_state.get("custom_end_date"))
        allocation = allocation[allocation["employee_id"].isin(scoped["employee_id"])]
        project_summary = allocation.assign(allocated_hours=pd.to_numeric(allocation["allocated_hours"], errors="coerce").fillna(0)).groupby("project_id", as_index=False)["allocated_hours"].sum().sort_values("allocated_hours", ascending=False)
        st.markdown("### Project allocation")
        st.dataframe(project_summary, use_container_width=True, hide_index=True)


def render_insights() -> None:
    """Render explainable rule-based workforce insights and alerts."""
    render_page_header(
        "Insights & Alerts",
        "System-generated intelligence indicating workforce conditions requiring attention.",
    )
    files = st.session_state.get("uploaded_files", {})
    metrics = calculate_capacity_metrics(
        files,
        st.session_state.get("period", "This Month"),
        st.session_state.get("custom_start_date"),
        st.session_state.get("custom_end_date"),
    )
    assignments = []
    try:
        assignments = get_assignments(
            st.session_state["access_token"],
            st.session_state.get("custom_start_date").isoformat()
            if st.session_state.get("period") == "Custom" and st.session_state.get("custom_start_date") else None,
            st.session_state.get("custom_end_date").isoformat()
            if st.session_state.get("period") == "Custom" and st.session_state.get("custom_end_date") else None,
        )
    except Exception:
        pass
    alerts = generate_insights(metrics, assignments)
    if alerts.empty:
        render_placeholder("No alerts for the selected period", height=220)
        return

    severity = st.selectbox("Severity", ["All", "Critical", "Warning", "Info"], key="insights_severity")
    visible = alerts if severity == "All" else alerts[alerts["severity"] == severity]
    counts = st.columns(3)
    counts[0].metric("Critical", int((alerts["severity"] == "Critical").sum()))
    counts[1].metric("Warnings", int((alerts["severity"] == "Warning").sum()))
    counts[2].metric("Informational", int((alerts["severity"] == "Info").sum()))
    st.dataframe(visible, use_container_width=True, hide_index=True)


def render_reports() -> None:
    """Render filtered data and summary report exports."""
    from io import BytesIO

    render_page_header(
        "Reports & Exports",
        "Configure, preview, and download filtered workforce analytics reports.",
    )
    files = st.session_state.get("uploaded_files", {})
    if not files:
        render_placeholder("Upload datasets to generate reports", height=300)
        return

    report_type = st.selectbox("Report", ["Filtered source data", "Capacity summary", "Insights and alerts"], key="report_type")
    export_format = st.selectbox("Format", ["CSV", "JSON", "Excel"], key="report_format")
    metrics = calculate_capacity_metrics(
        files,
        st.session_state.get("period", "This Month"),
        st.session_state.get("custom_start_date"),
        st.session_state.get("custom_end_date"),
    )
    if report_type == "Filtered source data":
        source_name = st.selectbox("Source dataset", list(files), key="report_source")
        report_df = filter_dataset(
            files[source_name],
            st.session_state.get("period", "This Month"),
            st.session_state.get("global_search", ""),
            st.session_state.get("custom_start_date"),
            st.session_state.get("custom_end_date"),
        )
    elif report_type == "Capacity summary":
        report_df = metrics
    else:
        report_df = generate_insights(metrics)

    st.caption(f"{len(report_df):,} rows will be exported using the current global filters.")
    st.dataframe(report_df.head(25), use_container_width=True, hide_index=True)
    if export_format == "CSV":
        data = report_df.to_csv(index=False).encode("utf-8")
        mime = "text/csv"
        extension = "csv"
    elif export_format == "JSON":
        data = report_df.to_json(orient="records", date_format="iso", indent=2).encode("utf-8")
        mime = "application/json"
        extension = "json"
    else:
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            report_df.to_excel(writer, index=False, sheet_name="Report")
        data = buffer.getvalue()
        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        extension = "xlsx"
    st.download_button(
        "Download report",
        data=data,
        file_name=f"workforce_{report_type.lower().replace(' ', '_')}.{extension}",
        mime=mime,
        type="primary",
        use_container_width=True,
    )


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
