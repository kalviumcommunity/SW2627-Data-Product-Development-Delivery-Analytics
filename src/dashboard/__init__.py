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
from .data_handler import (
    load_uploaded_file,
    get_dataset_summary,
    calculate_kpis,
    get_chart_data,
    calculate_capacity_metrics,
    filter_dataset,
    initialise_session_state,
    reset_session_state,
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
    "load_uploaded_file",
    "get_dataset_summary",
    "calculate_kpis",
    "get_chart_data",
    "calculate_capacity_metrics",
    "filter_dataset",
    "initialise_session_state",
    "reset_session_state",
]
