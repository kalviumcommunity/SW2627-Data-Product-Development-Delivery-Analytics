from __future__ import annotations

import streamlit as st

from .themer import TOKENS


def render_top_header(active_page_label):
    cols = st.columns([1.4, 2.6, 2.0, 0.4, 0.4, 0.4])
    with cols[0]:
        st.markdown(
            "<div class='brand-title'>Workforce Planner</div>"
            "<div class='brand-sub'>v1.0 - Sprint 1</div>",
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
    with cols[2]:
        st.markdown(
            "<div style='display:flex; gap:8px; justify-content:flex-end; align-items:center;'>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    with cols[3]:
        st.button("S", key="hdr_search", help="Search (LU 2.53)")
    with cols[4]:
        st.button("N", key="hdr_bell", help="Notifications")
    with cols[5]:
        st.button("U", key="hdr_user", help="Profile")
    return period


def render_page_header(title, subtitle):
    title_s = str(title)
    subtitle_s = str(subtitle)
    sec_color = TOKENS["text_secondary"]
    h1 = "<h1 style='margin-bottom:6px; font-size:28px;'>" + title_s + "</h1>"
    p = "<p style='color:" + sec_color + "; margin-top:0; margin-bottom:18px;'>" + subtitle_s + "</p>"
    st.markdown(h1 + p, unsafe_allow_html=True)


def render_kpi_card(container, label, value, icon, delta=None, icon_color=None):
    if icon_color is None:
        icon_color = TOKENS["accent_blue"]
    if delta is None:
        delta_html = ""
    else:
        s = delta.strip()
        if s.startswith("+") or s.startswith("UP"):
            delta_class = "kpi-delta-pos"
        elif s.startswith("-") or s.startswith("DN"):
            delta_class = "kpi-delta-neg"
        else:
            delta_class = "kpi-delta-neutral"
        delta_html = "<div class='kpi-delta " + delta_class + "'>" + str(delta) + "</div>"
    card = (
        "<div class='kpi-card'>"
        + "<div class='kpi-icon' style='color:" + icon_color + ";'>" + icon + "</div>"
        + "<div class='kpi-label'>" + str(label) + "</div>"
        + "<div class='kpi-value'>" + str(value) + "</div>"
        + delta_html
        + "</div>"
    )
    container.markdown(card, unsafe_allow_html=True)


def render_status_badge(status):
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
    return "<span class='status-badge " + cls + "'>" + text + "</span>"


def render_section_card_open(title, subtitle=None):
    sub_html = ""
    if subtitle:
        sub_html = "<div class='section-sub'>" + str(subtitle) + "</div>"
    card = (
        "<div class='section-card'>"
        + "<div class='section-title'>" + str(title) + "</div>"
        + sub_html
    )
    st.markdown(card, unsafe_allow_html=True)


def close_section_card():
    st.markdown("</div>", unsafe_allow_html=True)


def render_placeholder(text, height=220):
    muted = TOKENS["text_muted"]
    border = TOKENS["border"]
    style = (
        "height:" + str(height) + "px;"
        + "display:flex; align-items:center; justify-content:center;"
        + "color:" + muted + ";"
        + "border:1px dashed " + border + ";"
        + "border-radius:8px; font-size:12px;"
    )
    html = "<div style='" + style + "'>" + str(text) + "</div>"
    st.markdown(html, unsafe_allow_html=True)
