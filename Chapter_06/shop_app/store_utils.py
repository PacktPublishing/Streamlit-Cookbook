import streamlit as st
from dataclasses import dataclass
from collections import UserDict
from time import sleep
import json


@dataclass
class Item:
    sku: str
    name: str
    price: float
    description: str
    image: str

    def __post_init__(self):
        # Adds the product to the database dictionary
        st.session_state.items_db[self.sku] = self

    def render(self):
        with st.container(border=True):
            left_col, right_col = st.columns([1, 2], vertical_alignment="center")

            with left_col:
                st.image(self.image, use_column_width=True)

            with right_col:
                st.markdown(f":blue-background[:violet[**{self.name}**]]")
                st.caption(self.description)
                st.metric("Price", f"$ {self.price:.2f}", label_visibility="collapsed")

            if st.session_state.cart.get(self.sku, False):
                button_cols = st.columns([1, 5])

                with button_cols[1]:
                    self.render_add_to_cart_button()

                with button_cols[0]:
                    self.render_remove_from_cart_button()

            else:
                self.render_add_to_cart_button()

    def render_add_to_cart_button(self):
        st.button(
            "**➕ Add to cart**",
            key=f"btn_add_{self.sku}",
            use_container_width=True,
            type="primary",
            on_click=self.add_to_cart_callback,
            help="*Add to cart*",
        )

    def add_to_cart_callback(self):
        if self.sku in st.session_state.cart:
            st.session_state.cart[self.sku] += 1

        else:
            st.session_state.cart[self.sku] = 1

        st.toast(
            f"{self.name} was added to the cart.", icon=":material/add_shopping_cart:"
        )

    def render_remove_from_cart_button(self):
        st.button(
            "**−**",
            key=f"btn_del_{self.sku}",
            use_container_width=True,
            on_click=self.remove_from_cart_callback,
            disabled=not st.session_state.cart.get(self.sku, False),
            help="*Remove from cart*",
        )

    def remove_from_cart_callback(self):
        if self.sku in st.session_state.cart:
            st.session_state.cart[self.sku] -= 1

            if st.session_state.cart[self.sku] <= 0:
                del st.session_state.cart[self.sku]

            st.toast(
                f"{self.name} was removed from the cart.",
                icon=":material/remove_shopping_cart:",
            )


class ShoppingCart(UserDict):
    @property
    def summary(self):
        db = st.session_state.items_db
        skus = self.keys()

        return {
            "sku": skus,
            "name": [db[sku].name for sku in skus],
            "image": [db[sku].image for sku in skus],
            "price": [db[sku].price for sku in skus],
            "qty": list(self.values()),
        }

    @property
    def total(self):
        db = st.session_state.items_db
        qtys = self.values()
        prices = (db[sku].price for sku in self.keys())

        return sum([q * p for q, p in zip(qtys, prices)])

    def render_short_summary(self):
        names = self.summary["name"]
        qtys = self.summary["qty"]

        for name, qty in zip(names, qtys):
            st.markdown(f":gray[- {name} (× {qty:.0f})]")

    @st.experimental_dialog("🛒 Shopping cart", width="large")
    def show(self):
        """Dialog to show the shopping cart and options to pay"""

        st.dataframe(
            self.summary,
            use_container_width=True,
            hide_index=True,
            column_config={
                "sku": None,
                "name": "Name",
                "price": st.column_config.NumberColumn(
                    label="Price $", format=r"$%.2f"
                ),
                "image": st.column_config.ImageColumn(label="Image"),
                "qty": st.column_config.NumberColumn(label="Quantity", format=r"%.0f"),
            },
        )

        empty_cart_column, pay_column = st.columns([1,3])

        with empty_cart_column:
            if st.button(
                "Empty cart",
                disabled=not self,
                use_container_width=True,
            ):
                del st.session_state.cart
                st.rerun()

        with pay_column:

            pay_button = st.button(
                f"Pay total: ${self.total:.2f}",
                disabled=not self,
                type="primary",
                use_container_width=True,
            )

        if pay_button:
            self.run_payment()
            del st.session_state.cart
            st.rerun()

    def run_payment(self):
        with st.status("💵 Initiating payment...", expanded=False) as status:
            sleep(1)
            status.update(label="💰 Grabbing your wallet...")

            sleep(2)
            status.update(label="💸 Paying...")

            sleep(1)
            status.update(label="✅ Payment complete!", state="complete")
            sleep(1)


def create_items_db():
    with open("items.json", "r") as f:
        all_items = json.load(f)
        for item in all_items:
            Item(**item)
