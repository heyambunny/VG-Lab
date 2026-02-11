import streamlit as st
import pandas as pd
from route_guard import protect_page

protect_page('Sfdc Data Check')

if 'df1' not in st.session_state:
    st.session_state.df = None

file_1 = st.file_uploader('Upload SFDC File')

def read_file(file):
    file.seek(0)

    chunks=[]
    for chunk in pd.read_csv(file,
                            sep='\t',
                            engine='c',
                            chunksize=100_000):chunks.append(chunk)
    return pd.concat(chunks, ignore_index=True)

if file_1:
    if st.session_state.df1 is None:
        with st.spinner('Reading file....'):
            st.session_state.df1 = read_file(file_1)

        st.toast('File has been uploaded successfully')

data = st.session_state.df1
st.dataframe(data.head())

csv = data.to_csv(index=False)
st.download_button("Download CSV File",
                   csv,
                   'Retailer Transaction Report - 29 Dec.csv')