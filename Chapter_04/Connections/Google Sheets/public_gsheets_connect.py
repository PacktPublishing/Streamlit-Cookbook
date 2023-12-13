import streamlit as st
from streamlit_gsheets import GSheetsConnection

url = "https://docs.google.com/spreadsheets/d/xxxxx/edit?usp=sharing"  # Enter your copied Gsheets public URL

conn = st.experimental_connection("gsheets", type=GSheetsConnection)
df = conn.read(spreadsheet=url)

st.title(':green[Streamlit + Public Google Sheets 🔌]')

st.header('Glimpse of the Data 👀')
st.dataframe(df.head(15))
