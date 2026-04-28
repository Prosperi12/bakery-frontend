import streamlit as st
import requests

SUPABASE_URL = "https://mpgpvcutkibcdhsrbzxh.supabase.co"
SUPABASE_KEY = "sb_publishable_hJXHy_q1nuntSvyQa8lAiQ_zux_SwWi"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}

st.title("🇮🇹 Luigi's Italian Bakery")

st.header("Menu")

st.subheader("Add New Item")

with st.form("add_item_form"):
    name = st.text_input("Name")
    category = st.text_input("Category")
    price = st.number_input("Price", min_value=0.0)
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
            st.success("Item added!")
        else:
            st.write("Error adding item")
            st.write(res.text)

response = requests.get(
    f"{SUPABASE_URL}/rest/v1/bakery_items",
    headers=headers
)

if response.status_code == 200:
    items = response.json()
    for item in items:
        st.write(f"{item['name']} - ${item['price']} ({item['category']})")
else:
    st.write("Error loading items")
