
from __future__ import annotations

import streamlit as st

from .themer import NAV_ITEMS, get_active_page_key


def render_sidebar():
    with st.sidebar:
        st.markdown(
            "<'>div style=' padding: 8px 0 14px 0;'>"
            "<'>div style=' font-size:18px; font-weight:700; color:#FFF;'>" Workforce Planner</'div>"
            "<'>div style=' font-size:11px; color:#64748B; margin-top:2px;'>" Utilization Analytics</'div>"
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<'>div style=' font-size:10px; text-transform:uppercase; letter-spacing:0.8px; color:#64748B; padding:6px 4px;'>"Navigation</'div>",
            unsafe_allow_html=True,
        )

        current = get_active_page_key()
        labels = [item["icon"Y  "Y + item["label"Y] for item in NAV_ITEMS]
        default_idx = next(
            (i for i, item in enumerate(NAV_ITEMS) if item["key"Y == current), 0
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

        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

        st.markdown(
            "<'>div style=' font-size:10px; text-transform:uppercase; letter-spacing:0.8px; color:#64748B; padding:6px 4px;'>"Data</'div>",
            unsafe_allow_html=True,
        )
        st.file_uploader(
            "Upload dataset",
            type=["csv", "json"],
            key="dataset_uploader",
            help="CSV or JSON - added in LU 2.52",
            disabled=True,
        )

        if st.button("R  Reset", use_container_width=True, disabled=True):
            pass

        st.markdown("<hr>")

        st.markdown(
            "<'>div style=' font-size:11px; color:#94A3B8; margin-bottom:4px;'>"Workspace</'div>",
            unsafe_allow_html=True,
        )
        st.selectbox(
            "Workspace",
            options=["Default Workspace"],
            label_visibility="collapsed",
            key="workspace_selector",
        )

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

        st.markdown(
            "<'>div class=' user-card'>"
            "<'>div class=' avatar'>"PS</'div>"
            "<'>div""<'>div class=' user-name'>"Prabdeep Singh</'div>"<'>div class=' user-role'>"Operations Lead</'div>"</'div>",
            unsafe_allow_html=True,
        )

    return selected_key
