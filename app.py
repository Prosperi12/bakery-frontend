import streamlit as st
import requests

# Your Supabase info
SUPABASE_URL = "https://mpgpvcutkibcdhsrbzxh.supabase.co"
SUPABASE_KEY = "sb_publishable_hJXHy_q1nuntSvyQa8lAiQ_zux_SwWi"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {sb_publishable_hJXHy_q1nuntSvyQa8lAiQ_zux_SwWi}"
}

st.title("🇮🇹 Luigi's Italian Bakery")

st.header("Menu")

# READ (GET)
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
