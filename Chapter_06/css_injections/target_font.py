import streamlit as st


def main():

    font_family = "Impact"

    css = f"""
        <style>        
        @import url(https://fonts.bunny.net/css?family={font_family});
        h1 {{
            font-family: '{font_family}';
        }}
        </style>
    """

    if st.toggle("Inject CSS"):
        st.html(css)


    with st.echo(code_location="below"):
        st.title("The quick brown fox jumps over the lazy dog.")
        st.write("👻 some other text " * 10)


if __name__ == "__main__":
    main()
