"""Sidebar navigation for the Streamlit workforce planner."""

from __future__ import annotations

import streamlit as st

from .themer import NAV_ITEMS, get_active_page_key
from .data_handler import load_uploaded_file, reset_session_state


def render_sidebar() -> str:
    """Render the sidebar navigation and return the selected page key.

    Returns:
        The key of the currently selected navigation item.
    """
    with st.sidebar:
        # ── Brand ──────────────────────────────────────────────────────
        st.markdown(
            "<div style='padding:8px 0 14px 0;'>"
            "<div class='brand-title'>Workforce Planner</div>"
            "<div class='brand-sub'>Utilization Analytics</div>"
            "</div>",
            unsafe_allow_html=True,
        )

        # ── Section label ──────────────────────────────────────────────
        st.markdown(
            "<div style='font-size:10px; text-transform:uppercase; "
            "letter-spacing:0.8px; color:#64748B; padding:6px 4px;'>"
            "Navigation</div>",
            unsafe_allow_html=True,
        )

        # ── Navigation radio ───────────────────────────────────────────
        current = get_active_page_key()
        labels = [item["icon"] + "  " + item["label"] for item in NAV_ITEMS]
        default_idx = next(
            (i for i, item in enumerate(NAV_ITEMS) if item["key"] == current), 0
        )

        choice = st.radio(
            "Navigate",
            options=labels,
            index=default_idx,
            label_visibility="collapsed",
            key="nav_radio",
        )

        selected_key = NAV_ITEMS[labels.index(choice)]["key"]
        if selected_key != current:
            st.session_state["active_page"] = selected_key
            st.rerun()

        # ── Spacer ─────────────────────────────────────────────────────
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

        # ── Data section label ─────────────────────────────────────────
        st.markdown(
            "<div style='font-size:10px; text-transform:uppercase; "
            "letter-spacing:0.8px; color:#64748B; padding:6px 4px;'>"
            "Data</div>",
            unsafe_allow_html=True,
        )

        # ── File uploader (LU 2.52) ────────────────────────────────────
        uploaded_file = st.file_uploader(
            "Upload dataset",
            type=["csv", "json"],
            key="dataset_uploader",
            help="CSV or JSON file",
            label_visibility="collapsed",
        )

        if uploaded_file is not None:
            df = load_uploaded_file(uploaded_file)
            if df is not None:
                st.session_state["uploaded_df"] = df
                st.session_state["file_name"] = uploaded_file.name
                st.success(f"Loaded {uploaded_file.name}")
            else:
                st.error("Could not parse file")

        # ── Reset button (LU 2.53) ──────────────────────────────────────
        if st.button("\u21ba  Reset", use_container_width=True, key="reset_btn"):
            reset_session_state()
            st.rerun()

        st.markdown("<hr>")

        # ── Workspace selector ─────────────────────────────────────────
        st.markdown(
            "<div style='font-size:11px; color:#94A3B8; margin-bottom:4px;'>"
            "Workspace</div>",
            unsafe_allow_html=True,
        )
        st.selectbox(
            "Workspace",
            options=["Default Workspace"],
            label_visibility="collapsed",
            key="workspace_selector",
        )

        # ── User profile ───────────────────────────────────────────────
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='user-card'>"
            "<div class='avatar'>PS</div>"
            "<div>"
            "<div class='user-name'>Prabdeep Singh</div>"
            "<div class='user-role'>Operations Lead</div>"
            "</div>"
            "</div>",
            unsafe_allow_html=True,
        )

    return selected_key
