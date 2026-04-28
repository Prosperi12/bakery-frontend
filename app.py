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
.stApp {
    background: #fff8ef;
}
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
    background: #222;
    color: white;
    padding: 8px 18px;
    border-radius: 10px;
    border: none;
}
.nav-btn:hover {
    background: #9b2f23;
    color: white;
}
.nav-right {
    color: white;
    font-size: 20px;
}
h1, h2, h3, p, label {
    color: #111 !important;
}
.card h3,
.card p,
.section-box h3,
.section-box p {
    color: #111 !important;
}
[data-testid="stMarkdownContainer"] {
    color: #111 !important;
}
.hero {
    background-size: cover;
    background-position: center;
    padding: 120px 20px;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 40px;
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
.badge {
    padding: 6px 12px;
    border-radius: 999px;
    background: #e8f5e9;
    color: #1b5e20;
    font-weight: bold;
}
.section-box {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}
.cta-box h2,
.cta-box p {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns([1,1,1,1,2])

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
with col5:
    st.markdown("<div style='text-align:right;font-size:20px;'>🔍 🛒</div>", unsafe_allow_html=True)

if st.session_state.page == "Home":

    st.markdown(f"""
    <div class="hero" style="
        background-image: linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.45)),
        url('https://images.unsplash.com/photo-1653946402577-f2477b1002b7?auto=format&fit=crop&w=1600&q=80');
    ">
        <h1 style="font-size:56px; color:white;">Luigi's Italian Bakery</h1>
        <p style="font-size:22px; color:white;">Don’t be shy, eat some sweets 🍰</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Welcome")
    st.markdown("Fresh Italian bread, pastries, cookies, cakes, and bakery classics made daily.")

    st.markdown("### Featured Favorites")

    cols = st.columns(3)

    demo_items = [
        ("Cannoli", "Classic ricotta filled pastry", "$2.50"),
        ("Italian Bread", "Fresh baked daily", "$4.00"),
        ("Chocolate Cookies", "Soft and rich chocolate cookies", "$3.00")
    ]

    for i, item in enumerate(demo_items):
        with cols[i]:
            st.markdown(f"""
            <div class="card">
                <h3>{item[0]}</h3>
                <p>{item[1]}</p>
                <p class="price">{item[2]}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### Why Choose Us")

    cols = st.columns(3)

    features = [
        ("🍞 Fresh Daily", "Baked fresh every morning"),
        ("🇮🇹 Italian Tradition", "Family recipes passed down"),
        ("🎂 Custom Orders", "Cakes for any event")
    ]

    for i, f in enumerate(features):
        with cols[i]:
            st.markdown(f"""
            <div class="section-box">
                <h3>{f[0]}</h3>
                <p>{f[1]}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="cta-box" style="
        background:#111;
        padding:40px;
        border-radius:20px;
        text-align:center;
        margin-top:40px;
    ">
        <h2>Ready to Order?</h2>
        <p>Visit our shop page to browse fresh bakery items.</p>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "Shop":

    st.title("Shop Our Bakery")

    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/bakery_items?select=*&order=id.desc",
        headers=headers
    )

    items = response.json() if response.status_code == 200 else []

    categories = ["All"] + list(set([item["category"] for item in items if item.get("category")]))
    selected = st.selectbox("Filter by category", categories)

    filtered = items if selected == "All" else [i for i in items if i["category"] == selected]

    cols = st.columns(3)

    for i, item in enumerate(filtered):
        with cols[i % 3]:
            if item.get("image_url"):
                st.image(item["image_url"], use_container_width=True)

            st.markdown(f"""
            <div class="card">
                <h3>{item.get("name","")}</h3>
                <p>{item.get("description","")}</p>
                <p class="price">${item.get("price",0)}</p>
                <span class="badge">Available</span>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.page == "Past Cakes":

    st.title("Our Past Cakes")

    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            st.markdown("""
            <div class="section-box">
                Cake photo coming soon
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.page == "Contact":

    st.title("Contact Us")

    st.markdown("""
    <div class="section-box">
        <p>📍 Lynbrook, NY</p>
        <p>📞 Phone coming soon</p>
        <p>📧 Email coming soon</p>
        <p>🕒 Hours coming soon</p>
    </div>
    """, unsafe_allow_html=True)
