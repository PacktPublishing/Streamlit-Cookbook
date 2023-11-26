import streamlit as st

video_file = open('Earth.mp4', 'rb')
video_bytes = video_file.read()

st.subheader('Video on Earth 🌏')
st.video(video_bytes, format='video/mp4')

st.subheader('YOUTUBE Video')
st.video("https://www.youtube.com/watch?v=GlWNuzrqe7U")
