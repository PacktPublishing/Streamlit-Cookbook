# ----------------7: Using file upload widget----------------
import streamlit as st
import pandas as pd

st.title('File Uploading')

uploaded_file = st.file_uploader("Choose a CSV file")

if uploaded_file is not None:

    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)    # Displays the `vgsales.csv` dataset

# Uploads multiple files----
uploaded_files = st.file_uploader("Select one or more images", accept_multiple_files=True)
for file in uploaded_files:
    st.write("Filename:", file.name)
    st.image(file)
