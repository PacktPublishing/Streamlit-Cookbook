import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pymongo

st.title(':green[Streamlit + MongoDB Connection]🔌')

# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection(): # Replace <password> with yours in the connection string
    return pymongo.MongoClient("mongodb+srv://shru-mongo:<password>@cluster0.z3fbunv.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp")

client = init_connection()

# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data():
    db = client["Salaries"]
    collection = db["ds_salary_details"]
    res = collection.find()
    items = list(res)  # makes it hashable for st.cache_data
    return items

data = get_data()
df = pd.DataFrame(data)

st.header('Our Data 👀')
st.dataframe(df.head(5))
st.write("---")

st.header("Data Scientist's Salary Distribution")
sns_fig = plt.figure(figsize=(20, 10))
sns.histplot(df["salary_in_usd"],
             kde=True, bins="auto",
             alpha=1,fill=True,edgecolor="black")
st.pyplot(sns_fig)


st.subheader('Highest paid Data Science Job Roles 💸')
data_high = df.copy()
data_high = pd.DataFrame(data_high.groupby("job_title")["salary_in_usd"].max())
sns_fig_1 = plt.figure(figsize=(20, 10))
sns.barplot(x=data_high["salary_in_usd"],
            y=data_high.index,
            order=data_high.sort_values("salary_in_usd",ascending=False).index[:11])
st.pyplot(sns_fig_1)


st.subheader('Year-wise Avgerage Salary Timeline')
data_timeline = pd.DataFrame(df.groupby("work_year")["salary_in_usd"].mean())
data_timeline = data_timeline.reset_index()
data_timeline["work_year"].replace({2020:"2020",2021:"2021",2022:"2022"},inplace=True)
sns_fig_2 = plt.figure(figsize=(20,10))
sns.lineplot(x=data_timeline["work_year"],
             y=data_timeline["salary_in_usd"],
             data=data_timeline)
st.pyplot(sns_fig_2)
st.write("---")


st.header("Data Scientist's Experience Level")
sns_fig_3 = plt.figure(figsize=(20, 10))
sns.countplot(y=df["experience_level"],
              order=df["experience_level"].value_counts().index)
st.pyplot(sns_fig_3)


st.subheader("Data Scientist's Salary On Experience Level 💸")
sns_fig_4 = plt.figure(figsize=(20, 10))
sns.violinplot(x=df["experience_level"],
              y=df["salary_in_usd"],
              order=df["experience_level"].value_counts().index)
st.pyplot(sns_fig_4)
