import streamlit as st


def main():
    css = """
        <style>
        [data-testid="stImage"] {
            display: block;
            margin-left: auto;
            margin-right: auto;
        }

        img{
            border: 5px solid #ff4b4b;
            border-radius: 20px;
            transition: 0.1s linear;
            opacity: 0.90;
        }

        img:hover{
            transition: 0.1s linear;
            opacity: 1.0;
        }
        </style>
    """

    if st.toggle("Inject CSS"):
        st.html(css)

    with st.echo(code_location="below"):
        st.image("https://placekitten.com/200/300", caption="A cat 🐈‍⬛")


if __name__ == "__main__":
    main()
