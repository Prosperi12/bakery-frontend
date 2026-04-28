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

st.markdown("""
<style>
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #111;
    padding: 15px 30px;
    border-radius: 12px;
    margin-bottom: 25px;
}

.nav-left {
    display: flex;
    gap: 25px;
}

.nav-item {
    color: white;
    font-weight: 500;
    cursor: pointer;
}

.nav-item:hover {
    color: #ffccbc;
}

.nav-right {
    display: flex;
    gap: 20px;
    font-size: 18px;
    color: white;
}
</style>

<div class="navbar">
    <div class="nav-left">
        <div class="nav-item">Home</div>
        <div class="nav-item">Shop</div>
        <div class="nav-item">Past Cakes</div>
        <div class="nav-item">Contact Us</div>
    </div>
    <div class="nav-right">
        🔍 🛒
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.stApp {
    background: #fff8ef;
}
.hero {
    padding: 45px;
    border-radius: 25px;
    background: linear-gradient(135deg, #5c1f1b, #9b2f23);
    color: white;
    text-align: center;
    margin-bottom: 35px;
}
.hero h1 {
    font-size: 56px;
    margin-bottom: 8px;
}
.hero p {
    font-size: 20px;
}
.card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.12);
    margin-bottom: 20px;
    border-left: 6px solid #9b2f23;
}
.price {
    font-size: 24px;
    font-weight: bold;
    color: #9b2f23;
}
.badge {
    display: inline-block;
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
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.hero {
    position: relative;
    height: 420px;
    border-radius: 20px;
    overflow: hidden;
    margin-bottom: 40px;
}

.hero img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.hero-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.45);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: white;
    text-align: center;
}

.hero-overlay h1 {
    font-size: 60px;
    margin-bottom: 10px;
}

.hero-overlay p {
    font-size: 22px;
    font-style: italic;
}
</style>

st.markdown(f"""
    <div style="
        background-image: url('https://images.unsplash.com/photo-1653946402577-f2477b1002b7?auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        padding: 120px 20px;
        border-radius: 20px;
        text-align: center;
        color: white;
    ">
        <h1 style="font-size: 48px; margin-bottom: 10px;">Luigi's Italian Bakery</h1>
        <p style="font-size: 20px;">Don’t be shy, eat some sweets 🍰</p>
    </div>
""", unsafe_allow_html=True)

response = requests.get(
    f"{SUPABASE_URL}/rest/v1/bakery_items?select=*&order=id.desc",
    headers=headers
)

items = response.json() if response.status_code == 200 else []

st.subheader("Our Menu")

categories = ["All"] + sorted(list(set([item["category"] for item in items if item.get("category")])))
selected_category = st.selectbox("Filter by category", categories)

filtered_items = items if selected_category == "All" else [
    item for item in items if item.get("category") == selected_category
]

if len(filtered_items) == 0:
    st.info("No bakery items yet.")
else:
    cols = st.columns(3)

    for index, item in enumerate(filtered_items):
        with cols[index % 3]:
            image = item.get("image_url")

            if image:
                st.image(image, use_container_width=True)

            available_class = "badge" if item.get("available") else "badge soldout"
            available_text = "Available" if item.get("available") else "Sold Out"

            st.markdown(f"""
            <div class="card">
                <h3>{item.get("name", "Untitled Item")}</h3>
                <p><b>{item.get("category", "")}</b></p>
                <p>{item.get("description", "")}</p>
                <p class="price">${item.get("price", 0)}</p>
                <span class="{available_class}">{available_text}</span>
            </div>
            """, unsafe_allow_html=True)

st.divider()

with st.expander("Admin: Manage Bakery Items", expanded=False):
    st.markdown('<div class="admin-box">', unsafe_allow_html=True)
    st.subheader("Add New Item")

    with st.form("add_item_form"):
        name = st.text_input("Item name")
        category = st.text_input("Category")
        price = st.number_input("Price", min_value=0.0, step=0.25)
        description = st.text_area("Description")
        image_url = st.text_input("Image URL")
        available = st.checkbox("Available", value=True)

        submitted = st.form_submit_button("Add Item")

        if submitted:
            data = {
                "name": name,
                "category": category,
                "price": price,
                "description": description,
                "image_url": image_url,
                "available": available
            }

            res = requests.post(
                f"{SUPABASE_URL}/rest/v1/bakery_items",
                headers=headers,
                json=data
            )

            if res.status_code == 201:
                st.success("Item added! Refresh the page to see it.")
            else:
                st.error("Error adding item")
                st.write(res.text)

    st.markdown("</div>", unsafe_allow_html=True)
