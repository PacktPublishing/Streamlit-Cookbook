# ----------------2: Handling text----------------
import streamlit as st
import pandas as pd

st.title('Text Widgets 🔤')

st.header(':blue[Pandas]: About the Library')
st.subheader('An open-source Python tool for data analysis and manipulation')

st.text("""It can handle reading and writing data between in-memory data structures &
different formats such as CSV, TXT, XLSX, etc. Can perform data alignment,
manipulates messy data into an orderly form, and more.""")

st.markdown("### :orange[Install Pandas simply with -] `$ pip install pandas`")

# Magic function st.write
st.write('# st.write() Magic 🤩')
st.write(f"""Hey! This is James from Prague and I'm **{2023-1992}** years old.
            \nGiven below presents the nutritional data from fruits I love to eat 👇""")

st.write(pd.DataFrame({
    'Fruit': ['Apple', 'Banana', 'Kiwifruit', 'Orange', 'Peach', 'Pear', 'Plums'],
    'Calories(kcal)': [130, 110, 90, 80, 60, 100, 70],
    'Carbs (g)': [34, 30, 20, 19, 15, 26, 19],
    'Fiber (g)': [5, 3, 4, 3, 2, 6, 2],
    'Total Fat(g)': [0, 0, 1, 0, 0.5, 0, 0],
    'Vitamin C(%DV)': [8, 15, 240, 130, 15, 10, 10]
}))
