import streamlit as st


def main():
    css = """
        <style>
        h1 {
            text-align: center;
        }

        h2 {
            text-align: end;
        }

        h3 {
            text-align: justify;
        }
        </style>
    """

    if st.toggle("Inject CSS"):
        st.html(css)

    with st.echo(code_location="below"):
        st.title("A centered title")
        st.write("A bunch of repeated text 🐍. " * 6)

    st.divider()

    with st.echo(code_location="below"):
        st.header("An end-aligned header")
        st.write("A bunch of repeated text 🐍. " * 6)

    st.divider()

    with st.echo(code_location="below"):
        st.subheader("A start-aligned subheader")
        st.write("A bunch of repeated text 🐍. " * 6)


if __name__ == "__main__":
    main()
