import streamlit as st
import pandas as pd
import numpy as np
from route_guard import protect_page

protect_page('Hafele Sales Report')

st.set_page_config(
    page_title="Sales Team Report",
    layout="wide")

st.header('Hafele Sales Team Report')

st.divider()

if "df1" not in st.session_state:
    st.session_state.df1 = None
if "df2" not in st.session_state:
    st.session_state.df2 = None
if "df3" not in st.session_state:
    st.session_state.df3 = None
if "df4" not in st.session_state:
    st.session_state.df4 = None
if "df5" not in st.session_state:
    st.session_state.df5 = None


f1,f2,f3 = st.columns([1,1,1])
file_1 = f1.file_uploader('Upload Product Wise Report (Jan 22 to Dec 24)', type=['csv'])
file_2 = f2.file_uploader('Upload Product Wise Report (Jan 25 to Dec 25)', type=['csv'])
file_3 = f3.file_uploader('Upload Product Wise Report (Jan 26 to till date)', type=['csv'])

c1,c2 = st.columns([1,1])
file_4 = c1.file_uploader('Upload Enrolment Report', type=['csv'])
file_5 = c2.file_uploader('Upload Login Report', type=['csv'])

def read_file(file):
    file.seek(0)

    chunks = []
    for chunk in pd.read_csv(file,
                             engine='c',
                             chunksize=300_000):chunks.append(chunk)
    return pd.concat(chunks, ignore_index=True)

if file_1 and file_2 and file_3 and file_4 and file_5:
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
        with st.spinner("Reading file 2...."):
            st.session_state.df4 = read_file(file_4)

    if st.session_state.df5 is None:
        with st.spinner("Reading file 3...."):
            st.session_state.df5 = read_file(file_5)
    st.success("All files loaded successfully")

@st.cache_data(show_spinner=False)
def run_fun(tr1, tr2, tr3, df, login ):
    transactions = pd.concat([tr1, tr2, tr3], ignore_index=True)
    transactions['Member Mobile'] = transactions['Member Mobile'].astype(str)
    df = df.drop(columns=['DOB', 'Marital Status', 'Anniversary Date', 'Delivery Address',
            'Pincode', 'Email ID', 'WhatsApp Mobile','Permanent Address', 'Aadhar Number', 'Pan Number', 'Upi Id'
             ,'Account Type', 'Ifsc', 'Bank Name', 'Bank Account No', 'Holder Name','Branch Name', 'Profession', 'Contractor Mobile', 'Team Size','No Of Supervisors', 'Annual Business In Lacs', 'Major Brands','Types Of Products', 'Value Of Products', 'Types Of Projects','Solution Category', 'Dealer1', 'Dealer2', 'Dealer3', 'Sub Dealer'])
    df = df[~df['Validation Status'].isin(['DELETED'])]
    df = df[~df['Registration Id'].isin([16068, 62621, 71156, 71166, 72936, 72937, 72940, 74651, 75288])]
    df = df.rename(columns={
    'Redeemption': 'Redemption Status'})
    df['Redemption Status'] = df['Redemption Status'].replace({
    'OPEN': 'Unblock',
    'CLOSE': 'Block'})
    transactions['scan_date'] = pd.to_datetime(transactions['Date of Scan'], errors='coerce')

    last_scan_df = (
    transactions.groupby('Member Mobile', as_index=False)['scan_date']
           .max()
          .rename(columns={'scan_date': 'last_scan_date'})
    )
    new_df = df.merge(
    last_scan_df,
    on='Member Mobile',
    how='left'
    )
    today = pd.Timestamp.now().normalize()
    new_df['days_since_last_scan'] = (today - new_df['last_scan_date'].dt.normalize()).dt.days
    new_df['Status'] = np.where(
    new_df['last_scan_date'].isna(),
    'Inactive',
    np.where(
        new_df['days_since_last_scan'] <= 30,
        'Active',
        'Dormant'))
    new_df = new_df.merge(
    login[['Member Mobile', 'Total Points Earned', 'Total Points Redeemed']],
    on='Member Mobile',
    how='left')
    
#-------------------------------------------------------------------------------------
    cutoff_date = pd.Timestamp.now().normalize() - pd.Timedelta(days=30)
   # calculate earnings in last 90 days
    last_30_earnings = (
    transactions[transactions['scan_date'] >= cutoff_date]
    .groupby('Member Mobile', as_index=False)['Points ']
    .sum()
    .rename(columns={'Points ': 'Total Earn Points L 30 D'})
    )
    # merge into new_df
    new_df = new_df.merge(last_30_earnings,on='Member Mobile',how='left')

#-------------------------------------------------------------------------------------
    final = new_df[['Member Name', 'Member Mobile', 'Registration Date', 'Registration Id', 'Redemption Status',
       'State', 'District', 'City', 'Sales Executive Name',
       'Area Manager Name', 'RSM Manager Name', 'Approval/Rejection Date',
       'Validation Status', 'Region', 'Registration type',
       'Status', 'Total Points Earned', 'Total Points Redeemed',
       'Total Earn Points L 30 D']]
    final = final.rename(columns={
        'Total Points Earned':'Total Points Earned Till Date',
        'Total Points Redeemed':'Total Points Redeemed Till Date'
    })
    final['Last 30 Days Active'] = np.where(
    final['Total Earn Points L 30 D'].fillna(0) > 0,
    'Active',
    'Inactive')
    return final


if st.button('Generate Report'):
    data = run_fun(st.session_state.df1, st.session_state.df2, st.session_state.df3, st.session_state.df4, st.session_state.df5)
    st.success("Report generated successfully")
    st.dataframe(data)
    csv = data.to_csv(index=False)
    if csv!="":
        st.download_button(label='⬇ Download CSV',
                   data=csv,
                   file_name='Sales Team Summary Report.csv',
                   mime='text/csv')
    else:
        st.warning('File not yet uploaded! Please upload the file and try again.')

