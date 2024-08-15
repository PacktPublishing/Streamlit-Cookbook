import streamlit as st
from PIL import Image, ImageEnhance
from io import BytesIO


def main():
    ## Intial configuration
    st.set_page_config(
        layout="centered",
        page_icon="🖼️",
        page_title="My Photo Editor",
    )

    ## Define layout
    title_placeholder = st.container()
    uploader_placeholder = st.empty()
    photo_column, options_column = st.columns((2, 1))

    with options_column:
        tools_placeholder = st.expander("**Options**", icon=":material/brush:")
        download_col, restart_col = st.columns(2, vertical_alignment="center")

    ## Put a title on the app
    with title_placeholder:
        st.title("🖼️ Photo *editor*", anchor=False)

    ## Retrieve image as an uploaded file
    with uploader_placeholder:
        st.file_uploader(
            "Upload an image",
            type=["jpg", "jpeg"],
            accept_multiple_files=False,
            key="uploaded_file",
        )

    ## Show editing options if an image was uploaded
    if st.session_state.uploaded_file:
        ## Clear the uploader placeholder
        uploader_placeholder.empty()

        ## Load image from uploaded file
        img = Image.open(st.session_state.uploaded_file)

        with tools_placeholder:
            ## Define image operations
            slider_kwargs = dict(
                min_value=0.0,
                max_value=2.0,
                value=1.0,
                step=0.01,
            )

            contrast_factor = st.slider("Contrast", **slider_kwargs)
            contrast = ImageEnhance.Contrast(img)
            img = contrast.enhance(contrast_factor)

            brightness_factor = st.slider("Brightness", **slider_kwargs)
            brightness = ImageEnhance.Brightness(img)
            img = brightness.enhance(brightness_factor)

            sharpness_factor = st.slider("Sharpness", **slider_kwargs)
            sharpness = ImageEnhance.Sharpness(img)
            img = sharpness.enhance(sharpness_factor)

            color_factor = st.slider("Color", **slider_kwargs)
            color = ImageEnhance.Color(img)
            img = color.enhance(color_factor)

            ## Save the edited image
            with BytesIO() as buffer:
                img.save(buffer, format="JPEG")

                download_col.download_button(
                    "💾 Save",
                    file_name="edited_photo.jpg",
                    data=buffer.getvalue(),
                    use_container_width=True,
                )

            ## Start all over button
            if restart_col.button("🗑️ Clear", use_container_width=True):
                show_confirmation_dialog()

        ## Show processed photo
        with photo_column:
            st.image(img)


@st.dialog("Are you sure?")
def show_confirmation_dialog():
    yes_col, no_col = st.columns((1.5, 1))

    with yes_col:
        if st.button(
            "👍 Yes, start over", on_click=clear_uploader, use_container_width=True
        ):
            st.rerun()

    with no_col:
        if st.button("👎 No, go back", use_container_width=True):
            st.rerun()


def clear_uploader():
    del st.session_state.uploaded_file


if __name__ == "__main__":
    main()
