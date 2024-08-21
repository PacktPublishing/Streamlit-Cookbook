import streamlit as st

name = st.query_params.get("name", "Anonymous")
st.header(f"Hello {name.title()}!", divider="rainbow", anchor=False)
