import streamlit as st
from itertools import cycle
from store_utils import create_items_db, ShoppingCart


def main():
    st.set_page_config(
        page_title="The Little Store Online", page_icon="🛒", layout="wide"
    )

    if "cart" not in st.session_state:
        st.session_state.cart = ShoppingCart()

    if "items_db" not in st.session_state:
        st.session_state.items_db = {}
        create_items_db()

    ## Page layout
    st.header(":rainbow[The Little Store] ***:gray[Online]***", divider="grey")
    slogan_column, cart_column = st.columns([8, 2], vertical_alignment="bottom")
    items_area = st.container()
    st.divider()
    store_information_area = st.container()

    ## Page title and introduction
    with slogan_column:
        st.write("Welcome to the little store.")

    with store_information_area:
        st.caption("🔪 This is a recipe from the Streamlit Cookbook")

    ## Shopping cart interface
    with cart_column:
        with st.popover(
            "🛒",
            help=":gray[*Shopping cart*]",
            use_container_width=True,
        ):
            st.write("🛒 _Shopping Cart_")
            st.session_state.cart.render_short_summary()

            if st.button(
                "Go to checkout",
                use_container_width=True,
                help=f"Your total is *:green[${st.session_state.cart.total:.2f}]*",
                disabled=not st.session_state.cart,
            ):
                st.session_state.cart.show()

    ## Item description area
    with items_area:
        ## Create columns in the main section
        items_cols = cycle(st.columns(2))

        for col, item in zip(items_cols, st.session_state.items_db.values()):
            with col:
                item.render()


if __name__ == "__main__": 
    main()
