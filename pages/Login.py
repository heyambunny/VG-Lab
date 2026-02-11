# import streamlit as st
# from auth_config import ROLES

# from PIL import Image

# logo = Image.open("assets/V-Guard_NewLogo.jpg")
# st.sidebar.image(logo, width=250)

# USERS = st.secrets["users"]

# st.title("Login")

# username = st.text_input("Username")
# password = st.text_input("Password", type="password")

# if st.button("Login"):
#     user = USERS.get(username)

#     if user and user["password"] == password:
#         st.session_state.authenticated = True
#         st.session_state.username = username
#         st.session_state.role = user["role"]

#         st.switch_page("pages/index.py")
#     else:
#         st.error("Invalid credentials")

import streamlit as st
from auth_config import ROLES
from PIL import Image

# -------------------------
# Load Logo
# -------------------------
logo = Image.open("assets/V-Guard_NewLogo.jpg")
st.sidebar.image(logo, width=250)

# -------------------------
# Initialize session state
# -------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = None

if "role" not in st.session_state:
    st.session_state.role = None

# -------------------------
# If already logged in
# -------------------------
if st.session_state.authenticated:
    st.success(f"Logged in as {st.session_state.username}")
    st.switch_page("pages/index.py")

# -------------------------
# Load Users from Secrets
# -------------------------
try:
    USERS = st.secrets["users"]
except KeyError:
    st.error("User configuration not found in Streamlit Secrets.")
    st.stop()

# -------------------------
# Login UI
# -------------------------
st.title("Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):

    user = USERS.get(username)

    if user and user["password"] == password:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.role = user["role"]

        st.success("Login successful")
        st.switch_page("pages/index.py")

    else:
        st.error("Invalid username or password")
