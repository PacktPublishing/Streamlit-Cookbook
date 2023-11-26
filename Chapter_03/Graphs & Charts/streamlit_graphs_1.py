# ----------------4: Creating graphs and charts using Streamlit----------------
import streamlit as st
import pandas as pd

df = pd.read_csv('bestseller-books.csv')
st.write(df.head(5))

st.subheader('User Ratings based on the Genre: Non-Fiction and Fiction')
d1 = df[df["Genre"] == "Non Fiction"]
temp_d1 = d1['User Rating'].value_counts().reset_index()
st.line_chart(temp_d1)

d2 = df[df["Genre"] == "Fiction"]
temp_d2 = d2['User Rating'].value_counts().reset_index()
st.line_chart(temp_d2)
st.write('⚡Findings - :green[**More user ratings for Non-Fiction books!**]')


st.subheader('Relationship between Price and Reviews')
st.area_chart(data=df, x='Price', y='Reviews')
st.write('⚡Findings - :purple[**Most of the Bestsellers are crowded in a lower price range, so cannot conclude much.**]')


st.subheader('Top 10 Authors With Most Bestsellers')
temp = df.groupby('Author').count().reset_index().sort_values('Name',ascending=False).head(10)
st.bar_chart(temp, x='Author', y='Name')
