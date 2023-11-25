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

#----------------------There's more--------------
# Column Configuration API - st.column_config

@st.cache_data
def load_data():
    return pd.DataFrame({
    'Images': [
        "https://images.unsplash.com/photo-1570913149827-d2ac84ab3f9a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=870&q=80",
        "https://images.unsplash.com/photo-1481349518771-20055b2a7b24?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=939&q=80",
        "https://images.unsplash.com/photo-1610917040803-1fccf9623064?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=870&q=80",
        "https://images.unsplash.com/photo-1585827552668-d0728b355e3d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=870&q=80",
        "https://images.unsplash.com/photo-1642372849486-f88b963cb734?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=580&q=80",
        "https://images.unsplash.com/photo-1542820242-a3699d4f2bfe?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=869&q=80",
        "https://images.unsplash.com/photo-1569852118044-f57df8b4f0cf?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=840&q=80",
    ],
    'Fruit': ['Apple', 'Banana', 'Kiwifruit', 'Orange', 'Peach', 'Pear', 'Plums'],
    'Calories(kcal)': [130, 110, 90, 80, 60, 100, 70],
    'Carbs (g)': [34, 30, 20, 19, 15, 26, 19],
    'Fiber (g)': [5, 3, 4, 3, 2, 6, 2],
    'Total Fat(g)': [0, 0, 1, 0, 0.5, 0, 0],
    'Vitamin C(%DV)': [8, 15, 240, 130, 15, 10, 10]
})

st.header('Configuring an Image Column')
df_3 = load_data()
st.dataframe(df_3,
             column_config={
                 "Images": st.column_config.ImageColumn(
                     "Preview", help="fruits"
                )
    },
    hide_index=True,
)
