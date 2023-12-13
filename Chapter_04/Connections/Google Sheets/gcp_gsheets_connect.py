import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_gsheets import GSheetsConnection

st.title(":blue[Streamlit + Private Google Sheets🔌]")

conn = st.experimental_connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="data-science-salaries-1")

st.subheader('Glimpse of the Data 👀')
st.dataframe(df.head(5))

st.subheader("Popular Roles in Data Science 💼")
data = df['job title'].value_counts().index[:11]

sns_fig = plt.figure(figsize=(25,15))
sns.countplot(x=df["job title"], order=data)
st.pyplot(sns_fig)

#------------------------------------------------
#----------------------There's more--------------

# Before implementing this step, make sure to create an empty private GSheet with
# "Editor" access and replace this new URL within the `secrets.toml` file.

st.subheader("1. Load DataFrame into Google Sheets")

df = pd.DataFrame(
    {
        "Passenger ID": [1, 2, 3, 4, 5],
        "Name": ['Mei Chen', 'Pierre Dupont', 'Diego Rodriguez', 'Anna Martin', 'Nitin Mehta'],
        "Gender": ['F', 'M', 'M', 'F', 'M'],
        "Age": [24, 40, 28, 22, 35],
        "Destination": ['Tokyo', 'Paris', 'Sydney', 'Rome', 'Vancouver'],
        "Days(duration)": [5, 7, 14, 6, 7],
    }
)
st.dataframe(df)

# Click the button to update worksheet. This is behind a button to avoid exceeding Google API Quota
if st.button("➕ Create new worksheet"):
    df = conn.create(
        worksheet="sheets_conn_demo-1",
        data=df,
    )
    st.cache_data.clear()
    st.experimental_rerun()

st.write("---")


st.subheader("2. Read Google Worksheet as DataFrame")
st.info(
    "If the sheet has been deleted, press 'Create new worksheet' button above.",
    icon="ℹ️",
)
# Read Google WorkSheet as DataFrame
df = conn.read(
    worksheet="sheets_conn_demo-1",
)

# Display our Spreadsheet as st.dataframe
st.dataframe(df)
st.write("---")


st.subheader("3. Update Google Worksheet using DataFrame")

df = pd.DataFrame(
    {
        "Passenger ID": [1, 2, 3, 4, 5, 6],
        "Name": ['Mei Chen', 'Pierre Dupont', 'Diego Rodriguez', 'Anna Martin', 'Nitin Mehta', 'Selina Garcia'],
        "Gender": ['F', 'M', 'M', 'F', 'M', 'F'],
        "Age": [24, 40, 28, 22, 35, 30],
        "Destination": ['Tokyo', 'Paris', 'Sydney', 'Rome', 'Vancouver', 'Barcelona'],
        "Days(duration)": [5, 7, 14, 6, 7, 9],
        "Travel date": ['10 Sept 2023', '15 May 2023', '3 Jun 2023', '25 Jul 2023', '18 Aug 2023', '5 Oct 2023'],
        "Purpose": ['Business', 'Leisure', 'Vacation', 'Friends reunion', 'Cultural event', 'Vacation'],
    }
)
# Click the button to update the worksheet.
if st.button("⚡ Update worksheet"):
    df = conn.update(
        worksheet="sheets_conn_demo-1",
        data=df,
    )
    st.cache_data.clear()
    st.experimental_rerun()

# Display our updated Spreadsheet as st.dataframe
st.dataframe(df)
st.write("---")


st.subheader("4. Query Google WorkSheet with SQL and get results as DataFrame")
st.info(
    "Mutation SQL queries are in-memory only and do not results in the Worksheet update.",
    icon="ℹ️",
)
# Make sure worksheet name is in double quota "", DuckDB SQL dialect is supported
sql = 'select name, age, destination from "sheets_conn_demo-1" order by gender'

df = conn.query(sql=sql, ttl=3600)

 # Display our SQL query results as st.dataframe
st.dataframe(df)
st.write("---")


st.subheader("5. Clear Worksheet")

# Click button to delete worksheet.
if st.button("🧹 Clear worksheet"):
    conn.clear(worksheet="sheets_conn_demo-1")
    st.success("Worksheet sheets_conn_demo-1 is now cleared! 👍")
    st.cache_data.clear()
    st.experimental_rerun()

st.dataframe(df)
st.write("---")


st.subheader("6. Delete Worksheet")
# Click button to delete worksheet using the underlying gspread API.
if st.button("💀 Delete worksheet"):
    spreadsheet = conn.client._open_spreadsheet()  # type: ignore
    worksheet = spreadsheet.worksheet("sheets_conn_demo-1")
    spreadsheet.del_worksheet(worksheet)
    st.cache_data.clear()
    st.experimental_rerun()

st.dataframe(df)
