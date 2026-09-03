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
if "active_page" not in st.session_state:
    st.session_state["active_page"] = "overview"

if "period" not in st.session_state:
    st.session_state["period"] = "This Month"


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

def render_overview() -> None:
    """Render the Overview dashboard with KPI cards and chart placeholders."""
    render_page_header(
        "Workforce Overview",
        "Understand workforce capacity, planned workload and utilization across the organization.",
    )

    # ── KPI cards row ──────────────────────────────────────────────────
    kpi_cols = st.columns(6)

    kpis = [
        ("Total Employees",   "842",  "\U0001f465", "+3.2%",  None),
        ("Total Working Hours","6,736 hrs","\U0001f551", None,  None),
        ("Committed Hours",   "5,412 hrs","\U0001f512", None,  None),
        ("Available Capacity","1,324 hrs","\u26a1",     None,  None),
        ("Avg Utilization",   "80.3%", "\U0001f4c8",  None,  None),
        ("Employees at Risk", "47",    "\u26a0\ufe0f", None,  "accent_red"),
    ]

    for col, (label, value, icon, delta, icon_color) in zip(kpi_cols, kpis):
        render_kpi_card(col, label, value, icon, delta=delta, icon_color=icon_color)

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    # ── Charts row ─────────────────────────────────────────────────────
    chart_left, chart_right = st.columns([2, 1])

    with chart_left:
        render_section_card_open(
            "Workforce Capacity Overview",
            "Distribution of 6,738 total working hours",
        )
        render_placeholder("Capacity bar chart — LU 2.55", height=200)
        close_section_card()

    with chart_right:
        render_section_card_open("Needs Attention")
        render_placeholder("Alerts list — LU 2.55", height=200)
        close_section_card()

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    # ── Second row ─────────────────────────────────────────────────────
    trend_left, dist_right = st.columns([2, 1])

    with trend_left:
        render_section_card_open(
            "Utilization Trend",
            "Daily averages vs 85% Target",
        )
        render_placeholder("Line chart — LU 2.55", height=280)
        close_section_card()

    with dist_right:
        render_section_card_open("Capacity Distribution")
        render_placeholder("Pie / donut chart — LU 2.55", height=130)

        render_section_card_open("Allocation Breakdown")
        render_placeholder("Donut chart — LU 2.55", height=130)
        close_section_card()


def render_workforce() -> None:
    """Render the Workforce page (placeholder for LU 2.52+)."""
    render_page_header(
        "Workforce",
        "View employee capacity, workload and utilization.",
    )
    render_placeholder("Employee table with search and filters — LU 2.52", height=400)


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
