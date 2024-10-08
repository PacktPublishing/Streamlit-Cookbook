import streamlit as st
from translate import Translator
from typing import Optional
from functools import partial
from textwrap import wrap

LANGUAGES = {
    "en-US": "🇺🇸 English (US)",
    "es-CO": "🇨🇴 Español (CO)",
    "fr-FR": "🇫🇷 Français (FR)",
    "ja": "🇯🇵 日本語",
}

TRANSLATORS = {lang: Translator(to_lang=lang) for lang in LANGUAGES.keys()}


@st.cache_resource
def translate(message: str, lang: Optional[str] = None) -> str:
    if lang is None or lang == "en-US":
        return message

    translator = TRANSLATORS[lang]
    t_msg = ""
    for batch in wrap(
        message,
        width=500,
        replace_whitespace=False,
        break_long_words=False,
        fix_sentence_endings=True,
    ):
        t_msg += translator.translate("".join(batch))

    return t_msg


def main():
    # Layout of app
    title_col, config_col = st.columns([4, 1], vertical_alignment="bottom")
    left_col, right_col = st.columns(2)

    with config_col:
        # Check if a language was specified in the URL
        lang_idx = 0

        if lang := st.query_params.get("lang", False) or st.context.headers.get(
            "Accept-Language", False
        ):
            try:
                lang = lang[:2]
                available_languages = [k[:2] for k in LANGUAGES.keys()]
                lang_idx = available_languages.index(lang)

            except ValueError:
                st.toast(
                    f"The language `{lang}` is not supported. Defaulting to English.",
                    icon="🏴‍☠",
                )

        with st.popover("🦜", use_container_width=True):
            st.radio(
                "Select a language",
                LANGUAGES,
                index=lang_idx,
                key="lang",
                format_func=LANGUAGES.get,
                label_visibility="collapsed",
            )
            _ = partial(
                translate,
                lang=st.session_state.get("lang", None),
            )
            st.query_params["lang"] = st.session_state.lang[:2]

    # The actual contents of the app
    with title_col:
        st.title(_("🐝 About bees"), anchor=False)

    with left_col:
        bee_image_link = "https://upload.wikimedia.org/wikipedia/commons/d/d6/Amegilla_on_long_tube_of_Acanthus_ilicifolius_flower.jpg"

        st.image(bee_image_link, use_column_width=True)

        st.caption(
            _(
                "Long-tongued bees and long-tubed flowers "
                " coevolved, like this *Amegilla* species "
                "(Apidae) on  *Acanthus ilicifolius.* \n"
                f"Source: [wikimedia.org]({bee_image_link})"
            )
        )

    with right_col.container(height=400):
        st.markdown(
            _(
                """
                **Bees** are winged insects closely related to wasps 
                and ants, known for their roles in pollination and, in the 
                case of the best-known bee species, the western honey bee, 
                for producing honey. There are over 20,000 known species 
                of bees in seven recognized biological families. Some 
                species – including honey bees, bumblebees, and 
                stingless bees – live socially in colonies while most species 
                (>90%) – including mason bees, carpenter bees, leafcutter bees, 
                and sweat bees – are solitary.
                """
            )
        )

        st.markdown(
            _(
                """
                Bees are found on every continent except Antarctica, in 
                every habitat on the planet that contains insect-pollinated 
                flowering plants. The **most common** bees in the Northern 
                Hemisphere are the Halictidae, or sweat bees, but they are 
                small and often mistaken for wasps or flies. 
                Bees range in size from tiny stingless bee species, whose 
                workers are less than 2 millimetres (0.08 in) long, to the 
                leafcutter bee *Megachile pluto*, the largest species of 
                bee, whose females can attain a length of 39 millimetres 
                (1.54 in).
                """
            )
        )

        st.caption(
            _(
                """ Extracted from 
                [Wikipedia](https://en.wikipedia.org/wiki/Bee). 
                """
            )
        )


if __name__ == "__main__":
    main()
