"""Sidebar navigation for the Streamlit workforce planner."""

from __future__ import annotations

import streamlit as st

from .themer import NAV_ITEMS, get_active_page_key
from .data_handler import load_uploaded_file, reset_session_state
from .auth import logout


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
        uploaded_files = st.file_uploader(
            "Upload dataset",
            type=["csv", "json"],
            accept_multiple_files=True,
            key=f"dataset_uploader_{st.session_state.get('uploader_version', 0)}",
            help="Select one or more CSV or JSON files",
            label_visibility="collapsed",
        )

        if uploaded_files:
            loaded_files = {}
            for uploaded_file in uploaded_files:
                df = load_uploaded_file(uploaded_file)
                if df is not None:
                    loaded_files[uploaded_file.name] = df
                else:
                    st.error(f"Could not parse {uploaded_file.name}")

            if loaded_files:
                st.session_state["uploaded_files"] = loaded_files
                if st.session_state.get("selected_file") not in loaded_files:
                    st.session_state["selected_file"] = next(iter(loaded_files))

        files = st.session_state.get("uploaded_files", {})
        if files:
            selected_file = st.selectbox(
                "Active dataset",
                options=list(files),
                index=list(files).index(st.session_state.get("selected_file"))
                if st.session_state.get("selected_file") in files else 0,
                key="active_dataset_selector",
                label_visibility="collapsed",
            )
            st.session_state["selected_file"] = selected_file
            st.session_state["uploaded_df"] = files[selected_file]
            st.session_state["file_name"] = selected_file
            st.success(f"Loaded {len(files)} dataset(s)")

        # ── Reset button (LU 2.53) ──────────────────────────────────────
        if st.button("\u21ba  Reset", use_container_width=True, key="reset_btn"):
            reset_session_state()
            st.rerun()

        # ── User profile ───────────────────────────────────────────────
        current_user = st.session_state.get("current_user", {})
        if st.button("Sign out", use_container_width=True, key="sign_out_btn"):
            logout()
            st.rerun()
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='user-card'>"
            "<div class='avatar'>" + current_user.get("full_name", "User")[:2].upper() + "</div>"
            "<div>"
            "<div class='user-name'>" + current_user.get("full_name", "User") + "</div>"
            "<div class='user-role'>" + current_user.get("role", "viewer").title() + "</div>"
            "</div>"
            "</div>",
            unsafe_allow_html=True,
        )

    return selected_key
