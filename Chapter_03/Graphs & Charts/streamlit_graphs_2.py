# ----------------5: Creating graphs and charts using third party libraries----------------
import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

df = pd.read_csv('bestseller-books.csv')

#------------------Matplotlib Pie Chart------------------
plt.pie([240,310], labels=['Fiction','Non Fiction'], autopct='%.0f%%')
plt.title('Genre Count')
st.pyplot(plt)

#------------------Altair Scatter Plot------------------
a1 = df.groupby('Author').mean().sort_values('Reviews',ascending=False).reset_index().head(10)

st.subheader('AVG. Reviews and Ratings Relationship Of Top 10 Authors')
chart = alt.Chart(a1).mark_circle().encode(x='User Rating', y='Reviews', size='Author', color='Author')
st.altair_chart(chart, use_container_width=True)

#------------------Plotly Treemap------------------
common_books=df['Name'].value_counts()[:7].rename_axis('Common Books').reset_index(name='count')

fig = px.treemap(common_books, path=['Common Books'], values='count')
st.subheader('Top 7 Multiple Times Bestsellers')
st.plotly_chart(fig, use_container_width=True)

#--------Plotly Bar Chart--------
st.subheader('Top 10 highest rated Books and their Authors')
top = df[["Name","Reviews","Author"]].sort_values(by="Reviews")[-10:].reset_index()

fig_1 = px.bar(top, x='Name', y='Reviews', hover_data=['Name', 'Reviews'],
               color='Author', height=400)
st.plotly_chart(fig_1, use_container_width=True)

#------------------Seaborn Swarm Plot------------------
sns_fig = plt.figure(figsize=(15,8))

sns.swarmplot(df, x="Price", y="Genre", hue="Genre")

st.subheader('Pricing based on Genre')
st.write(sns_fig)


#--------Seaborn Barplot--------
st.subheader('Top 10 Highly priced books and their Authors')

top_1 = df[["Name","Price","Author"]].sort_values(by="Price")[-10:].reset_index()

sns_fig_1 = plt.figure(figsize=(20,15))

sns.barplot(x=top_1["Name"],y=top_1["Price"],hue=top_1["Author"])
st.pyplot(sns_fig_1, use_container_width=True)
