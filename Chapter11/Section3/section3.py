import streamlit as st

if "conversation" not in st.session_state:
    st.session_state.conversation = []

chat = st.chat_input("Start a conversation please")

if chat:
    st.session_state.conversation.append(chat)
    
for line in st.session_state.conversation:
    st.write(line)