import streamlit as st
from auth_config import ROLES

def protect_page(page_name: str):
    if not st.session_state.get("authenticated"):
        st.switch_page("pages/Login.py")

    role = st.session_state.get("role")

    if role not in ROLES:
        st.error("Invalid role")
        st.stop()

    if page_name not in ROLES[role]["allowed_pages"]:
        st.error("You are not authorized to access this page.")
        st.stop()
