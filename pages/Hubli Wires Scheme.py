import streamlit as st
import pandas as pd
import numpy as np
from route_guard import protect_page
from PIL import Image

protect_page('Hubli Wires Scheme')
if not st.session_state.get("authenticated"):
    st.switch_page('pages/Login.py')

st.title('Hubli Wires Scheme')
st.write('Scheme Duration: 01 Dec 2025 to 31 Mar 2026')
@st.dialog("Scheme Preview")
def show_preview():
    st.image("assets/hubli_wires.jpeg", use_container_width=True)

if st.button("View Scheme"):
    show_preview()
st.divider()

if "df1" not in st.session_state:
    st.session_state.df1 = None
if "df2" not in st.session_state:
    st.session_state.df2 = None
if "df3" not in st.session_state:
    st.session_state.df3 = None

file_3 = st.file_uploader('Upload Enrollment Report', type=['xls'])

c1, c2 = st.columns([1,1])
file_1 = c1.file_uploader('Upload Dec Month File', type=['xls', 'csv'])
file_2 = c2.file_uploader('Upload Jan Month File', type=['xls', 'csv'])

@st.cache_data(show_spinner=False)
def read_file(file):
    file.seek(0)
    filename = file.name.lower()

    if filename.endswith(".csv"):
        sep = ","
        chunksize=100_000
    elif filename.endswith(".xls"):
        sep = "\t"
        chunksize=300_000
    else:
        raise ValueError('Only CSV or XLS format allowed')
    
    chunks =[]
    for chunk in pd.read_csv(file,
                             sep=sep,
                             engine="python",
                             chunksize=chunksize):chunks.append(chunk)
    return pd.concat(chunks, ignore_index=True)

MAX_FILE_SIZE_MB = 500

def validate_file(uploaded_file, label):
    if uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        st.error(f"{label} exceeds {MAX_FILE_SIZE_MB} MB")
        st.stop()

if file_1 and file_2:
    if st.session_state.df1 is None:
        with st.spinner("Reading File 1..."):
            st.session_state.df1 = read_file(file_1)

    if st.session_state.df2 is None:
        with st.spinner("Reading File 2..."):
            st.session_state.df2 = read_file(file_2)

    st.success("Both files loaded successfully")

    st.write(
        "Dec → Total Data:", len(st.session_state.df1),
        "Columns:", len(st.session_state.df1.columns)
    )
    st.write(
        "Jan → Total Data:", len(st.session_state.df2),
        "Columns:", len(st.session_state.df2.columns)
    )


@st.cache_data(show_spinner=False)
def run_scheme(a, b):
    df = pd.concat([a, b], ignore_index=True)
    Hubli_Gulbarga = df[df['Branch'].isin(['Hubli', 'Gulbarga'])]
    Hubli_Gulbarga = Hubli_Gulbarga[Hubli_Gulbarga['Influencer Type'].isin(['Plumbing Expert','Electrical Expert','Electrical and Plumbing Expert'])]
    Hubli_Gulbarga = Hubli_Gulbarga[Hubli_Gulbarga['Product Category'].isin(['Wires'])]
    Hubli_Gulbarga = Hubli_Gulbarga[Hubli_Gulbarga['Base Points']>0]
    scheme = Hubli_Gulbarga.groupby(['Rishta Id', 'Member name', 'Mobile Number', 'State', 'District', 'Branch']).agg(
     Wires_Scan_Count=('Base Points','count'))
    scheme_report = scheme.reset_index()
    conditions = [
    scheme_report['Wires_Scan_Count'] < 50,
    (scheme_report['Wires_Scan_Count'] >= 50) & 
    (scheme_report['Wires_Scan_Count'] < 80),
    (scheme_report['Wires_Scan_Count'] >= 80) & 
    (scheme_report['Wires_Scan_Count'] < 125),
    (scheme_report['Wires_Scan_Count'] >= 125) & 
    (scheme_report['Wires_Scan_Count'] < 180),
    scheme_report['Wires_Scan_Count'] >= 180
    ]
    values = [
    'Not Qualified',
    'Borosil Lunch Box',
    'V-Guard Gas Stove',
    'V-Guard Invidia 75-3J Mixer Grinder',
    'V-Guard Water Heater: Sieta - 10 Ltr'
    ]
    scheme_report['Gift Qualification'] = np.select(conditions, values, default='Not Qualified')
    qualified = scheme_report[~scheme_report['Gift Qualification'].isin(['Not Qualified'])]
    return qualified

if st.button('Generate'):
    if (st.session_state.df1) is None:
      st.warning('File Not Yet Uploaded, please upload the file!')
    else:
      qualified = run_scheme(st.session_state.df1, st.session_state.df2)
      st.success("Scheme generated successfully")
      st.title("Qualified Members Report")
      st.dataframe(qualified)
      st.divider()
      summary = qualified.groupby(['Gift Qualification'])['Rishta Id'].count()
      st.title("Gifts Summary")
      st.dataframe(summary)

