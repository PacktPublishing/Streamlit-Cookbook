import streamlit as st

if 'button_pressed' not in st.session_state:
    st.session_state.button_pressed = False

if st.button('Toggle button',key="button_key"):
    st.session_state.button_pressed = not st.session_state.button_pressed  

if st.session_state.button_pressed:
    st.write("pressed")
else:
    st.write("Not pressed")