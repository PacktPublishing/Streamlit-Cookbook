import streamlit as st
# ----------------1: Using text/number input and Text area----------------

st.title('Dining Experience at a Restaurant')
name = st.text_input('Please enter your name', '')

age = st.number_input('How old are you? (AGE)', min_value=15, max_value=100)

likeness = st.text_area('What was the best part of your visit?',
'''Explain in a few words...''',max_chars=300)

feedback = st.text_area('Please share your comments or concerns (OPTIONAL)', '''N/A''')

st.subheader("Responses")
st.write(f"**Guest's Name**: {name}\n\n**Age**: {age}")
st.write(f"**Best part**: {likeness}\n\n**Comments**: {feedback}")

#------------------------------------------------------------------------------
# ----------------2: Using radio buttons----------------

find = st.radio(
    "How did you hear about us?",
    ('Facebook', 'Instagram', 'Search engines', 'Word of Mouth', 'Other'))

visit = st.radio("Was this your first time at the restaurant?",
                 ('Yes', 'No'),
                 index=1)

st.write(f"**You found us through**: {find}\n\n**First time visit**: {visit}")

#----------------------There's more--------------
if "show" not in st.session_state:
    st.session_state.horizontal = False

st.checkbox("Not visiting for the first time?", key="horizontal")
    
often = st.radio(
        "How often do you visit restaurants?",
        ["Everyday", "Once a week", "Once a month"],
        key="show",
        horizontal=st.session_state.horizontal,
)

st.write(f"**Often visits**: {often}")

#------------------------------------------------------------------------------
# ----------------3: Using checkboxes----------------

st.write("What things attracted you more to our restaurant?")
c1 = st.checkbox("Variety in menu")
c2 = st.checkbox("Quick service")
c3 = st.checkbox("Easy to locate")

if c1 & c2 & c3:
    st.write("Thanks for all the love! 🤗")
elif c1 | c2 | c3:
    st.write("*We will work on your feedback.*")
else:
    st.write("Please select one or more options 👆")

#------------------------------------------------------------------------------
# ----------------4: Using select and multiselect boxes----------------

areas = st.selectbox(
    'Select areas to answer further questions:',
    ('', 'Food & Drink', 'Facilities', 'Services'))

if areas == 'Food & Drink':
    drink = st.radio("Were you pleased with our drink offerings?", ('Yes', 'No'))

    dishes = st.multiselect(
    'Which among the following are your favorite dishes?',
    ['Risotto', '🧇Chicken & Waffles', '🍔Cheeseburger & fries', 
     'Fancy Iced Tea', '🍝Spaghetti', 'Virgin Piña Colada',
     '🍕Pizzas'])
    
    st.write("Drinks satisfaction: ", drink)
    st.write('*Your favorites:*', dishes)

elif areas == 'Facilities':
    st.write("What is the main problem you faced at our restaurant?")
    ch1 = st.checkbox("Uncomfortable seats")
    ch2 = st.checkbox("Hygiene problems")
    ch3 = st.checkbox("Wrong order received")
    ch4 = st.checkbox("No complains!")

    if ch1 & ch2 & ch3:
        st.write("Sorry for the inconvenience you faced! 🙏")
    elif ch1 | ch2 | ch3:
        st.write("Thanks! We will work on improving our facilities.")
    elif ch4:
        st.write("*Glad you liked our facilities!*")
    else:
        st.write("Please select one or more options 👆")

elif areas == 'Services':
    s1 = st.radio("Was the service friendly and welcoming?",
                  ('Yes', 'No'))
    s2 = st.radio("Did your server handle the food well?",
                  ('Yes', 'No'))

    st.write(f"**Service friendly?** {s1}\n\n**Food handling:** {s2}")

else:
    st.write("Please select an option 👆")

#------------------------------------------------------------------------------
# ----------------5: Using sliders and range sliders----------------

recommend = st.slider('How likely is it that you would recommend our restaurant to a friend or colleague?', 1, 10, 7)
st.write('Indicates -- *0: Not at all likely;  10: Extremely likely*')

st.subheader('Please rate our restaurant based on three categories ⭐')

food_rating = st.slider("Food & Drink 🍸", min_value=0.0, max_value=5.0, step=0.5, value=(3.5, 5.0))
facility_rating = st.slider("Facilities (includes hygiene, etc.)", min_value=0.0, max_value=5.0, step=0.5, value=(2.5, 4.0))
service_rating = st.slider("Services (includes quick order, etc.)", min_value=0.0, max_value=5.0, step=0.5, value=(2.5, 3.0))

st.write(f"**Restaurant likeliness**: {recommend}")

# Responses displayed----
st.subheader('Average Ratings')
st.write(f"**Food & Drink**: {(sum(food_rating)/2):.2f} / 5⭐")
st.write(f"**Facilities**: {(sum(facility_rating)/2):.2f} / 5⭐")
st.write(f"**Services**: {(sum(service_rating)/2):.2f} / 5⭐")

#----------------------There's more--------------
from datetime import time, datetime

scheduled = st.slider("Schedule your table time:",
    min_value=time(4,30),
    max_value=time(11,00))

book_table = st.slider(
    "Select the day of your visit based on your table scheduled",
    min_value=datetime(2023, 7, 25, 11, 00),
    max_value=datetime(2023, 8, 2, 11, 00),
    format="MM/DD/YY - hh:mm")


fruit = st.select_slider(
    'Select your favorite fruit',
    options=['🍎Apple', '🍊Orange', '🍍Pineapple', '🍉Watermelon', '🍒Cherries', '🍇Grapes'])

start_color, end_color = st.select_slider(
    'Select a range of color wavelength',
    options=['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'],
    value=('red', 'blue'))

# Responses displayed----
st.write("You're scheduled for:", scheduled)
st.write("Your day of visit:", book_table)
st.write('Your favorite fruit:', fruit)
st.write('*You selected wavelengths between*', start_color, '*and*', end_color)
