import streamlit as st
import matplotlib.pyplot as plt
import random

col1,col2 = st.columns([2,1])
if 'user_words' in st.session_state and st.session_state.user_words:
    fig, ax = plt.subplots()
    for word, freq in st.session_state.user_words.items():
        rotation = random.choice([0, 90])  
        color = (random.random(), random.random(), random.random())
        ax.text(random.random(), random.random(), word, fontsize=freq*10, rotation=rotation,alpha=0.9,color=color) # Adjust size factor as per your preference

    ax.axis('off')  
    col1.pyplot(fig)
else:
    st.write("No words entered yet. Please enter some words in the previous page.")