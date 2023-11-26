import streamlit as st

audio_file = open('Birds.mp3', 'rb')
audio_bytes = audio_file.read()

st.subheader('Birds Chirping 🐦')
st.audio(audio_bytes, format='audio/mp3')
