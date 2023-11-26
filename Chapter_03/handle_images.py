# ----------------6: Displaying images----------------
import streamlit as st
import numpy as np
from PIL import Image
import cv2

st.title('Beautiful Images')

# Image displays from a local path---
st.subheader('Image from a `local path`')
st.image("icecream.jpg", caption='Pinky Popsicles')

# Image converted to grayscale using NumPy & Pillow---
original_img = Image.open("icecream.jpg")
demo = np.array(original_img)
converted_img = cv2.cvtColor(demo, cv2.COLOR_BGR2GRAY)

st.subheader('Image converted to `gray scale`')
st.image(converted_img)

# Images from Unsplash---
st.subheader(':orange[Unsplash Image URL]')
st.image("https://images.unsplash.com/photo-1531594652722-292a43e752b4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1331&q=80")

st.subheader(':blue[Unsplash Image sets the image width to `column width`]')
st.image('https://images.unsplash.com/photo-1494390248081-4e521a5940db?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8aGVhbHRoeSUyMGJyZWFrZmFzdHxlbnwwfHwwfHx8Mg%3D%3D&auto=format&fit=crop&w=500&q=60')

st.image("https://images.unsplash.com/photo-1494390248081-4e521a5940db?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8aGVhbHRoeSUyMGJyZWFrZmFzdHxlbnwwfHwwfHx8Mg%3D%3D&auto=format&fit=crop&w=500&q=60",
         use_column_width=True)

#----------------------There's more--------------
img_size = st.slider('Select width size for the below image', 100 , 600)
st.image("icecream.jpg", width=img_size)
