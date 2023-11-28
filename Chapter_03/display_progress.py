# ----------------10: Displaying status/progress----------------
import streamlit as st
from time import sleep

st.title("General Quiz!")

st.info('On every correct guess the progress bar updates itself!')

capital = st.selectbox(
    "What is the capital city of Egypt?",
    ('Luxor', 'Cairo', 'Giza'))

if capital == 'Luxor':
    st.warning('Try once again as you are near the right answer.')
elif capital == 'Cairo':
    st.success('Correct!', icon="✅")
elif capital == 'Giza':
    st.error('Incorrect 👎')
else:
    st.write('')


day = st.radio(
    "Which day is observed as the 'International Literacy Day'?",
    ('Nov 28', 'Sept 22', 'Sept 8'))
if day == 'Nov 28':
    st.warning('Try once again as you are near the right answer.')
elif day == 'Sept 22':
    st.error('Incorrect 👎')
elif day == 'Sept 8':
    st.success('Correct!', icon="✅")
else:
    st.write('')

# Stores the "progress" in a session state that keeps track of the completed questions
st.session_state["progress"] = st.session_state.get("progress", 0)
bar = st.progress(st.session_state["progress"], text="Quiz in progress...")  # Displays the progress bar

# Checks whether the answer selected by the user matches or not, and if it does, then increase the "progress" value count by 50
if capital == 'Cairo':
    st.session_state["progress"] = min(100, st.session_state["progress"] + 50)
    bar.progress(st.session_state["progress"], text="Progress: {}%".format(st.session_state["progress"]))

# The balloons pop up once the quiz is complete
if st.session_state["progress"] == 100:
    sleep(2)
    st.balloons()


st.subheader('Spinner Widget')
if st.button('Click to load image'):
    with st.spinner('Please wait...'):
        sleep(2)
    st.image("icecream.jpg")
    st.success('Done!')
