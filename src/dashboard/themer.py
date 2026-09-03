"""Dark enterprise theme tokens and CSS injection for Streamlit dashboard."""

from __future__ import annotations

import streamlit as st


# ---------------------------------------------------------------------------
# Design tokens — matches Figma / reference UI
# ---------------------------------------------------------------------------
TOKENS = {
    "bg_app": "#0B1020",
    "bg_sidebar": "#0F1729",
    "bg_card": "#161D33",
    "bg_card_hover": "#1B2340",
    "border": "#2A3450",
    "border_strong": "#3A4565",
    "text_primary": "#FFFFFF",
    "text_secondary": "#94A3B8",
    "text_muted": "#64748B",
    "accent_blue": "#3B82F6",
    "accent_indigo": "#6366F1",
    "accent_cyan": "#06B6D4",
    "accent_purple": "#8B5CF6",
    "accent_green": "#10B981",
    "accent_amber": "#F59E0B",
    "accent_orange": "#F97316",
    "accent_red": "#EF4444",
    "radius": "12px",
    "radius_sm": "8px",
    "shadow": "0 4px 16px rgba(0, 0, 0, 0.25)",
}


# ---------------------------------------------------------------------------
# Navigation items — 7 pages with icons and accent colours
# ---------------------------------------------------------------------------
NAV_ITEMS = [
    {"key": "overview",        "label": "Overview",              "icon": "\U0001f4ca", "color": TOKENS["accent_cyan"]},
    {"key": "workforce",       "label": "Workforce",             "icon": "\U0001f465", "color": TOKENS["accent_cyan"]},
    {"key": "work_planning",   "label": "Work Planning",         "icon": "\U0001f4cb", "color": TOKENS["accent_purple"]},
    {"key": "capacity",        "label": "Capacity & Utilization","icon": "\U0001f4c8", "color": TOKENS["accent_blue"]},
    {"key": "team_analytics",  "label": "Team Analytics",        "icon": "\U0001f52c", "color": TOKENS["accent_cyan"]},
    {"key": "insights",        "label": "Insights / Alerts",     "icon": "\U0001f514", "color": TOKENS["accent_orange"]},
    {"key": "reports",         "label": "Reports",               "icon": "\U0001f4c4", "color": TOKENS["accent_cyan"]},
]


def get_active_page_key() -> str:
    """Return the current active page key from session state."""
    return st.session_state.get("active_page", "overview")


def inject_global_css() -> None:
    """Inject dark-theme CSS into the Streamlit app."""
    t = TOKENS
    css = f"""
    <style>
    /* ── App background ─────────────────────────────────────────────── */
    .stApp {{
        background-color: {t['bg_app']};
        color: {t['text_primary']};
    }}

    /* ── Typography ────────────────────────────────────────────────── */
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}
    h1, h2, h3, h4 {{
        color: {t['text_primary']} !important;
        font-weight: 600;
    }}
    .stMarkdown p {{
        color: #CBD5E1;
    }}

    /* ── Sidebar ───────────────────────────────────────────────────── */
    section[data-testid="stSidebar"] {{
        background-color: {t['bg_sidebar']};
        border-right: 1px solid {t['border']};
    }}
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] label {{
        color: {t['text_secondary']};
    }}
    section[data-testid="stSidebar"] .stRadio > div {{
        gap: 4px;
    }}

    /* ── KPI Card ──────────────────────────────────────────────────── */
    .kpi-card {{
        background: {t['bg_card']};
        border: 1px solid {t['border']};
        border-radius: {t['radius']};
        padding: 18px 18px 14px 18px;
        position: relative;
        box-shadow: {t['shadow']};
        min-height: 110px;
    }}
    .kpi-card:hover {{
        border-color: {t['border_strong']};
    }}
    .kpi-label {{
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: {t['text_secondary']};
        font-weight: 600;
    }}
    .kpi-value {{
        font-size: 28px;
        font-weight: 700;
        color: {t['text_primary']};
        margin-top: 6px;
        line-height: 1.1;
    }}
    .kpi-icon {{
        position: absolute;
        top: 14px;
        right: 16px;
        font-size: 18px;
        opacity: 0.85;
    }}
    .kpi-delta {{
        font-size: 11px;
        margin-top: 8px;
        font-weight: 500;
    }}
    .kpi-delta-pos {{ color: {t['accent_green']}; }}
    .kpi-delta-neg {{ color: {t['accent_red']}; }}
    .kpi-delta-neutral {{ color: {t['text_muted']}; }}

    /* ── Section card ──────────────────────────────────────────────── */
    .section-card {{
        background: {t['bg_card']};
        border: 1px solid {t['border']};
        border-radius: {t['radius']};
        padding: 18px;
        margin-bottom: 14px;
    }}
    .section-title {{
        font-size: 14px;
        font-weight: 600;
        color: {t['text_primary']};
        margin-bottom: 4px;
    }}
    .section-sub {{
        font-size: 11px;
        color: {t['text_secondary']};
        margin-bottom: 12px;
    }}

    /* ── Status badges ─────────────────────────────────────────────── */
    .status-badge {{
        display: inline-block;
        padding: 2px 10px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.3px;
    }}
    .badge-healthy {{ background: rgba(6,182,212,0.15); color: {t['accent_cyan']}; }}
    .badge-high    {{ background: rgba(249,115,22,0.15); color: {t['accent_orange']}; }}
    .badge-over    {{ background: rgba(239,68,68,0.15);  color: {t['accent_red']}; }}
    .badge-warn    {{ background: rgba(245,158,11,0.15); color: {t['accent_amber']}; }}
    .badge-info    {{ background: rgba(99,102,241,0.15); color: {t['accent_indigo']}; }}

    /* ── Radio button hover ────────────────────────────────────────── */
    div[role="radiogroup"] label {{
        padding: 8px 10px !important;
        border-radius: {t['radius_sm']} !important;
        margin-bottom: 2px !important;
    }}
    div[role="radiogroup"] label:hover {{
        background: rgba(255,255,255,0.04) !important;
    }}

    /* ── Brand title in sidebar ────────────────────────────────────── */
    .brand-title {{
        font-size: 18px;
        font-weight: 700;
        color: {t['text_primary']};
    }}
    .brand-sub {{
        font-size: 11px;
        color: {t['text_muted']};
        margin-top: 2px;
    }}

    /* ── User card in sidebar ──────────────────────────────────────── */
    .user-card {{
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 0;
    }}
    .avatar {{
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, {t['accent_cyan']}, {t['accent_blue']});
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        font-weight: 700;
        color: #fff;
    }}
    .user-name {{
        font-size: 13px;
        font-weight: 600;
        color: {t['text_primary']};
    }}
    .user-role {{
        font-size: 11px;
        color: {t['text_secondary']};
    }}

    /* ── Placeholder / empty state ─────────────────────────────────── */
    .placeholder-box {{
        height: 220px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: {t['text_muted']};
        border: 1px dashed {t['border']};
        border-radius: 8px;
        font-size: 12px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
