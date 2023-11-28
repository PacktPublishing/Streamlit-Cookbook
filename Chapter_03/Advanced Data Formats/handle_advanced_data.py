# ----------------11: Handling advanced data formats----------------
import streamlit as st
import json
import xml.etree.ElementTree as ET

#------------------JSON------------------
# Loads JSON data from a file
with open('covid_data.json') as json_file:
    data = json.load(json_file)

# Displays data from the JSON file
st.subheader("COVID-19 Statistics")
st.json(data)

st.subheader("Pretty-printed JSON string")
st.json({
    'veggies': 'cabbage',
    'pulses': 'green peas',
    'fruits': [
        'apple',
        'banana',
        'watermelon',
        'berries',
    ],
})

#------------------XML------------------
# Creates a `tree` object and parses data from the XML file
tree = ET.parse('users.xml')

# Extracts root specific data for all user's records
root = tree.getroot()

# To extract every detail for each user
st.subheader("XML Data Handling")

for user in root.findall('user'):
    name = user.find('name').text
    age = user.find('age').text
    
    address = user.find("address")
    street = address.find("street").text
    city = address.find("city").text
    country = address.find("country").text
    
    st.write('**Name:**', name)
    st.write('**Age:**', age)
    st.write('**Address:**', street + ', ' + city + ', ' + country)
    st.divider()
