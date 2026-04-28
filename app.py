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

if "selected_product" not in st.session_state:
    st.session_state.selected_product = None

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

def nav(page):
    st.session_state.page = page
    st.session_state.selected_product = None

def add_to_cart(product):
    if product in st.session_state.cart:
        st.session_state.cart[product] += 1
    else:
        st.session_state.cart[product] = 1

cart_count = sum(st.session_state.cart.values())

st.markdown("""
<style>
.stApp { background: #fff8ef; }

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #111;
    padding: 15px 40px;
    border-radius: 12px;
    margin-bottom: 25px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    border-left: 6px solid #9b2f23;
    margin-bottom: 25px;
    color: black;
}

.card h3, .card h2 {
    color: black;
}

.card p {
    color: #333;
}

.price {
    font-size: 20px;
    font-weight: bold;
    color: #9b2f23;
}

.section-title {
    font-size: 28px;
    font-weight: bold;
    margin-top: 40px;
    margin-bottom: 10px;
    color: black;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="navbar">', unsafe_allow_html=True)

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

st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.page == "Search":
    st.markdown('<div class="section-title">Search</div>', unsafe_allow_html=True)
    query = st.text_input("Search items", value=st.session_state.search_query)
    st.session_state.search_query = query

    items = ["Cannoli", "Italian Bread", "Chocolate Cookies", "Cakes", "Sfogliatelle", "Rainbow Cookies"]

    results = [i for i in items if query.lower() in i.lower()]

    for r in results:
        st.markdown(f"<div class='card'><h3>{r}</h3></div>", unsafe_allow_html=True)

elif st.session_state.page == "Cart":
    st.markdown('<div class="section-title">Your Cart</div>', unsafe_allow_html=True)

    if not st.session_state.cart:
        st.write("Cart is empty")
    else:
        for item, qty in st.session_state.cart.items():
            st.markdown(f"<div class='card'><h3>{item}</h3><p>Quantity: {qty}</p></div>", unsafe_allow_html=True)

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
        <h1 style="font-size: 56px;">Luigi's Italian Bakery</h1>
        <p style="font-size: 22px; font-style: italic;">Don’t be shy, eat some sweets 🍰</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Featured Favorites</div>', unsafe_allow_html=True)

    items = [
        ("Cannoli", "Classic ricotta filled pastry", "$2.50"),
        ("Italian Bread", "Fresh baked daily", "$4.00"),
        ("Chocolate Cookies", "Soft and rich chocolate cookies", "$3.00"),
        ("Cakes", "Custom cakes for any occasion", "$25+"),
        ("Sfogliatelle", "Flaky Italian pastry with ricotta filling", "$3.50"),
        ("Rainbow Cookies", "Almond layered cookies with chocolate", "$2.75")
    ]

    for i in range(0, len(items), 3):
        cols = st.columns(3, gap="large")
        for j in range(3):
            if i + j < len(items):
                item = items[i + j]
                with cols[j]:
                    st.markdown(f"""
                    <div class="card">
                        <h3>{item[0]}</h3>
                        <p>{item[1]}</p>
                        <p class="price">{item[2]}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button(f"Add {item[0]}", key=item[0]):
                        add_to_cart(item[0])
                        st.success(f"{item[0]} added")

elif st.session_state.page == "Shop":
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/bakery_items?select=*",
        headers=headers
    )

    if response.status_code == 200:
        items = response.json()
        for item in items:
            st.write(f"{item['name']} - ${item['price']}")

elif st.session_state.page == "Past Cakes":
    st.markdown('<div class="section-title">Past Cakes</div>', unsafe_allow_html=True)
    st.write("Cake gallery coming soon")

elif st.session_state.page == "Contact":
    st.markdown('<div class="section-title">Contact Us</div>', unsafe_allow_html=True)
    st.write("Lynbrook, NY")
    st.write("Phone coming soon")
    st.write("Email coming soon")
