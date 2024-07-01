import streamlit as st

st.set_page_config(layout="wide")


@st.experimental_dialog("Dialog")
def show_dialog():
    st.image(
        "https://placehold.co/300x200?text=I'm+in+the+dialog+box",
        caption="An image in a dialog box",
        use_column_width=True,
    )


with st.sidebar:
    st.header("Sidebar")
    st.image(
        "https://placehold.co/200x250?text=I'm+in+the+sidebar",
        caption="An image in the sidebar",
        use_column_width=True,
    )

st.logo("https://placehold.co/240x100?text=Logo")

st.title("Main body")
st.image(
    "https://placehold.co/500x180?text=I'm+in+the+main+body",
    caption="An image in the main body",
    use_column_width=True,
)

st.divider()

with st.popover("Popover"):
    st.image(
        "https://placehold.co/200x100?text=I'm+in+a+popover",
        caption="An image inside a popover",
        use_column_width=True,
    )

# with st._bottom:
#     st.image(
#         "https://placehold.co/600x50?text=I'm+in+the+_bottom",
#         use_column_width=True,
#     )


st.toast(
    """
    ![An image in a toast](https://placehold.co/200x100?text=I'm+in+a+toast)
    """,
    icon="🦜",
)
