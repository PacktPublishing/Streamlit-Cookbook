import streamlit as st
from st_files_connection import FilesConnection
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.title(':orange[Streamlit + AWS S3 Connection]')

# Create a connection object and retrieve file contents.
# Specify the input format as a "csv" and cache the result for 600 seconds.
conn = st.connection('s3', type=FilesConnection)
df = conn.read("st-aws-connect-bucket/data-science-salaries-1.csv", input_format="csv", ttl=600)

st.header('Our Data 👀')
st.dataframe(df.head(5))
st.write("---")

st.subheader("Company's Origins")
data = df['company location'].value_counts().index[:11]
sns_fig = plt.figure(figsize=(18,10))
sns.countplot(x=df["company location"], order=data)
st.pyplot(sns_fig)

st.subheader("Companies in North America 🌎")
chart = px.choropleth(data_frame = df["company location"].value_counts(),
                    locations=df["company location"].value_counts().index,
                    locationmode="country names", 
                    color=df["company location"].value_counts().values,
                    height= 600,scope="north america",
                    labels={"color":"Company","locations":"Country"})

st.plotly_chart(chart)
