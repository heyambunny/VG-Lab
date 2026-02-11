import streamlit as st
import pandas as pd
from database import get_conn

st.title("Daily Data Import")

conn = get_conn()

file = st.file_uploader("Upload CSV", type=["csv",'xls'])

if st.button("Import Data"):
    if file is None:
        st.warning("Please upload a file")
    else:
        file.seek(0)
        df = pd.read_csv(file,sep="\t")

        # tracking columns (recommended)
        df["source_file"] = file.name
        df["import_date"] = pd.Timestamp.today().date()

        df.to_sql(
            "transactions",
            conn,
            if_exists="append",
            index=False
        )

        st.success("Data added successfully")
