from __future__ import annotations

import streamlit as st

# ---------------------------------------------------------------------------
# Page config – dark theme
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Workforce Utilization Platform",
    page_icon="📊",
    layout="wide",
)


# ---------------------------------------------------------------------------
# Navigation (sidebar) – matches reference UI
# ---------------------------------------------------------------------------
NAV = [
    ("📊 Overview", "overview"),
    ("👥 Workforce", "workforce"),
    ("📋 Work Planning", "work_planning"),
    ("📈 Capacity & Utilization", "capacity"),
    ("🔬 Team Analytics", "team_analytics"),
    ("🔔 Insights / Alerts", "insights"),
    ("📄 Reports", "reports"),
]


def render_sidebar() -> str:
    st.sidebar.title("Workforce Planner")
    st.sidebar.caption("Utilization Analytics")

    # Radio with emoji labels – each item has its accent colour
    labels = [f"{icon}  {title}" for title, key in NAV for icon in [title[0]]]
    # map label → key
    label_to_key = {f"{icon}  {title}": key for title, key in NAV for icon in [title[0]]}

    # keep selection in session state
    if "page_key" not in st.session_state:
        st.session_state.page_key = "overview"

    choice = st.sidebar.radio(
        "Navigate",
        options=labels,
        index=[k for k in [v for k, v in NAV]].index(st.session_state.page_key),
        label_visibility="collapsed",
    )
    selected_key = label_to_key[choice]
    if selected_key != st.session_state.page_key:
        st.session_state.page_key = selected_key
        st.rerun()

    # ── File uploader (LU 2.52 placeholder) ──────────────────────────────
    st.sidebar.divider()
    st.sidebar.file_uploader(
        "Upload dataset",
        type=["csv", "json"],
        help="CSV or JSON – added in LU 2.52",
    )

    # ── Reset button (LU 2.53 placeholder) ──────────────────────────────
    if st.sidebar.button("↺ Reset", disabled=True):
        pass

    # ── Workspace selector ───────────────────────────────────────────────
    st.sidebar.selectbox("Workspace", ["Default Workspace"])

    # ── User profile footer ──────────────────────────────────────────────
    st.sidebar.divider()
    st.sidebar.caption("Prabdeep Singh · Operations Lead")

    return selected_key


# ---------------------------------------------------------------------------
# Top header – period selector, search, user icons
# ---------------------------------------------------------------------------
def render_top_header() -> str:
    c1, c2, c3, c4, c5 = st.columns([1.5, 2.5, 1.5, 0.8, 0.7])
    with c1:
        st.title("Workforce Planner")
    with c2:
        period = st.radio(
            "Period",
            options=["This Week", "This Month", "This Quarter", "Custom"],
            horizontal=True,
            label_visibility="collapsed",
        )
    with c3:
        st.caption("Search")
    with c4:
        st.caption("Notifications")
    with c5:
        st.caption("Profile")
    return period


# ---------------------------------------------------------------------------
# Page renderers
# ---------------------------------------------------------------------------
def render_overview() -> None:
    """LU 2.51 – Overview dashboard skeleton."""
    period = render_top_header()
    render_page_header("Workforce Overview", "Understand workforce capacity, planned workload and utilization across the organization.")

    # 6 KPI cards (placeholder values – will be dynamic once data is loaded)
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    for card, (label, value, delta, icon) in zip(
        [k1, k2, k3, k4, k5, k6],
        [
            ("Total Employees", "842", "+3.2%", "👤"),
            ("Total Working Hours", "6,736 hrs", "", "⏱️"),
            ("Committed Hours", "5,412 hrs", "", "📋"),
            ("Available Capacity", "1,324 hrs", "", "💚"),
            ("Average Utilization", "80.3%", "", "📊"),
            ("Employees at Risk", "47", "", "⚠️"),
        ],
    ):
        card.metric(label, value, delta=delta)

    # ── Charts (placeholders – will render once data is loaded) ─────────
    st.divider()

    # A. Workforce Capacity Overview
    st.subheader("Workforce Capacity Overview")
    st.info("Stacked bar / area chart: Working Hours vs Committed Hours vs Available Hours (toggle: Hours / %)")

    # B. Utilization Trend
    st.subheader("Utilization Trend")
    st.line_chart({"Utilization": [80, 82, 78, 85, 81]}, use_container_width=True)

    # C. Capacity Distribution
    st.subheader("Capacity Distribution")
    st.caption("Bands: <60% • 60–80% • 80–95% • 95–100% • >100%")

    # D. Work Allocation Breakdown
    st.subheader("Work Allocation Breakdown")
    st.caption("Donut: Meetings • Project/Task Work • Admin Work • Training • Other")

    # E. Team Capacity Comparison
    st.subheader("Team Capacity Comparison")
    st.bar_chart(
        {"Engineering": 85, "Design": 78, "Product": 88, "Marketing": 65, "Sales": 72, "Operations": 80, "HR": 70},
        use_container_width=True,
    )

    # F. Priority Insights
    st.subheader("Needs Attention")
    st.success("12 employees above 100% planned utilization")
    st.success("Engineering has 240 hrs unused capacity")
    st.success("Meeting time increased 14% this month")


def render_page_header(title: str, subtitle: str) -> None:
    st.markdown(f"## {title}")
    st.caption(subtitle)


def render_empty_state() -> None:
    st.warning("⚠️ No data uploaded. Please upload a CSV or JSON file to begin.")


# ---------------------------------------------------------------------------
# Router – dispatches to the correct page renderer
# ---------------------------------------------------------------------------
def router(page_key: str) -> None:
    {
        "overview": render_overview,
        "workforce": lambda: render_empty_state(),
        "work_planning": lambda: render_empty_state(),
        "capacity": lambda: render_empty_state(),
        "team_analytics": lambda: render_empty_state(),
        "insights": lambda: render_empty_state(),
        "reports": lambda: render_empty_state(),
    }[page_key]()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    page_key = render_sidebar()
    period = render_top_header()
    render_page_header("Workforce Overview", "Understand workforce capacity, planned workload and utilization across the organization.")
    router(page_key)


if __name__ == "__main__":
    main()