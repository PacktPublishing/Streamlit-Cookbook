import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('BMI Calculator for Multiple Users')

if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
col1,col2,col3 = st.columns([3,0.3,6])
with col1:
    with st.form(key='bmi_form'):
        user_name = st.text_input("What's your name?")
        weight = st.number_input("Enter your weight (in kg): ", min_value=0.0)
        height = st.number_input("Enter your height (in meters): ", min_value=0.0)
        submit_button = st.form_submit_button(label='Calculate BMI')

if submit_button and user_name and weight and height:
    bmi = weight / (height ** 2)
    st.session_state.user_data[user_name] = bmi
    st.write(f"{user_name}, your BMI is: {bmi:.2f}")

if st.session_state.user_data:
    user_df = pd.DataFrame.from_dict(st.session_state.user_data, orient='index', columns=['BMI'])
    fig, ax = plt.subplots()
    user_df.plot(kind='bar', legend=False, ax=ax)
    ax.set_xlabel("User")
    ax.set_ylabel("BMI")
    col3.pyplot(fig)





