import streamlit as st
# Made by Edwin Saavedra C.


def main():
    ## Initialize the session state
    if "wizard_step" not in st.session_state:
        st.session_state.wizard_step = 0

    ## Define the layout of the wizard
    st.header("🧙‍♂️ Wizard skeleton", anchor=False)
    st.caption(f"`{st.session_state.wizard_step =: }`")
    prev_col, restart_col, next_col = st.columns(3)
    content_placeholder = st.empty()

    with prev_col:
        st.button(
            "⬅️ Previous",
            on_click=prev_step,
            disabled=st.session_state.wizard_step <= 0,
            use_container_width=True,
        )

    with restart_col:
        st.button(
            "↻ Restart",
            on_click=restart_step,
            disabled=st.session_state.wizard_step == 0,
            use_container_width=True,
        )

    with next_col:
        st.button(
            "Next ➡️",
            on_click=next_step,
            disabled=st.session_state.wizard_step >= 3,
            use_container_width=True,
        )

    ## Define the content of the wizard
    with content_placeholder.container(border=True):
        if st.session_state.wizard_step == 0:
            st.write("This is the **first step**.")
            st.session_state.number = st.number_input(
                "Enter a number",
                value=st.session_state.get("number", 0),
            )

        elif st.session_state.wizard_step == 1:
            "This is the **second step**."
            f"In the first step, you set `{st.session_state.number =: .2f}`"
            st.session_state.text = st.text_input(
                "Write some text",
                value=st.session_state.get("text", ""),
            )

        elif st.session_state.wizard_step == 2:
            "This is the **third step**."
            f"In the second step, you set `{st.session_state.text =:s}`"
            st.session_state.color = st.color_picker(
                "Pick a color",
                st.session_state.get("color", "#990000"),
            )

        elif st.session_state.wizard_step == 3:
            "This is the **final step** of the wizard."
            "Here is the `session_state` after all previous steps:"
            st.json(st.session_state)


def next_step():
    st.session_state.wizard_step += 1


def prev_step():
    st.session_state.wizard_step -= 1


def restart_step():
    del st.session_state.wizard_step


if __name__ == "__main__":
    main()
