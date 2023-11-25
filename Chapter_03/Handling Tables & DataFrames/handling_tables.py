import streamlit as st
import pandas as pd

st.title('Tables and DataFrames')
df = pd.read_csv('exams.csv')
df_1 = pd.read_excel('student_exams.xls')
df_2 = pd.read_excel('student_exams_1.xlsx')

st.header('st.table displaying `.csv` file')
st.table(df.head(5))

st.header('st.table displaying `.xls` file')
st.table(df_1.head(5))

# Feature 1 - Uses container width
@st.cache_data
def load_data():
    return pd.DataFrame({
        'Fruit': ['Apple', 'Banana', 'Kiwifruit', 'Orange', 'Peach', 'Pear', 'Plums'],
        'Calories(kcal)': [130, 110, 90, 80, 60, 100, 70],
        'Carbs (g)': [34, 30, 20, 19, 15, 26, 19],
        'Fiber (g)': [5, 3, 4, 3, 2, 6, 2],
        'Total Fat(g)': [0, 0, 1, 0, 0.5, 0, 0],
        'Vitamin C(%DV)': [8, 15, 240, 130, 15, 10, 10]
})

st.checkbox("Use container width", value=False, key="use_container_width")

df_3 = load_data()
st.dataframe(df_3,
    use_container_width=st.session_state.use_container_width)

# Uses container width along with 'hide_index=True' parameter
df_3 = load_data()
st.dataframe(df_3,
    use_container_width=st.session_state.use_container_width,
    hide_index=True,
)

# Feature 2 - Pandas styler highlight
st.dataframe(df_2.head(10).style.highlight_max(axis=0))

# Feature 3 - For highlighting additional UI features
st.dataframe(df_2.head(10))
