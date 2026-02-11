import streamlit as st
import pandas as pd
import numpy as np
from route_guard import protect_page

protect_page('Switch Gear Pan India')

st.set_page_config(
    page_title="Switch Gear Pan India",
    layout="wide")

if "df1" not in st.session_state:
    st.session_state.df1 = None
if "df2" not in st.session_state:
    st.session_state.df2 = None
if "df3" not in st.session_state:
    st.session_state.df3 = None

st.title('Switch Gear PAN India Scheme')
st.write('Scheme Duration: 15 Dec 2025 to 15 Mar 2026')
@st.dialog("Scheme Preview")
def show_preview(img):
    st.image(img, use_container_width=True)

if st.button("View Scheme Banner"):
        show_preview('assets/SGPANINDIA.jpeg')

st.divider()

f1,f2,f3 = st.columns([1,1,1])
file_1 = f1.file_uploader('Upload 15-31 Dec Month Transactions', type=['xls','csv'])
file_2 = f2.file_uploader('Upload Jan Month Transactions', type=['xls','csv'])
file_3 = f3.file_uploader('Upload Feb Month Transactions', type=['xls','csv'])

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

if file_1 and file_2:
    if st.session_state.df1 is None:
        with st.spinner("Reading file 1...."):
            st.session_state.df1 = read_file(file_1)
    
    if st.session_state.df2 is None:
        with st.spinner("Reading file 2...."):
            st.session_state.df2 = read_file(file_2)
    
    if st.session_state.df3 is None:
        with st.spinner("Reading file 3...."):
            st.session_state.df3 = read_file(file_3)
    st.success("All files loaded successfully")

@st.cache_data(show_spinner=False)
def run_scheme(file1, file2, file3):
    df = pd.concat([file1, file2, file3], ignore_index=True)
    ahm = df[~df['Branch'].isin(['Cochin'])]
    ahm = ahm[ahm['Influencer Type'].isin(['Plumbing Expert','Electrical Expert','Electrical and Plumbing Expert'])]
    ahm = ahm[ahm['Product Category'].isin(['MCBs and DBs'])]
    ahm = ahm[ahm['Base Points']>0]
    scheme = ahm.groupby(['Rishta Id', 'State', 'District', 'Branch']).agg(
    SG_Scan_Count=('Base Points','count'))
    scheme_report = scheme.reset_index()
    conditions = [
    scheme_report['SG_Scan_Count'] >= 500,
    scheme_report['SG_Scan_Count'] >= 400,
    scheme_report['SG_Scan_Count'] >= 300,
    scheme_report['SG_Scan_Count'] >= 200,
    scheme_report['SG_Scan_Count'] >= 100,
    scheme_report['SG_Scan_Count'] >= 50,
    scheme_report['SG_Scan_Count'] <50,
    ]
    values = ['6000', '4500', '3000', '1500', '700', '250', 'Not Qualified']
    scheme_report['Reward Qualification'] = np.select(conditions, values, default='Not Qualified')
    qualified = scheme_report[~scheme_report['Reward Qualification'].isin(['Not Qualified'])]
    return scheme_report

@st.cache_data(show_spinner=False)
def run_schem(file1, file2, file3):
    df = pd.concat([file1, file2, file3], ignore_index=True)
    ahm = df[~df['Branch'].isin(['Cochin'])]
    ahm = ahm[ahm['Influencer Type'].isin(['Plumbing Expert','Electrical Expert','Electrical and Plumbing Expert'])]
    ahm = ahm[ahm['Product Category'].isin(['MCBs and DBs'])]
    ahm = ahm[ahm['Base Points']>0]
    scheme = ahm.groupby(['Rishta Id', 'State', 'District', 'Branch','Product SubCategory']).agg(
    SG_Scan_Count=('Base Points','count')).unstack('Product SubCategory', fill_value=0)
    scheme.columns = scheme.columns.droplevel(0)
    scheme_report = scheme.reset_index()
    return scheme_report

@st.cache_data(show_spinner=False)
def run_cochin_scheme(file1, file2, file3):
    df = pd.concat([file1, file2, file3], ignore_index=True)
    ahm = df[df['Branch'].isin(['Cochin'])]
    ahm = ahm[ahm['Influencer Type'].isin(['Plumbing Expert','Electrical Expert','Electrical and Plumbing Expert'])]
    ahm = ahm[ahm['Product Category'].isin(['MCBs and DBs'])]
    ahm = ahm[ahm['Base Points']>0]
    scheme = ahm.groupby(['Rishta Id', 'State', 'District','DOJ' ,'Branch']).agg(
    SG_Scan_Count=('Base Points','count'))
    scheme_report = scheme.reset_index()
    conditions = [
    scheme_report['SG_Scan_Count'] >= 300,
    scheme_report['SG_Scan_Count'] >= 200,
    scheme_report['SG_Scan_Count'] >= 125,
    scheme_report['SG_Scan_Count'] >= 75,
    scheme_report['SG_Scan_Count'] >= 30,
    scheme_report['SG_Scan_Count'] <30,
    ]
    values = ['V-Guard Food Processor', 'V-Guard 3-Burner Glass Stove', 'V-Guard Pedestal Fan', 'V-Guard Induction Cooktop', 'Helmet', 'Not Qualified']
    scheme_report['Reward Qualification'] = np.select(conditions, values, default='Not Qualified')
    qualified = scheme_report
    return qualified

@st.cache_data(show_spinner=False)
def run_cochin_schem(file1, file2, file3):
    df = pd.concat([file1, file2, file3], ignore_index=True)
    ahm = df[df['Branch'].isin(['Cochin'])]
    ahm = ahm[ahm['Influencer Type'].isin(['Plumbing Expert','Electrical Expert','Electrical and Plumbing Expert'])]
    ahm = ahm[ahm['Product Category'].isin(['MCBs and DBs'])]
    ahm = ahm[ahm['Base Points']>0]
    scheme = ahm.groupby(['Rishta Id', 'State', 'District','DOJ' ,'Branch','Product SubCategory']).agg(
    SG_Scan_Count=('Base Points','count')).unstack('Product SubCategory', fill_value=0)
    scheme.columns = scheme.columns.droplevel(0)
    scheme_report = scheme.reset_index()
    return scheme_report

if st.button('Members Wise Scan Report'):
    data = run_scheme(st.session_state.df1, st.session_state.df2, st.session_state.df3)
    st.success("Scheme generated successfully")
    st.title("Qualified Members Report")
    st.dataframe(data)
    st.divider()
    summary = data.groupby(['Reward Qualification'])['Rishta Id'].count()
    st.title("Rewards Summary")
    st.dataframe(summary)

if st.button('Generate Sub-Category Report'):
    data = run_schem(st.session_state.df1, st.session_state.df2, st.session_state.df3)
    st.toast("Scheme generated successfully")
    st.title("Sub-Category Scanning Report")
    st.dataframe(data)
    st.divider()

if st.button('Cochin Scan Report'):
    data = run_cochin_scheme(st.session_state.df1, st.session_state.df2, st.session_state.df3)
    st.success("Scheme generated successfully")
    st.title("Qualified Members Report")
    st.dataframe(data)
    st.divider()
    summary = data.groupby(['Reward Qualification'])['Rishta Id'].count()
    st.title("Rewards Summary")
    st.dataframe(summary)

if st.button('Generate Cochin Sub-Category Report'):
    data = run_cochin_schem(st.session_state.df1, st.session_state.df2, st.session_state.df3)
    st.toast("Scheme generated successfully")
    st.title("Sub-Category Scanning Report")
    st.dataframe(data)
    st.divider()