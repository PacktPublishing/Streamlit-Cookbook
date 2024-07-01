import streamlit as st

def main():
    st.set_page_config(layout="wide")

    cols = st.columns(3, gap="medium")

    options = ["Option 1", "Option 2", "Option 3"]

    with cols[0]:
        st.title(":rainbow-background[Colors]")
        st.slider("st.slider", value=50)
        st.select_slider("st.select_slider", options, value="Option 2")
        
        small_cols = st.columns(2)
        with small_cols[0]:
            st.toggle("st.toggle", True)
        
        with small_cols[1]:    
            st.checkbox("st.checkbox", True)
        
        st.radio("st.radio", options, horizontal=True)

        small_cols = st.columns(2)
        with small_cols[0]:
            "Primary button"
            st.button("st.button", type="primary", use_container_width=True)
        
        with small_cols[1]:
            "Secondary button"
            st.button("st.button", type="secondary", use_container_width=True)

    with cols[1]:
        st.text_area("st.text_area", height=50)
        st.text_input("st.text_input")
        st.number_input("st.number_input")
        st.selectbox("st.selectbox", options)
        st.date_input("st.date_input")
        st.color_picker("st.color_picker", value="#FB48C4")

    with cols[2]:
        st.multiselect("st.multiselect", options, default=["Option 2"])
        st.file_uploader("st.file_uploader")

    with st.sidebar:
        st.title("🐍")
        st.divider()
        st.write("st.sidebar")



if __name__ == "__main__":
    main()
