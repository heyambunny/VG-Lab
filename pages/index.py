import streamlit as st
import pandas as pd
from route_guard import protect_page
from PIL import Image
csv = ""

logo = Image.open("assets/V-Guard_NewLogo.jpg")
st.sidebar.image(logo, width=150)

# st.image("assets/vguard.png", use_container_width=True)
protect_page("index")
if not st.session_state.get("authenticated"):
    st.switch_page("pages/Login.py")


st.title("XLS to CSV conversion")
st.write("Data upload required to get the correct response")
# st.divider()


# if st.button('Generate'):
#     st.warning('Button Clicked')

# # st.success("Button clicked")

# name = st.text_input("Enter your name")
# if name:
#     st.write(f"Hello! {name}")

# st.divider()
# option = st.selectbox(
#     "Choose an option",
#     ["Branch", "Profession", "Points"]
# )
# if option!="": st.write("Selected:", option)

# agree = st.checkbox("I agree to terms & conditions")

# date = st.date_input("Select a date")
# st.write("Selected date:", date)

# st.divider()

# st.title("CSV Upload + Input Controls")

uploaded_file = st.file_uploader("Upload CSV file", type=["xls", "csv"])
MAX_FILE_SIZE_MB = 500

@st.cache_data(show_spinner=False)
def load_csv_in_chunks(file, chunksize=100_000):
    file.seek(0)
    filename = file.name.lower()

    if filename.endswith(".csv"):
        sep = ","
    elif filename.endswith(".xls"):
        sep = "\t"
    else:
        raise ValueError("Only .csv and .xls files are supported")
    
    chunks = []
    for chunk in pd.read_csv(file, 
        sep=sep,
        engine="c",
        chunksize=chunksize,
        on_bad_lines="skip"):
        chunks.append(chunk)
    return pd.concat(chunks, ignore_index=True)

if uploaded_file:
    if uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        st.error(f"File size exceeds {MAX_FILE_SIZE_MB} MB")
        st.stop()

    with st.spinner("Reading Uploaded file..."):
        df = load_csv_in_chunks(uploaded_file)

    st.success("CSV loaded successfully")
    st.write("Rows:", len(df))
    st.write("Columns:", len(df.columns))
    st.dataframe(df.head(20))
    csv = df.to_csv(index=False)


if st.checkbox('Data is created as per my uploaded files and files are correct as per my knowledge'):
    if csv!="":
        st.download_button(label='⬇ Download CSV',
                   data=csv,
                   file_name='Summary.csv',
                   mime='text/csv')
    else:
        st.warning('File not yet uploaded! Please upload the file and try again.')

# x = st.selectbox('Select', options=[1,2,3,4])
# if x: st.warning(x)