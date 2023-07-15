import streamlit as st

if "counter" not in st.session_state:
    st.session_state.counter = 0

def add_number(num):
    st.session_state.counter += num

number = st.number_input("Number to add:",step=1)

button = st.button("Add number", on_click=lambda: add_number(number))

st.write(st.session_state.counter)
