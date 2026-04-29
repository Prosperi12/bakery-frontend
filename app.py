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
    margin-bottom: 25px;
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

c1, c2, c3, c4, c5, c6, c7 = st.columns([1,1,1,1,4,1,1])

with c1:
    if st.button("Home"):
        nav("Home")
with c2:
    if st.button("Shop"):
        nav("Shop")
with c3:
    if st.button("Past Cakes"):
        nav("Past Cakes")
with c4:
    if st.button("Contact Us"):
        nav("Contact")
with c6:
    if st.button("🔍"):
        nav("Search")
with c7:
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

        st.markdown(f"<h2>Total: ${total:.2f}</h2>", unsafe_allow_html=True)

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
        ("Cannoli", "Classic ricotta filled pastry", "images/cannoli.jpg"),
        ("Italian Bread", "Fresh baked daily", "images/bread.jpg"),
        ("Chocolate Cookies", "Soft and rich chocolate cookies", "images/cookies.jpg"),
        ("Cakes", "Custom cakes for any occasion", "images/cake.jpg"),
        ("Sfogliatelle", "Flaky Italian pastry with ricotta filling", "images/sfoglia.jpg"),
        ("Rainbow Cookies", "Almond layered cookies with chocolate", "images/rainbow.jpg"),
        ("Pignoli Cookies", "Almond cookies topped with pine nuts", "images/pignoli.jpg"),
        ("Anisette Cookies", "Soft cookies with light anise flavor", "images/ani.webp"),
        ("Almond Biscotti", "Crunchy almond twice-baked cookies", "images/almond.jpg"),
        ("Linzertarts", "Raspberry filled shortbread tart", "images/linzer.jpg"),
        ("Black and White Cookie", "Classic half chocolate half vanilla", "images/black.webp"),
        ("Apple Turnover", "Flaky pastry filled with apple", "images/turnover.jpg"),
        ("Cheese Danish", "Sweet cheese pastry", "images/danish.jpg"),
        ("Tiramisu", "Coffee layered dessert", "images/tiramisu.webp"),
        ("Cream Puff", "Pastry filled with cream", "images/creampuff.jpg"),
        ("Eclair", "Chocolate topped cream pastry", "images/eclairs.avif")
    ]

    for item in shop_items:
        col1, col2 = st.columns([1,2])

        with col1:
            st.image(item[2], use_container_width=True)

        with col2:
            st.markdown(f"""
            <div class="card">
                <h2>{item[0]}</h2>
                <p>{item[1]}</p>
                <p class="price">${product_prices[item[0]]:.2f}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Add {item[0]}", key=f"shop_{item[0]}"):
                add_to_cart(item[0])
                st.success(f"{item[0]} added to cart!")

elif st.session_state.page == "Past Cakes":
    st.markdown('<div class="section-title">Past Cakes</div>', unsafe_allow_html=True)
    st.write("Cake gallery coming soon")

elif st.session_state.page == "Contact":
    st.markdown('<div class="section-title">Contact Us</div>', unsafe_allow_html=True)
    st.write("Lynbrook, NY")
    st.write("Phone coming soon")
    st.write("Email coming soon")
