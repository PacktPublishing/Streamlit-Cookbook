import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from google.cloud import bigquery
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.title(':violet[Streamlit + BigQuery Connection]')

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
  
    # Convert to a list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows


rows = run_query("SELECT * FROM `aerial-form-397913.ds_salaries.ds_salary_details` LIMIT 15;")

st.header("Our Data 👀")
st.dataframe(rows)
st.write("---")

# Uses pandas-gbq package to read the data directly from the CSV file
query = "SELECT employee_residence FROM `aerial-form-397913.ds_salaries.ds_salary_details`;"
df = pd.read_gbq(query, credentials=credentials)

st.header("Employee's Origins 👨‍💼")
data = df['employee_residence'].value_counts().index[:11]
sns_fig = plt.figure(figsize=(20,10))
sns.countplot(x=df["employee_residence"], order=data)
st.pyplot(sns_fig)

st.subheader("Data Scientists from North America 🌎")

chart_1 = px.choropleth(data_frame = df["employee_residence"].value_counts(),
                    locations=df["employee_residence"].value_counts().index,
                    locationmode="country names", 
                    color=df["employee_residence"].value_counts().values,
                    height= 600,scope="north america",
                    labels={"color":"Data Scientist","locations":"Country"})
st.plotly_chart(chart_1)

st.subheader("Data Scientists from Europe 🌍")

chart_2 = px.choropleth(data_frame = df["employee_residence"].value_counts(),
                    locations=df["employee_residence"].value_counts().index,
                    locationmode="country names", 
                    color=df["employee_residence"].value_counts().values,
                    height= 600,scope="europe",
                    labels={"color":"Data Scientist","locations":"Country"})
st.plotly_chart(chart_2)
