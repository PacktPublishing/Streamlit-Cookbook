import streamlit as st

# ----------------6: Using button and Download button----------------

st.title('Interactive Buttons')

birth_year = st.slider('Which year were you born?',
            min_value=1900, max_value=2023)
if st.button('Check your age'):
    age = 2023 - birth_year
    st.write(f"You are **{age}** years old.")

with open("icecream.jpg", "rb") as file:
    st.download_button(
        label="Download an image",
        data=file,
        file_name="icecream.jpg",
        mime="image/jpg"
        )

with open("Python-book.pdf", "rb") as file_1:
    st.download_button(
        label="Download a PDF",
        data=file_1,
        file_name="Python-book.pdf",
        mime='text/pdf',
    )

#----------------------There's more--------------
# ---A: Stateful button---

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

st.button('Click me', on_click=click_button)

if st.session_state.clicked:
    st.write('Button clicked!')

# ---B: Toggle button---

if 'button' not in st.session_state:
    st.session_state.button = False

def click_toggle():
    st.session_state.button = not st.session_state.button

st.button('Click me for magic!', on_click=click_toggle)

if st.session_state.button:
    st.subheader(':violet[A subheader in violet color]')
else:
    st.subheader('A normal subheader')
