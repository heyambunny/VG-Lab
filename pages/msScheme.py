import streamlit as st
import pandas as pd
import numpy as np
from route_guard import protect_page

protect_page("msScheme")
if not st.session_state.get("authenticated"):
    st.switch_page("pages/Login.py")

st.title("MS Bhubaneswar Scheme")
st.write("Scheme Duration: 01 Nov 2025 to 31 Mar 2026")
st.divider()
c1, c2 = st.columns([1,1])
file_1 = c1.file_uploader('Upload Nov Month File', type=['xls', 'csv'])
file_2 = c2.file_uploader('Upload Dec Month File', type=['xls', 'csv'])

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
    if "df1" not in st.session_state:
        with st.spinner("Reading File 1..."):
            st.session_state.df1 = read_file(file_1)

    if "df2" not in st.session_state:
        with st.spinner("Reading File 2..."):
            st.session_state.df2 = read_file(file_2)

    st.success("Both files loaded successfully")

    st.write(
        "Nov → Total Data:", len(st.session_state.df1),
        "Columns:", len(st.session_state.df1.columns)
    )
    st.write(
        "Dec → Total Data:", len(st.session_state.df2),
        "Columns:", len(st.session_state.df2.columns)
    )

@st.cache_data(show_spinner=False)
def run_scheme(a, b):
    df = pd.concat([a, b], ignore_index=True)
    bhubaneswar = df[df['Branch']=='Bhubaneswar']
    bhubaneswar = bhubaneswar[bhubaneswar['Influencer Type'].isin(['Plumbing Expert','Electrical Expert','Electrical and Plumbing Expert'])]
    bhubaneswar = bhubaneswar[bhubaneswar['Product Category'].isin(['Modular Switches'])]
    bhubaneswar = bhubaneswar[bhubaneswar['Base Points']>0]
    scheme = bhubaneswar.groupby(['Rishta Id', 'Member name', 'Mobile Number', 'State', 'District', 'Branch']).agg(
    Total_Base_Points=('Base Points','sum'))
    scheme_report = scheme.reset_index()
    conditions = [
    scheme_report['Total_Base_Points'] < 1200,
    (scheme_report['Total_Base_Points'] >= 1200) & 
    (scheme_report['Total_Base_Points'] < 2000),
    (scheme_report['Total_Base_Points'] >= 2000) & 
    (scheme_report['Total_Base_Points'] < 4000),
    (scheme_report['Total_Base_Points'] >= 4000) & 
    (scheme_report['Total_Base_Points'] < 6000),
    scheme_report['Total_Base_Points'] >= 6000
    ]

    values = [
    'Not Qualified',
    'Branded Double Bed Bedsheet worth Rs 1999',
    'Branded Single Bed Blanket worth Rs 2999',
    '1 Nos Safari Trolley Bag worth Rs 9999',
    '1 Nos 350w Bosch Drilling Machine'
    ]
    scheme_report['Gift Qualification'] = np.select(conditions, values, default='Not Qualified')
    qualified = scheme_report[~scheme_report['Gift Qualification'].isin(['Not Qualified'])]
    return qualified

if st.button("Generate"):
    qualified_df = run_scheme(
        st.session_state.df1,
        st.session_state.df2
    )
    st.success("Scheme Report Generated Successfully")
    st.title("Qualified Members Report")
    st.dataframe(qualified_df)
    st.divider()
    summary = qualified_df.groupby(['Gift Qualification']).agg(Members_Count=('Rishta Id','count'), Total_base_Points=('Total_Base_Points','sum'))
    st.title("Gifts Summary")
    st.dataframe(summary)


