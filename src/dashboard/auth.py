"""Streamlit authentication gate for the FastAPI-backed dashboard."""

from __future__ import annotations

import streamlit as st

from .api_client import login


def render_login() -> bool:
    """Render login when no API session exists and return access state."""
    if st.session_state.get("access_token"):
        return True

    st.markdown(
        "<style>div[data-testid='InputInstructions']{display:none!important;}</style>",
        unsafe_allow_html=True,
    )
    st.markdown("## Sign in to Workforce Planner")
    with st.form("login_form", enter_to_submit=True):
        email = st.text_input("Email", autocomplete="email")
        password = st.text_input("Password", type="password", autocomplete="current-password")
        submitted = st.form_submit_button("Sign in", type="primary")
    if submitted:
        result, error = login(email.strip(), password)
        if error:
            st.error(error)
        else:
            st.session_state["access_token"] = result["access_token"]
            st.session_state["current_user"] = result["user"]
            st.rerun()
    return False


def logout() -> None:
    """Clear the current API session."""
    st.session_state.pop("access_token", None)
    st.session_state.pop("current_user", None)
