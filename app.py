import streamlit as st
from auth_config import ROLES
from PIL import Image

# logo = Image.open("assets/vguard.png")
# st.sidebar.image(logo, width=150)

st.set_page_config(
    page_title="CSV Processing App",
    layout="wide")

# -----------------------------
# SESSION INITIALIZATION
# -----------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "role" not in st.session_state:
    st.session_state.role = None

# -----------------------------
# GLOBAL AUTH GUARD
# -----------------------------
if not st.session_state.authenticated:
    st.switch_page("pages/Login.py")

# -----------------------------
# SIDEBAR (ROLE-BASED NAV)
# -----------------------------
st.sidebar.title("Navigation")

allowed_pages = ROLES[st.session_state.role]["allowed_pages"]

PAGE_MAP = {
    "index": "pages/index.py",
    "Retailer Points": "pages/Retailer Points.py",
    "msScheme": "pages/msScheme.py",
    "Milestone": "pages/Milestone.py",
    'Hubli Wires Scheme':"pages/Hubli Wires Scheme.py",
    'SG Mega Bonanza': 'pages/SG Mega Bonanza.py',
    'Ahmedabad Wires Scheme': 'pages/Ahmedabad Wires Scheme.py',
    'data_import': 'pages/data_import.py',
    "Sfdc Data Check": 'pages/Sfdc Data Check.py',
    'Switch Gear Pan India': 'pages/Switch Gear Pan India.py',
    'Hafele Sales Report':'Hafele Sales Report.py',
    'eSeal':'eSeal.py'
}

for page in allowed_pages:
    st.sidebar.page_link(PAGE_MAP[page], label=page)

st.sidebar.divider()

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.switch_page("pages/Login.py")

# -----------------------------
# HOME CONTENT
# -----------------------------
st.title("Dashboard")

st.success(f"Welcome, {st.session_state.role.upper()} user")
st.write("Use the sidebar to navigate through the application.")


# tab1, tab2, tab3 = st.tabs(["Overview", "Branch-wise", "Member-wise"])

# with tab1:
#     st.write("Overview metrics")

# with tab2:
#     st.write("Branch data")

# with tab3:
#     st.write("Member-level insights")

# with st.expander("Scheme Performance Summary"):
#     st.write("Content here")

# with st.expander("Region-wise Breakdown"):
#     st.write("Content here")

# col1, col2 = st.columns(2)

# with col1:
#     st.metric("Total Scans", 12500)

# with col2:
#     st.metric("Active Members", 820)

# with st.sidebar:
#     st.header("Filters")
#     scheme = st.selectbox("Scheme", ["Switch Gear", "Wires", "Pipes"])
#     date_range = st.date_input("Date Range")

# st.metric("Error QRs", 250, delta="+45")

# mode = st.toggle("Presentation Mode")