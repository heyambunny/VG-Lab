import streamlit as st
import pandas as pd
import numpy as np
import requests
from route_guard import protect_page

protect_page('eSeal')

if not st.session_state.get('authenticated'):
    st.switch_page('pages/Login.py')


tab1, tab2, tab3 = st.tabs(["eSeal IOT Info", "Pin Verification", "Pin Validation"])

with tab1:
    st.write("To verify the product information")
    module_id = st.secrets["module_id"]
    access_token = st.secrets["access_token"]
    vendor_token = st.secrets["vendor_token"]

    #API_URL = "https://live.esealcom.com/scoapi/IoTinfo"   # 🔁 replace with actual API

# -------------------- UI Form --------------------
    with st.form("iot_form"):
        iot = st.text_input(
        "Enter QR Code",
        placeholder="e.g. 1234567890"
        )
        submit = st.form_submit_button("Fetch Details")

# -------------------- API Call --------------------
    if submit:
        if not iot:
           st.error("IOT number is required")
        elif not iot.isdigit():
           st.error("IOT must be numeric")
    else:
        form_data = {
            "module_id": module_id,
            "access_token": access_token,
            "vendor_token": vendor_token,
            "iot": iot
        }

        try:
            with st.spinner("Calling API..."):
                response = requests.post(
                    API_URL,
                    data=form_data,
                    timeout=15
                )

            if response.status_code == 200:
                st.success("Data fetched successfully")

                try:
                    data = response.json()

                    if isinstance(data, list):
                        st.dataframe(data)
                    else:
                        st.json(data)

                except Exception:
                    st.text(response.text)

            else:
                st.error(f"API failed (Status: {response.status_code})")
                st.text(response.text)

        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {e}")

with tab2:
    st.write("To check whether PIN is Required to scan this product or not")

with tab3:
    st.write("To validate the PIN is correct or not")

st.set_page_config(
    page_title="eSeal API",
    layout="wide")

