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
    padding: 15px 40px;
    border-radius: 12px;
    margin-bottom: 25px;
}
.nav-left {
    display: flex;
    gap: 40px;
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

st.markdown("""
<style>
.stApp {
    background: #fff8ef;
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
            <p class="price">${item.get("price", 0)}</p>
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
