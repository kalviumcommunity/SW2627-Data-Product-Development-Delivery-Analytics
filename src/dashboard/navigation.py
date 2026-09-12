"""Sidebar navigation for the Streamlit workforce planner."""

from __future__ import annotations

import streamlit as st

from .themer import NAV_ITEMS, get_active_page_key
from .data_handler import load_database_files, load_uploaded_file, reset_session_state
from .auth import logout
from .api_client import create_user, list_users, update_user_role, update_user_status


def render_sidebar() -> str:
    """Render the sidebar navigation and return the selected page key.

    Returns:
        The key of the currently selected navigation item.
    """
    with st.sidebar:
        st.markdown(
            "<div style='padding:8px 0 14px 0;'>"
            "<div class='brand-title'>Workforce Planner</div>"
            "<div class='brand-sub'>Utilization Analytics</div>"
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div style='font-size:10px; text-transform:uppercase; "
            "letter-spacing:0.8px; color:#64748B; padding:6px 4px;'>"
            "Navigation</div>",
            unsafe_allow_html=True,
        )

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

        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

        st.markdown(
            "<div style='font-size:10px; text-transform:uppercase; "
            "letter-spacing:0.8px; color:#64748B; padding:6px 4px;'>"
            "Data</div>",
            unsafe_allow_html=True,
        )

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
                st.session_state["using_database_files"] = False
                if st.session_state.get("selected_file") not in loaded_files:
                    st.session_state["selected_file"] = next(iter(loaded_files))

        files = st.session_state.get("uploaded_files", {})
        if not files:
            database_files = load_database_files()
            if database_files:
                files = database_files
                st.session_state["uploaded_files"] = database_files
                st.session_state["using_database_files"] = True
                st.session_state["selected_file"] = next(iter(database_files))
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

        if st.button("\u21ba  Reset", use_container_width=True, key="reset_btn"):
            reset_session_state()
            st.rerun()

        current_user = st.session_state.get("current_user", {})
        if st.button("Sign out", use_container_width=True, key="sign_out_btn"):
            logout()
            st.rerun()

        if current_user.get("role") == "admin":
            with st.expander("Admin", expanded=False):
                token = st.session_state.get("access_token")
                try:
                    users = list_users(token)
                    st.caption(f"{len(users)} user(s)")
                    with st.form("create_user_form", clear_on_submit=True, enter_to_submit=False):
                        new_name = st.text_input("Full name")
                        new_email = st.text_input("Email")
                        new_password = st.text_input("Temporary password", type="password")
                        new_role = st.selectbox("Role", ["viewer", "manager", "admin"])
                        if st.form_submit_button("Create user"):
                            create_user(token, {"full_name": new_name, "email": new_email, "password": new_password, "role": new_role})
                            st.success("User created")
                            st.rerun()
                    for user in users:
                        st.markdown(f"**{user['full_name']}**  \n{user['email']}")
                        role_col, status_col = st.columns(2)
                        role = role_col.selectbox("Role", ["viewer", "manager", "admin"], index=["viewer", "manager", "admin"].index(user["role"]), key=f"role_{user['id']}")
                        if role != user["role"] and role_col.button("Save role", key=f"save_role_{user['id']}"):
                            update_user_role(token, user["id"], role)
                            st.rerun()
                        label = "Deactivate" if user["is_active"] else "Activate"
                        is_current_user = user["id"] == current_user.get("id")
                        if is_current_user and user["is_active"]:
                            status_col.caption("Current user")
                        elif status_col.button(label, key=f"toggle_user_{user['id']}"):
                            update_user_status(token, user["id"], not user["is_active"])
                            st.rerun()
                except Exception as exc:
                    st.error(f"Could not load users: {exc}")
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
