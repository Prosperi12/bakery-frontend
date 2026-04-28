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
    st.session_state.page = "home"

st.markdown("""
<style>
.stApp {
    background: #fff8ef;
}
div.stButton > button {
    background-color: #111;
    color: white;
    border: none;
    padding: 10px 22px;
    border-radius: 10px;
    font-weight: 600;
}
div.stButton > button:hover {
    background-color: #9b2f23;
    color: white;
}
.nav-box {
    background: #111;
    padding: 15px 30px;
    border-radius: 14px;
    margin-bottom: 25px;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    border-left: 5px solid #9b2f23;
    min-height: 210px;
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
.soldout {
    background: #ffebee;
    color: #b71c1c;
}
.admin-box {
    background: #fff;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}
.section-box {
    background: white;
    padding: 30px;
    border-radius: 18px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="nav-box">', unsafe_allow_html=True)
nav1, nav2, nav3, nav4, nav5 = st.columns([1, 1, 1.3, 1.2, 1])

with nav1:
    if st.button("Home"):
        st.session_state.page = "home"

with nav2:
    if st.button("Shop"):
        st.session_state.page = "shop"

with nav3:
    if st.button("Past Cakes"):
        st.session_state.page = "cakes"

with nav4:
    if st.button("Contact Us"):
        st.session_state.page = "contact"

with nav5:
    st.markdown("<h3 style='color:white; text-align:right;'>🔍 🛒</h3>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

response = requests.get(
    f"{SUPABASE_URL}/rest/v1/bakery_items?select=*&order=id.desc",
    headers=headers
)

items = response.json() if response.status_code == 200 else []

sample_items = [
    {
        "name": "Cannoli",
        "category": "Pastry",
        "price": 4.50,
        "description": "Classic Sicilian cannoli filled with sweet ricotta cream.",
        "available": True,
        "image_url": ""
    },
    {
        "name": "Italian Bread",
        "category": "Bread",
        "price": 5.00,
        "description": "Fresh baked Italian bread with a crisp crust and soft center.",
        "available": True,
        "image_url": ""
    },
    {
        "name": "Rainbow Cookies",
        "category": "Cookies",
        "price": 14.99,
        "description": "Traditional Italian rainbow cookies with almond flavor and chocolate.",
        "available": True,
        "image_url": ""
    },
    {
        "name": "Sfogliatelle",
        "category": "Pastry",
        "price": 4.75,
        "description": "Flaky Italian pastry with a sweet ricotta and citrus filling.",
        "available": True,
        "image_url": ""
    },
    {
        "name": "Pignoli Cookies",
        "category": "Cookies",
        "price": 18.99,
        "description": "Soft almond cookies covered with pine nuts.",
        "available": True,
        "image_url": ""
    },
    {
        "name": "Custom Cake",
        "category": "Cakes",
        "price": 35.00,
        "description": "Fresh custom cakes made for birthdays, holidays, and special events.",
        "available": True,
        "image_url": ""
    }
]

display_items = items if len(items) > 0 else sample_items

if st.session_state.page == "home":
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

    st.subheader("Welcome")
    st.write("Fresh Italian bread, pastries, cookies, cakes, and bakery classics made daily.")

    st.subheader("Featured Favorites")

    featured = display_items[:3]
    cols = st.columns(3)

    for i, item in enumerate(featured):
        with cols[i]:
            st.markdown(f"""
            <div class="card">
                <h3>{item.get("name", "")}</h3>
                <p><b>{item.get("category", "")}</b></p>
                <p>{item.get("description", "")}</p>
                <p class="price">${float(item.get("price", 0)):.2f}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### Why Choose Us")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="section-box">
            <h3>🍞 Fresh Daily</h3>
            <p>Our bread, pastries, and cookies are baked fresh every morning.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="section-box">
            <h3>🇮🇹 Italian Tradition</h3>
            <p>Classic Italian bakery favorites made with family-style recipes.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="section-box">
            <h3>🎂 Custom Orders</h3>
            <p>We make cakes and trays for birthdays, holidays, parties, and events.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style='
        background:#111;
        color:white;
        padding:40px;
        border-radius:16px;
        text-align:center;
        margin-top:25px;
    '>
        <h2>Ready to Order?</h2>
        <p>Visit our shop page to browse fresh bakery items.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Go to Shop"):
        st.session_state.page = "shop"

if st.session_state.page == "shop":
    st.subheader("Our Menu")

    categories = ["All"] + sorted(list(set([item["category"] for item in display_items if item.get("category")])))
    selected_category = st.selectbox("Filter by category", categories)

    filtered_items = display_items if selected_category == "All" else [
        item for item in display_items if item.get("category") == selected_category
    ]

    cols = st.columns(3)

    for i, item in enumerate(filtered_items):
        with cols[i % 3]:
            if item.get("image_url"):
                st.image(item["image_url"], use_container_width=True)

            available_class = "badge" if item.get("available") else "badge soldout"
            available_text = "Available" if item.get("available") else "Sold Out"

            st.markdown(f"""
            <div class="card">
                <h3>{item.get("name", "")}</h3>
                <p><b>{item.get("category", "")}</b></p>
                <p>{item.get("description", "")}</p>
                <p class="price">${float(item.get("price", 0)):.2f}</p>
                <span class="{available_class}">{available_text}</span>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    with st.expander("Admin: Add Items"):
        st.markdown('<div class="admin-box">', unsafe_allow_html=True)

        with st.form("add_item"):
            name = st.text_input("Name")
            category = st.text_input("Category")
            price = st.number_input("Price", min_value=0.0)
            description = st.text_area("Description")
            image_url = st.text_input("Image URL")
            available = st.checkbox("Available", True)

            submit = st.form_submit_button("Add Item")

            if submit:
                res = requests.post(
                    f"{SUPABASE_URL}/rest/v1/bakery_items",
                    headers=headers,
                    json={
                        "name": name,
                        "category": category,
                        "price": price,
                        "description": description,
                        "image_url": image_url,
                        "available": available
                    }
                )

                if res.status_code == 201:
                    st.success("Item added!")
                else:
                    st.error("Error adding item")

        st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.page == "cakes":
    st.subheader("Past Cakes")
    st.write("A gallery of custom cakes and bakery creations will go here.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("Cake photo coming soon")

    with col2:
        st.info("Cake photo coming soon")

    with col3:
        st.info("Cake photo coming soon")

if st.session_state.page == "contact":
    st.subheader("Contact Us")
    st.write("📍 Lynbrook, NY")
    st.write("📞 Phone number coming soon")
    st.write("📧 Email coming soon")
    st.write("🕒 Hours coming soon")
