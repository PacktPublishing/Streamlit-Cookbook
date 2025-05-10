import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.title(':blue[Streamlit + MySQL Connection]')

# Initialize connection.
conn = st.connection('mysql', type='sql')

# Perform query.
df = conn.query('SELECT * FROM ds_salary_details;', ttl=600)

st.header('Our Data 👀')
st.dataframe(df.head(5))
st.write("---")

st.header("Data Scientist's Employment Type")
sns_fig = plt.figure(figsize=(20, 10))
sns.countplot(y=df["employment_type"],
              order=df["employment_type"].value_counts().index)
st.pyplot(sns_fig)


st.subheader("Data Scientist's Salary On Employment Type")
sns_fig_1 = plt.figure(figsize=(20, 10))
sns.violinplot(x=df["employment_type"],
              y=df["salary_in_usd"],
              order=df["employment_type"].value_counts().index)
st.pyplot(sns_fig_1)
st.write("---")


st.header("Company Size 🏢")
sns_fig_2 = plt.figure(figsize=(20, 10))
sns.countplot(y=df["company_size"],
              order=df["company_size"].value_counts().index)
st.pyplot(sns_fig_2)


st.subheader("Data Scientist's Salary On Company Size")
sns_fig_3 = plt.figure(figsize=(20, 10))
sns.violinplot(x=df["company_size"],
              y=df["salary_in_usd"],
              order=df["company_size"].value_counts().index)
st.pyplot(sns_fig_3)
