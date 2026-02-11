import streamlit as st
import pandas as pd
from route_guard import protect_page
protect_page("Retailer Points")

if "df1" not in st.session_state:
    st.session_state.df1 = None
if "df2" not in st.session_state:
    st.session_state.df2 = None
if "df3" not in st.session_state:
    st.session_state.df3 = None

st.title('Retailer Points Summary')
st.divider()

p1, p2, p3 = st.columns([1,1,1])
file_1 = p1.file_uploader('Upload Apr to Aug Month File', type=['xls', 'csv'])
file_2 = p2.file_uploader('Upload Sep Month File', type=['xls', 'csv'])
file_3 = p3.file_uploader('Upload Oct to Dec Month File', type=['xls', 'csv'])

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

if file_1 and file_2 and file_3:
    if st.session_state.df1 is None:
        with st.spinner("Reading File 1..."):
            st.session_state.df1 = read_file(file_1)

    if st.session_state.df2 is None:
        with st.spinner("Reading File 2..."):
            st.session_state.df2 = read_file(file_2)

    if st.session_state.df3 is None:
        with st.spinner("Reading File 3..."):
            st.session_state.df3 = read_file(file_3)

    st.success("All files loaded successfully")

    st.write(
        "Apr - Aug → Total Data:", len(st.session_state.df1),
        "Columns:", len(st.session_state.df1.columns)
    )
    st.write(
        "Sep → Total Data:", len(st.session_state.df2),
        "Columns:", len(st.session_state.df2.columns)
    )
    st.write(
        "Oct - Dec → Total Data:", len(st.session_state.df3),
        "Columns:", len(st.session_state.df3.columns)
    )

@st.cache_data(show_spinner=False)
def run_scheme(a, b, c):
    df = pd.concat([a, b, c], ignore_index=True)
    points = df.groupby(['RetailerRishtaID'])['Total Points'].sum()
    return points

if st.button("Generate"):
    points = run_scheme(
        st.session_state.df1,
        st.session_state.df2,
        st.session_state.df3
    )
    st.success("Data generated successfully")
    st.title("Points Summary")
    st.dataframe(points)

