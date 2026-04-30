import streamlit as st
import requests

SUPABASE_URL = "https://mpgpvcutkibcdhsrbzxh.supabase.co"
SUPABASE_KEY = "sb_publishable_hJXHy_q1nuntSvyQa8lAiQ_zux_SwWi"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

st.set_page_config(page_title="Luigi's Italian Bakery", page_icon="🇮🇹", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

def nav(page):
    st.session_state.page = page

def add_to_cart(product):
    if product in st.session_state.cart:
        st.session_state.cart[product] += 1
    else:
        st.session_state.cart[product] = 1

def remove_one(product):
    if product in st.session_state.cart:
        st.session_state.cart[product] -= 1
        if st.session_state.cart[product] <= 0:
            del st.session_state.cart[product]

product_prices = {
    "Cannoli": 2.50,
    "Italian Bread": 4.00,
    "Chocolate Cookies": 3.00,
    "Cakes": 25.00,
    "Sfogliatelle": 3.50,
    "Rainbow Cookies": 2.75,
    "Pignoli Cookies": 4.50,
    "Anisette Cookies": 3.50,
    "Almond Biscotti": 3.00,
    "Linzertarts": 3.75,
    "Black and White Cookie": 3.25,
    "Apple Turnover": 3.75,
    "Cheese Danish": 3.50,
    "Tiramisu": 6.00,
    "Cream Puff": 3.50,
    "Eclair": 3.75
}

cart_count = sum(st.session_state.cart.values())

st.markdown("""
<style>
.stApp { background: #fff8ef; }
.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    border-left: 6px solid #9b2f23;
    margin-bottom: 15px;
    color: black;
}
.card h2, .card h3, .card p {
    color: black;
}
.price {
    font-size: 20px;
    font-weight: bold;
    color: #9b2f23 !important;
}
.section-title {
    font-size: 28px;
    font-weight: bold;
    margin-top: 40px;
    margin-bottom: 10px;
    color: black;
}
.footer-box h3,
.footer-box p {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

c1, c2, c3, c4, c5, c6 = st.columns([1,1,1,4,1,1])

with c1:
    if st.button("Home"):
        nav("Home")
with c2:
    if st.button("Shop"):
        nav("Shop")
with c3:
    if st.button("Contact Us"):
        nav("Contact")
with c5:
    if st.button("🔍"):
        nav("Search")
with c6:
    if st.button(f"🛒 {cart_count}"):
        nav("Cart")

if st.session_state.page == "Search":
    st.markdown('<div class="section-title">Search</div>', unsafe_allow_html=True)
    query = st.text_input("Search items", value=st.session_state.search_query)
    st.session_state.search_query = query

    items = list(product_prices.keys())
    results = [i for i in items if query.lower() in i.lower()]

    for r in results:
        st.markdown(f"<div class='card'><h3>{r}</h3><p class='price'>${product_prices[r]:.2f}</p></div>", unsafe_allow_html=True)
        if st.button(f"Add {r}", key=f"search_add_{r}"):
            add_to_cart(r)
            st.success(f"{r} added to cart!")

elif st.session_state.page == "Cart":
    st.markdown('<div class="section-title">Your Cart</div>', unsafe_allow_html=True)

    if not st.session_state.cart:
        st.write("Cart is empty")
    else:
        total = 0

        for item, qty in list(st.session_state.cart.items()):
            price = product_prices[item]
            subtotal = price * qty
            total += subtotal

            st.markdown(f"""
            <div class="card">
                <h2>{item}</h2>
                <p class="price">${price:.2f}</p>
                <p>Quantity: {qty}</p>
                <p><b>Subtotal:</b> ${subtotal:.2f}</p>
            </div>
            """, unsafe_allow_html=True)

            minus_col, qty_col, plus_col = st.columns([1,1,1])

            with minus_col:
                if st.button("−", key=f"minus_{item}"):
                    remove_one(item)
                    st.rerun()

            with qty_col:
                st.markdown(f"<h3 style='text-align:center;'>{qty}</h3>", unsafe_allow_html=True)

            with plus_col:
                if st.button("+", key=f"plus_{item}"):
                    add_to_cart(item)
                    st.rerun()

        st.markdown(f"""
        <div class="card">
            <h2>Order Total</h2>
            <p class="price">${total:.2f}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Checkout - ${total:.2f}"):
            st.success(f"Checkout started. Final total: ${total:.2f}")

elif st.session_state.page == "Home":
    st.markdown("""
    <div style='
        background-image: linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.45)), url("https://images.unsplash.com/photo-1653946402577-f2477b1002b7?auto=format&fit=crop&w=1600&q=80");
        background-size: cover;
        background-position: center;
        padding: 120px 20px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 40px;
    '>
        <h1 style="font-size: 56px; color:white;">Luigi's Italian Bakery</h1>
        <p style="font-size: 22px; font-style: italic; color:white;">Don’t be shy, eat some sweets 🍰</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Featured Favorites</div>', unsafe_allow_html=True)

    home_items = [
        ("Cannoli", "Classic ricotta filled pastry", "$2.50"),
        ("Italian Bread", "Fresh baked daily", "$4.00"),
        ("Chocolate Cookies", "Soft and rich chocolate cookies", "$3.00"),
        ("Cakes", "Custom cakes for any occasion", "$25+"),
        ("Sfogliatelle", "Flaky Italian pastry with ricotta filling", "$3.50"),
        ("Rainbow Cookies", "Almond layered cookies with chocolate", "$2.75")
    ]

    for i in range(0, len(home_items), 3):
        cols = st.columns(3, gap="large")
        for j in range(3):
            if i + j < len(home_items):
                item = home_items[i + j]
                with cols[j]:
                    st.markdown(f"""
                    <div class="card">
                        <h3>{item[0]}</h3>
                        <p>{item[1]}</p>
                        <p class="price">{item[2]}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button(f"Add {item[0]}", key=f"home_{item[0]}"):
                        add_to_cart(item[0])
                        st.success(f"{item[0]} added to cart!")

    st.markdown("""
    <div class="footer-box" style='
        background:#6b4b3e;
        padding:50px 40px;
        border-radius:20px;
        margin-top:50px;
        text-align:center;
    '>
        <h3 style='margin-bottom:15px;'>Working Hours</h3>
        <p style='margin:5px 0;'>Monday - Saturday: 6:00am - 7:00pm</p>
        <p style='margin:5px 0;'>Sunday: 6:00am - 6:00pm</p>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "Shop":
    st.markdown('<div class="section-title">Shop</div>', unsafe_allow_html=True)

    shop_items = [
        ("Cannoli", "Classic ricotta filled pastry"),
        ("Italian Bread", "Fresh baked daily"),
        ("Chocolate Cookies", "Soft and rich chocolate cookies"),
        ("Cakes", "Custom cakes for any occasion"),
        ("Sfogliatelle", "Flaky Italian pastry with ricotta filling"),
        ("Rainbow Cookies", "Almond layered cookies with chocolate"),
        ("Pignoli Cookies", "Almond cookies topped with pine nuts"),
        ("Anisette Cookies", "Soft cookies with light anise flavor"),
        ("Almond Biscotti", "Crunchy almond twice-baked cookies"),
        ("Linzertarts", "Raspberry filled shortbread tart"),
        ("Black and White Cookie", "Classic half chocolate half vanilla"),
        ("Apple Turnover", "Flaky pastry filled with apple"),
        ("Cheese Danish", "Sweet cheese pastry"),
        ("Tiramisu", "Coffee layered dessert"),
        ("Cream Puff", "Pastry filled with cream"),
        ("Eclair", "Chocolate topped cream pastry")
    ]

    for item in shop_items:
        name = item[0]
        description = item[1]
        qty = st.session_state.cart.get(name, 0)

        st.markdown(f"""
        <div class="card">
            <h2>{name}</h2>
            <p>{description}</p>
            <p class="price">${product_prices[name]:.2f}</p>
            <p><b>Quantity selected:</b> {qty}</p>
        </div>
        """, unsafe_allow_html=True)

        minus_col, qty_col, plus_col = st.columns([1,1,1])

        with minus_col:
            if st.button("−", key=f"shop_minus_{name}"):
                remove_one(name)
                st.rerun()

        with qty_col:
            st.markdown(f"<h3 style='text-align:center;'>{qty}</h3>", unsafe_allow_html=True)

        with plus_col:
            if st.button("+", key=f"shop_plus_{name}"):
                add_to_cart(name)
                st.rerun()

    shop_total = 0
    for cart_item, cart_qty in st.session_state.cart.items():
        shop_total += product_prices[cart_item] * cart_qty

    st.markdown(f"""
    <div class="card">
        <h2>Checkout Total</h2>
        <p class="price">${shop_total:.2f}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(f"Checkout - ${shop_total:.2f}", key="shop_checkout"):
        st.success(f"Checkout started. Final total: ${shop_total:.2f}")


elif st.session_state.page == "Contact":
    st.markdown('<div class="section-title">Contact Us</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown("""
        <div class="card">
            <h3>Leave Us a Message</h3>
            <input placeholder="First Name" style="width:48%; padding:10px; margin:5px;" />
            <input placeholder="Last Name" style="width:48%; padding:10px; margin:5px;" /><br>
            <input placeholder="Phone" style="width:48%; padding:10px; margin:5px;" />
            <input placeholder="Email" style="width:48%; padding:10px; margin:5px;" /><br>
            <input placeholder="Subject" style="width:98%; padding:10px; margin:5px;" />
            <textarea placeholder="Message" style="width:98%; padding:10px; margin:5px; height:120px;"></textarea><br>
            <button style="background:#f4a300; color:white; padding:12px 25px; border:none; border-radius:6px; font-weight:bold;">SEND MESSAGE</button>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
    <div class="card">
    <h3>... OR CONTACT US DIRECTLY</h3>
    <p>If you have any questions, feel free to reach out.</p>
    <p>We’ll get back to you as soon as possible.</p>

    <p>Luigi’s Bakery is dedicated to making your experience smooth and simple. Whether you're ordering desserts or planning something special, we're here to help.</p>

    <p><b>📞 Phone:</b> 493-489-2933</p>
    <p><b>📍 Address:</b> 26 Watkins Avenue, Oneonta, NY, 13820</p>
    <p><b>📧 Email:</b> contactluigi@yahoo.com</p>
    </div>
    """, unsafe_allow_html=True)
