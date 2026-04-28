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

def nav(page):
    st.session_state.page = page

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
.nav-left {
    display: flex;
    gap: 40px;
}
.nav-btn {
    background: #111;
    color: white;
    border: none;
    font-weight: 500;
    cursor: pointer;
}
.nav-btn:hover {
    color: #ffccbc;
}
.nav-right {
    display: flex;
    gap: 20px;
    font-size: 18px;
    color: white;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    border-left: 5px solid #9b2f23;
}
.price {
    font-size: 22px;
    font-weight: bold;
    color: #9b2f23;
}
.section-title {
    font-size: 28px;
    font-weight: bold;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="navbar">', unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,4,1])

with col1:
    if st.button("Home"):
        nav("Home")
with col2:
    if st.button("Shop"):
        nav("Shop")
with col3:
    if st.button("Past Cakes"):
        nav("Past Cakes")
with col4:
    if st.button("Contact Us"):
        nav("Contact")

with col6:
    st.write("🔍 🛒")

st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.page == "Home":

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

    cols = st.columns(3)

    items = [
        ("Cannoli", "Classic ricotta filled pastry", "$2.50"),
        ("Italian Bread", "Fresh baked daily", "$4.00"),
        ("Chocolate Cookies", "Soft and rich chocolate cookies", "$3.00"),
        ("Cakes", "Custom cakes for any occasion", "$25+"),
        ("Sfogliatelle", "Flaky Italian pastry with ricotta filling", "$3.50"),
        ("Rainbow Cookies", "Almond layered cookies with chocolate", "$2.75")
    ]

    for i, item in enumerate(items):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="card">
                <h3>{item[0]}</h3>
                <p>{item[1]}</p>
                <p class="price">{item[2]}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Why Choose Us</div>', unsafe_allow_html=True)

    cols2 = st.columns(3)

    features = [
        ("🍞 Fresh Daily", "Baked fresh every morning"),
        ("🇮🇹 Italian Tradition", "Family recipes passed down"),
        ("🎂 Custom Orders", "Cakes for any event")
    ]

    for i, f in enumerate(features):
        with cols2[i]:
            st.markdown(f"""
            <div class="card">
                <h3>{f[0]}</h3>
                <p>{f[1]}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#111; padding:40px; border-radius:20px; text-align:center; margin-top:40px; color:white;'>
        <h2>Ready to Order?</h2>
        <p>Visit our shop page to browse fresh bakery items.</p>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "Shop":

    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/bakery_items?select=*",
        headers=headers
    )

    if response.status_code == 200:
        items = response.json()
        for item in items:
            st.markdown(f"{item['name']} - ${item['price']}")

elif st.session_state.page == "Past Cakes":

    st.markdown('<div class="section-title">Past Cakes</div>', unsafe_allow_html=True)
    st.write("Cake gallery coming soon")

elif st.session_state.page == "Contact":

    st.markdown('<div class="section-title">Contact Us</div>', unsafe_allow_html=True)
    st.write("Lynbrook, NY")
    st.write("Phone coming soon")
    st.write("Email coming soon")
