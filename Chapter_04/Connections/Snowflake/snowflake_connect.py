import streamlit as st
import pandas
import matplotlib.pyplot as plt
import seaborn as sns

st.title(':blue[Streamlit + Snowflake Connection❄]')

# Initialize connection.
conn = st.connection('snowflake')

# Perform query.
df = conn.query('SELECT * from DS_SALARY_DETAILS;', ttl=600)

st.header('Our Data 👀')
st.dataframe(df.head(5))
st.write("---")

st.header("Data Scientist's Remote Job Types")
sns_fig = plt.figure(figsize=(35, 15))
sns.countplot(y=df["REMOTE_RATIO"],
              order=df["REMOTE_RATIO"].value_counts().index)
st.pyplot(sns_fig)


st.subheader("Data Scientist's Salary On Remote Job Types")
sns_fig_1 = plt.figure(figsize=(35, 15))
sns.violinplot(x=df["REMOTE_RATIO"],
              y=df["SALARY_IN_USD"],
              order=df["REMOTE_RATIO"].value_counts().index)
st.pyplot(sns_fig_1)
