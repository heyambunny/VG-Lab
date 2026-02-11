import streamlit as st
from auth_config import ROLES

from PIL import Image

logo = Image.open("assets/V-Guard_NewLogo.jpg")
st.sidebar.image(logo, width=250)

USERS = {
    "admin": {"password": "Vguard@123", "role": "admin"},
    "sachin": {"password": "sachin@123", "role": "user"},
    "himanshu": {"password": "himanshu@123", "role": "user2"}
}

st.title("Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    user = USERS.get(username)

    if user and user["password"] == password:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.role = user["role"]

        st.switch_page("pages/index.py")
    else:
        st.error("Invalid credentials")
