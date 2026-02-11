import streamlit as st
import pandas as pd
import numpy as np
from route_guard import protect_page

protect_page('Ahmedabad Wires Scheme')

if not st.session_state.get('authenticated'):
    st.switch_page('pages/Login.py')

st.set_page_config(
    page_title="Ahemdabad Wires Scheme",
    layout="wide")

if "df1" not in st.session_state:
    st.session_state.df1 = None
if "df2" not in st.session_state:
    st.session_state.df2 = None
if "df3" not in st.session_state:
    st.session_state.df3 = None
if "df4" not in st.session_state:
    st.session_state.df4 = None

st.title('Ahmedabad Wires Scheme')
st.write('Scheme Period: 01 Sep 2025 to 31 Mar 2026')
@st.dialog('Image Preview')
def img_preview(img):
    st.image(img, use_container_width=True)

if st.button("View Scheme Banner"): img_preview('assets/AHM_wires.jpeg')

st.divider()

f1,f2,f3,f4 = st.columns([1,1,1,1])

file_1 = f1.file_uploader('Upload Sep Month Transactions', type=['xls','csv'])
file_2 = f2.file_uploader('Upload Oct Month Transactions', type=['xls','csv'])
file_3 = f3.file_uploader('Upload Nov Month Transactions', type=['xls','csv'])
file_4 = f4.file_uploader('Upload Dec Month Transactions', type=['xls','csv'])

def read_file(file):
    file.seek(0)
    filename = file.name.lower()

    if filename.endswith('.csv'):
        sep = ','
        chunksize=100_000
    elif filename.endswith('.xls'):
        sep = '\t'
        chunksize=300_000
    else:
        raise ValueError('Only CSV or XLS format allowed')
    
    chunks = []
    for chunk in pd.read_csv(file,
                             sep=sep,
                             engine='c',
                             chunksize=chunksize):chunks.append(chunk)
    return pd.concat(chunks, ignore_index=True)

if file_1 and file_2 and file_3 and file_4:
    if st.session_state.df1 is None:
        with st.spinner("Reading file 1...."):
            st.session_state.df1 = read_file(file_1)
    
    if st.session_state.df2 is None:
        with st.spinner("Reading file 2...."):
            st.session_state.df2 = read_file(file_2)

    if st.session_state.df3 is None:
        with st.spinner("Reading file 3...."):
            st.session_state.df3 = read_file(file_3)

    if st.session_state.df4 is None:
        with st.spinner("Reading file 4...."):
            st.session_state.df4 = read_file(file_4)

    st.success("All files loaded successfully")

@st.cache_data(show_spinner=False)
def run_scheme(sep,oct,nov,dec):
    df = pd.concat([sep,oct,nov,dec], ignore_index=True)
    ahm = df[df['Branch'].isin(['Ahmedabad'])]
    ahm = ahm[ahm['Influencer Type'].isin(['Plumbing Expert','Electrical Expert','Electrical and Plumbing Expert'])]
    ahm = ahm[ahm['Product Category'].isin(['Wires'])]
    ahm = ahm[ahm['Base Points']>0]
    scheme = ahm.groupby(['Rishta Id', 'State', 'District', 'Branch']).agg(
    Wires_Scan_Count=('Base Points','count'))
    scheme_report = scheme.reset_index()
    conditions = [
    scheme_report['Wires_Scan_Count'] >= 1100,
    scheme_report['Wires_Scan_Count'] >= 600,
    scheme_report['Wires_Scan_Count'] >= 400,
    scheme_report['Wires_Scan_Count'] >= 300,
    scheme_report['Wires_Scan_Count'] >= 225,
    scheme_report['Wires_Scan_Count'] >= 150,
    scheme_report['Wires_Scan_Count'] >= 100,
    scheme_report['Wires_Scan_Count'] >= 75,
    scheme_report['Wires_Scan_Count'] >= 50,
    scheme_report['Wires_Scan_Count'] <50,
    ]
    values = [
    'Hero HF Deluxe Bike',
    'Branded Air Conditioner 1.5 Ton',
    'Branded Washing Machine',
    'Branded Smart TV 32 Inch',
    'Branded Smart Phone',
    'Aristrocraft Fencer pack of 3 trolley Suitcases Cabin, Medium & Large',
    'Bosch Drill Machine',
    'Smart Watch (Titan Fast-track or equivalent)',
    'Bluetooth Earbuds (Boat/Pebble or equivalent)',
    'Not Qualified'
    ]
    scheme_report['Gift Qualification'] = np.select(conditions, values, default='Not Qualified')
    qualified = scheme_report[~scheme_report['Gift Qualification'].isin(['Not Qualified'])]
    return qualified

if st.button('Generate Report'):
    data = run_scheme(st.session_state.df1,
                      st.session_state.df2,
                      st.session_state.df3,
                      st.session_state.df4)
    st.success("Scheme generated successfully")
    st.title("Qualified Members Report")
    st.dataframe(data)
    st.divider()
    summary = data.groupby(['Gift Qualification'])['Rishta Id'].count()
    st.title("Gifts Summary")
    st.dataframe(summary)
