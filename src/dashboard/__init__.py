"""Dashboard module for Streamlit workforce planner application."""

from .themer import inject_global_css, TOKENS, NAV_ITEMS
from .navigation import render_sidebar
from .layout import (
    render_top_header,
    render_page_header,
    render_kpi_card,
    render_status_badge,
    render_section_card_open,
    close_section_card,
    render_placeholder,
)

__all__ = [
    "inject_global_css",
    "TOKENS",
    "NAV_ITEMS",
    "render_sidebar",
    "render_top_header",
    "render_page_header",
    "render_kpi_card",
    "render_status_badge",
    "render_section_card_open",
    "close_section_card",
    "render_placeholder",
]
