import streamlit as st
from itertools import cycle
from store_utils import Product, ShoppingCart, run_payment
import json

if "cart" not in st.session_state:
    st.session_state.cart = ShoppingCart()


if "product_db" not in st.session_state:
    st.session_state.product_db = {}


def main():
    st.set_page_config(
        page_title="The Little Store Online", page_icon="🛒", layout="wide"
    )

    ## Page layout
    st.header(":rainbow[The Little Store] ***:gray[Online]***", divider="grey")
    slogan_column, cart_column = st.columns([8, 2], vertical_alignment="bottom")
    items_area = st.container()

    ## Page title and introduction
    with slogan_column:
        st.write("Welcome to the little store.")

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
                help=f"Your total is *:green[${st.session_state.cart.total}]*",
                disabled=not st.session_state.cart
            ):
                show_shopping_cart_in_dialog()

    ## Read products and assemble a database
    with open("products.json", "r") as f:
        products = json.load(f)
        for product in products:
            Product(**product)

    ## Item description area
    with items_area:

        ## Create columns in the main section
        products_cols = cycle(st.columns(2))
        
        for col, product in zip(products_cols, st.session_state.product_db.values()):
            with col:
                product.render()


@st.experimental_dialog("🛒 Shopping cart", width="large")
def show_shopping_cart_in_dialog():
    """Dialog to show the shopping cart and options to pay"""

    st.dataframe(
        st.session_state.cart.summary,
        use_container_width=True,
        hide_index=True,
        column_config={
            "sku": None,
            "name": "Name",
            "price": st.column_config.NumberColumn(label="Price $", format=r"$%.2f"),
            "image": st.column_config.ImageColumn(label="Image", width=20),
            "qty": st.column_config.NumberColumn(label="Quantity", format=r"%.0f"),
        },
    )

    empty_cart_column, pay_column = st.columns(2)

    with empty_cart_column:
        if st.button(
            "Empty cart",
            disabled=not st.session_state.cart,
            use_container_width=True,
        ):
            del st.session_state.cart
            st.rerun()

    with pay_column:
        total = st.session_state.cart.total

        pay_button = st.button(
            f"Pay total: ${total:.2f}",
            disabled=not st.session_state.cart,
            type="primary",
            use_container_width=True,
        )

    if pay_button:
        run_payment()
        st.rerun()


if __name__ == "__main__":
    main()
