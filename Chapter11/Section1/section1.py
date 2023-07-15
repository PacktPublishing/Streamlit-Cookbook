import streamlit as st

if 'key'  not in st.session_state:
    st.session_state['key']="value"
    
if 'list' not in st.session_state:
    st.session_state.list = []

st.text_input("Your name", key="name")
st.slider('Select a number',key='number')
'''Session state content:'''
st.session_state
