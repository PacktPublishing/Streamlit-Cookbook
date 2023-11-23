# ----------------8: Using editable DataFrame----------------

import streamlit as st
import pandas as pd

st.title('Interactive Dataframes')

df = pd.read_csv('fast-food-data.csv')

edited_df = st.data_editor(df.head(5), num_rows="dynamic", key="edited")

st.write('Here is the edited data 👇')
st.write(st.session_state["edited"])   # Displays edited work in the JSON format
