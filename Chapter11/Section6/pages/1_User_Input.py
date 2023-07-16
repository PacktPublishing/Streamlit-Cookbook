import streamlit as st
from collections import Counter

st.title('Word Cloud in Streamlit')

user_input = st.text_input("Enter some words")

if user_input:
    if 'user_words' not in st.session_state:
        st.session_state.user_words = Counter(user_input.split())
    else:
        st.session_state.user_words.update(user_input.split())
    
    st.success("Words saved. Check out the word Cloud in the next page.")
