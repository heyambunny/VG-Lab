import streamlit as st
import pandas as pd
from route_guard import protect_page
protect_page('SG Mega Bonanza')

if "df1" not in st.session_state:
    st.session_state.df1 = None

if not st.session_state.get('authenticated'):
    st.switch_page('pages/Login.py')

st.title('Switch Gear Bonanza Scheme')
st.write('Scheme Duration: 15 Dec 2025 to 15 Mar 2026')
@st.dialog("Scheme Preview")
def show_preview(img):
    st.image(img, use_container_width=True)

if st.button("View Scheme Banner"):
        show_preview('assets/SG.jpeg')

st.divider()

file_1 = st.file_uploader('Upload Dec Month file',type=['xls'])

def read_file(file):
     file.seek(0)

     chunks = []
     for chunk in pd.read_csv(file,
                              sep='\t',
                              engine='c',
                              chunksize=300_000):chunks.append(chunk)
     return pd.concat(chunks, ignore_index=True)

if file_1:
    if st.session_state.df1 is None:
        with st.spinner("Reading File 1..."):
            st.session_state.df1 = read_file(file_1)
    st.success('Data files loaded successfully')

    st.write(
        "Dec → Total Data:", len(st.session_state.df1),
        "Columns:", len(st.session_state.df1.columns)
    )

@st.cache_data(show_spinner=False)
def run_scheme(df):
     cs = df.columns
     return cs

if st.button('Generate'):
     data = run_scheme(st.session_state.df1)
     st.success("Data Fetched Successfully")
     st.dataframe(data)
