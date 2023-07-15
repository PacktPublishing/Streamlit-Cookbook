import streamlit as st

st.title('Temperature Converter')

def convert_temperature(temp, conversion):
    if conversion == 'Celsius to Fahrenheit':
        converted_temp = temp * 9/5 + 32
    elif conversion == 'Fahrenheit to Celsius':
        converted_temp = (temp - 32) * 5/9
    st.session_state.converted_temp = round(converted_temp, 2)

if 'converted_temp' not in st.session_state:
    st.session_state.converted_temp = 0

conversion = st.selectbox("Select your conversion", ['Celsius to Fahrenheit', 'Fahrenheit to Celsius'])
temp = st.number_input("Enter the temperature to convert", min_value=-100, max_value=100, value=0)

st.button('Convert Temperature', on_click=convert_temperature, args=(temp,), kwargs={'conversion': conversion})

st.write('The converted temperature is: ', st.session_state.converted_temp)