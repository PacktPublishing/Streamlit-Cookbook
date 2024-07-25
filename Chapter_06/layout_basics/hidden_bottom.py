import streamlit as st

st.title("Main body")
st.write("A bunch of repeated text 🐍 " * 500)

with st._bottom:
    with st.popover("**`st._bottom` is always visible!**", use_container_width=True):
        st.markdown("👻 Surprise 👻")

