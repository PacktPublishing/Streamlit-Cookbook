import streamlit as st
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance


@st.cache_resource
def get_resized_photo(path: Path):
    """Fit to size and return a PIL.Image"""
    size = (500, 400)

    with Image.open(path) as img:
        edited_img = ImageOps.fit(img, size)

    return edited_img


def main():
    ## Define layout
    title_placeholder = st.container()
    go_back, photo_col, go_next = st.columns([1, 5, 1], vertical_alignment="center")
    tools_placeholder = st.expander("**Options**", icon=":material/brush:")

    ## Retrieve a list of photos
    list_of_photos = list(Path("photos").iterdir())
    n_photos = len(list_of_photos)

    ## Define index of photo in session state
    if "photo_index" not in st.session_state:
        st.session_state.photo_index = 0

    ## Insert navigation buttons
    with go_back:
        if st.button("◀", help="Show **previous** photo", use_container_width=True):
            st.session_state.photo_index -= 1

    with go_next:
        if st.button("▶", help="Show **next** photo", use_container_width=True):
            st.session_state.photo_index += 1

    st.session_state.photo_index %= n_photos

    ## Get image based on the current photo index
    img = get_resized_photo(list_of_photos[st.session_state.photo_index])

    ## Define image operations
    with tools_placeholder:
        lcol, rcol = st.columns(2, vertical_alignment="center")

        with lcol:
            if st.toggle("Grayscale?"):
                img = img.convert("L")

            if st.toggle(
                "Posterize?",
                help="What is [Posterization](https://en.wikipedia.org/wiki/Posterization)?",
            ):
                img = ImageOps.posterize(img, bits=3)

        with rcol:
            contrast_factor = st.slider("Contrast", 0.2, 2.0, 1.0, 0.1)
            contrast = ImageEnhance.Contrast(img)
            img = contrast.enhance(contrast_factor)

            brightness_factor = st.slider("Brightness", 0.0, 2.0, 1.0, 0.1)
            brightness = ImageEnhance.Brightness(img)
            img = brightness.enhance(brightness_factor)

    ## Show processed photo
    with photo_col:
        st.image(img, use_column_width=True)

    ## Put a title on the app!
    with title_placeholder:
        st.title("Photo*dog*")


if __name__ == "__main__":
    main()
