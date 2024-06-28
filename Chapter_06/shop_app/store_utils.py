from dataclasses import dataclass
from collections import OrderedDict
import streamlit as st
from time import sleep


@dataclass
class Product:
    sku: str
    name: str
    brand: str
    price: float
    description: str
    image: str

    def __post_init__(self):
        # Adds the product to the database dictionary
        st.session_state.product_db[self.sku] = self

    def __hash__(self) -> int:
        return hash(self.sku)

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

    def render_remove_from_cart_button(self):
        st.button(
            "**−**",
            key=f"btn_del_{self.sku}",
            use_container_width=True,
            on_click=self.remove_from_cart_callback,
            disabled=not st.session_state.cart.get(self.sku, False),
            help="*Remove from cart*",
        )

    def add_to_cart_callback(self):
        if self.sku in st.session_state.cart:
            st.session_state.cart[self.sku] += 1

        else:
            st.session_state.cart[self.sku] = 1

        st.toast(
            f"{self.name} was added to the cart.", icon=":material/add_shopping_cart:"
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


class ShoppingCart(OrderedDict):

    def render_short_summary(self):
        names = self.summary["name"]
        prices = self.summary["price"]
        qtys = self.summary["qty"]
        
        for name, price, qty in zip(names, prices, qtys):
            # st.markdown(f"**{name}**: \${price:.2f} × {qty:.0f} = \${price * qty:.2f}")
            st.markdown(f":gray[- {name} (× {qty:.0f})]")



    @property
    def summary(self):
        db = st.session_state.product_db
        skus = list(self.keys())
        qtys = list(self.values())

        return {
            "sku": skus,
            "name": [db[sku].name for sku in skus],
            "image": [db[sku].image for sku in skus],
            "price": [db[sku].price for sku in skus],
            "qty": qtys,
        }

    @property
    def total(self):
        qtys = self.values()
        prices = [st.session_state.product_db[sku].price for sku in self.keys()]

        return sum([q * p for q, p in zip(qtys, prices)])


def run_payment():
    """Emulates some payment process that takes a few seconds"""

    with st.status("💵 Initiating payment...", expanded=False) as status:
        sleep(1)
        status.update(label="💰 Grabbing your wallet...")
        sleep(2)
        status.update(label="💸 Paying...")
        sleep(1)
        status.update(label="✅ Payment complete!", state="complete", expanded=False)
        sleep(1)

        del st.session_state.cart
