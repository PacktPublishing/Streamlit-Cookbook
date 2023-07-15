import streamlit as st

# Initialize the session state for 'button_pressed' if it's not already initialized
if 'button_pressed' not in st.session_state:
    st.session_state.button_pressed = False

# Create a button
if st.button('Toggle button',key="button_key"):
    # Change the value of 'button_pressed' in the session state
    st.session_state.button_pressed = not st.session_state.button_pressed  # Toggle the boolean value

# Display the current state of the button
#st.write(f"Button state: {'Pressed' if st.session_state.button_pressed else 'Not Pressed'}")
if st.session_state.button_pressed:
    st.write("pressed")
else:
    st.write("Not pressed")
