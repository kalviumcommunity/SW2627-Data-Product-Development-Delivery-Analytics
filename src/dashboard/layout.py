"""Reusable layout components for the Streamlit workforce planner."""

from __future__ import annotations

from datetime import date

import streamlit as st

from .themer import TOKENS


def render_top_header(active_page_label: str) -> str:
    """Render the top header bar with brand, period selector, and utility buttons.

    Args:
        active_page_label: Label of the currently active page (unused, reserved).

    Returns:
        The selected period string.
    """
    cols = st.columns([1.4, 2.6, 2.0, 0.4, 0.4, 0.4])

    with cols[0]:
        st.markdown(
            "<div class='brand-title'>Workforce Planner</div>"
            "<div class='brand-sub'>Utilization Analytics</div>",
            unsafe_allow_html=True,
        )

    with cols[1]:
        period = st.radio(
            "Period",
            options=["This Week", "This Month", "This Quarter", "Custom"],
            index=1,
            horizontal=True,
            label_visibility="collapsed",
            key="period_selector",
        )
        st.session_state["period"] = period
        if period == "Custom":
            default_start = st.session_state.get("custom_start_date", date.today().replace(day=1))
            default_end = st.session_state.get("custom_end_date", date.today())
            selected_range = st.date_input(
                "Custom date range",
                value=(default_start, default_end),
                key="custom_date_range",
            )
            if isinstance(selected_range, tuple) and len(selected_range) == 2:
                st.session_state["custom_start_date"], st.session_state["custom_end_date"] = selected_range

    with cols[2]:
        st.markdown(
            "<div style='display:flex; gap:8px; justify-content:flex-end; align-items:center;'>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with cols[3]:
        with st.popover("\U0001f50d"):
            st.text_input("Search the dashboard", key="global_search", placeholder="Search employees, teams...")

    with cols[4]:
        with st.popover("\U0001f514"):
            st.markdown("**Notifications**")
            st.caption("No new workforce alerts.")

    with cols[5]:
        with st.popover("\U0001f464"):
            current_user = st.session_state.get("current_user", {})
            st.markdown(f"**{current_user.get('full_name', 'User')}**")
            st.caption(current_user.get("role", "viewer").title())

    return period


def render_page_header(title: str, subtitle: str) -> None:
    """Render a page title and subtitle.

    Args:
        title: Large heading text.
        subtitle: Smaller description text below the heading.
    """
    sec_color = TOKENS["text_secondary"]
    html = (
        f"<h1 style='margin-bottom:6px; font-size:28px;'>{title}</h1>"
        f"<p style='color:{sec_color}; margin-top:0; margin-bottom:18px;'>{subtitle}</p>"
    )
    st.markdown(html, unsafe_allow_html=True)


def render_kpi_card(
    container,
    label: str,
    value: str,
    icon: str,
    delta: str | None = None,
    icon_color: str | None = None,
) -> None:
    """Render a KPI metric card inside the given container.

    Args:
        container: A Streamlit column or container to render into.
        label: Metric label (e.g. "Total Employees").
        value: Formatted metric value (e.g. "842").
        icon: Emoji or text icon.
        delta: Optional change indicator (e.g. "+3.2%").
        icon_color: Optional CSS colour for the icon.
    """
    if icon_color is None:
        icon_color = TOKENS["accent_blue"]

    if delta is None:
        delta_html = ""
    else:
        s = delta.strip()
        if s.startswith("+") or s.upper().startswith("UP"):
            delta_class = "kpi-delta-pos"
        elif s.startswith("-") or s.upper().startswith("DN"):
            delta_class = "kpi-delta-neg"
        else:
            delta_class = "kpi-delta-neutral"
        delta_html = f"<div class='kpi-delta {delta_class}'>{delta}</div>"

    card = (
        f"<div class='kpi-card'>"
        f"<div class='kpi-icon' style='color:{icon_color};'>{icon}</div>"
        f"<div class='kpi-label'>{label}</div>"
        f"<div class='kpi-value'>{value}</div>"
        f"{delta_html}"
        f"</div>"
    )
    container.markdown(card, unsafe_allow_html=True)


def render_status_badge(status: str) -> str:
    """Return HTML for a coloured status badge.

    Args:
        status: Status text (e.g. "Healthy", "High", "Overloaded").

    Returns:
        HTML string for the badge.
    """
    s = status.lower()
    if s in ("healthy", "ok", "on target"):
        cls, text = "badge-healthy", "Healthy"
    elif s in ("high", "warning"):
        cls, text = "badge-high", "High"
    elif s in ("overloaded", "critical"):
        cls, text = "badge-over", "Overloaded"
    elif s in ("under-utilized", "under"):
        cls, text = "badge-warn", "Under-utilized"
    else:
        cls, text = "badge-info", status
    return f"<span class='status-badge {cls}'>{text}</span>"


def render_section_card_open(title: str, subtitle: str | None = None) -> None:
    """Open a section card with a title and optional subtitle.

    Args:
        title: Section heading.
        subtitle: Optional description below the heading.
    """
    sub_html = ""
    if subtitle:
        sub_html = f"<div class='section-sub'>{subtitle}</div>"
    card = (
        f"<div class='section-card'>"
        f"<div class='section-title'>{title}</div>"
        f"{sub_html}"
    )
    st.markdown(card, unsafe_allow_html=True)


def close_section_card() -> None:
    """Close the currently open section card."""
    st.markdown("</div>", unsafe_allow_html=True)


def render_placeholder(text: str, height: int = 220) -> None:
    """Render a dashed-border placeholder box.

    Args:
        text: Message to display inside the placeholder.
        height: Box height in pixels.
    """
    muted = TOKENS["text_muted"]
    border = TOKENS["border"]
    style = (
        f"height:{height}px;"
        "display:flex; align-items:center; justify-content:center;"
        f"color:{muted};"
        f"border:1px dashed {border};"
        "border-radius:8px; font-size:12px;"
    )
    html = f"<div style='{style}'>{text}</div>"
    st.markdown(html, unsafe_allow_html=True)
