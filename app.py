import streamlit as st
import requests
from supabase import create_client

SUPABASE_URL = "https://mpgpvcutkibcdhsrbzxh.supabase.co"
SUPABASE_KEY = "sb_publishable_hJXHy_q1nuntSvyQa8lAiQ_zux_SwWi"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

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
    st.session_state.cart[product] = st.session_state.cart.get(product, 0) + 1

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

product_descriptions = {
    "Cannoli": "Classic Sicilian pastry shells filled with sweet ricotta cream.",
    "Italian Bread": "Crusty on the outside, soft on the inside — baked fresh every morning.",
    "Chocolate Cookies": "Rich, fudgy cookies packed with deep chocolate flavor.",
    "Cakes": "Custom-crafted cakes for birthdays, weddings, and every occasion.",
    "Sfogliatelle": "Delicate, shell-shaped pastry layered with semolina and ricotta.",
    "Rainbow Cookies": "Tri-color almond sponge layered with apricot jam and dark chocolate.",
    "Pignoli Cookies": "Chewy almond cookies studded generously with pine nuts.",
    "Anisette Cookies": "Soft, pillowy Italian cookies with a gentle anise fragrance.",
    "Almond Biscotti": "Twice-baked, perfectly crunchy — ideal for dipping in espresso.",
    "Linzertarts": "Buttery shortbread tart with a bright raspberry jam center.",
    "Black and White Cookie": "A New York classic — half vanilla, half chocolate fondant.",
    "Apple Turnover": "Golden, flaky puff pastry wrapped around cinnamon-spiced apples.",
    "Cheese Danish": "Tender pastry filled with lightly sweetened cream cheese.",
    "Tiramisu": "Espresso-soaked ladyfingers layered with mascarpone cream.",
    "Cream Puff": "Light choux pastry filled with fresh vanilla Chantilly cream.",
    "Eclair": "Classic oblong choux topped with glossy dark chocolate ganache."
}

cart_count = sum(st.session_state.cart.values())

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,500&family=Lato:wght@300;400;700&display=swap');

.stApp {
    background: #fdf6ee;
    font-family: 'Lato', sans-serif;
}

div[data-testid="stHorizontalBlock"] > div > div > button {
    background: transparent !important;
    border: none !important;
    font-family: 'Lato', sans-serif !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: #3b2010 !important;
    padding: 10px 18px !important;
    border-radius: 0 !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.25s ease !important;
}
div[data-testid="stHorizontalBlock"] > div > div > button:hover {
    color: #b5451b !important;
    border-bottom: 2px solid #b5451b !important;
    background: transparent !important;
}

.nav-divider {
    height: 2px;
    background: linear-gradient(90deg, #b5451b, #e8a45a, #b5451b);
    border-radius: 2px;
    margin: 0 0 32px 0;
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 38px;
    font-weight: 700;
    color: #2c1304;
    margin: 0 0 6px 0;
    line-height: 1.2;
}
.section-subtitle {
    font-family: 'Lato', sans-serif;
    font-size: 15px;
    color: #7a5c44;
    letter-spacing: 0.5px;
    margin-bottom: 28px;
}

.card {
    background: #ffffff;
    padding: 24px 26px;
    border-radius: 14px;
    box-shadow: 0 4px 20px rgba(60,20,0,0.08);
    border-top: 4px solid #b5451b;
    margin-bottom: 18px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(60,20,0,0.14);
}
.card h2 {
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    color: #2c1304;
    margin: 0 0 6px 0;
}
.card h3 {
    font-family: 'Playfair Display', serif;
    font-size: 19px;
    color: #2c1304;
    margin: 0 0 5px 0;
}
.card p {
    font-family: 'Lato', sans-serif;
    font-size: 14px;
    color: #6b4b33;
    margin: 0 0 8px 0;
    line-height: 1.55;
}
.price {
    font-family: 'Playfair Display', serif !important;
    font-size: 21px !important;
    font-weight: 700 !important;
    color: #b5451b !important;
}
.badge {
    display: inline-block;
    background: #fdf0e6;
    color: #b5451b;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 8px;
    border: 1px solid #e8c9aa;
}

.total-card {
    background: linear-gradient(135deg, #2c1304 0%, #5c2a0e 100%);
    padding: 28px 30px;
    border-radius: 14px;
    margin: 24px 0 10px 0;
}
.total-card h2 {
    font-family: 'Playfair Display', serif;
    color: #f5d9b8 !important;
    font-size: 20px;
    margin: 0 0 6px 0;
}
.total-card .price {
    color: #f5a623 !important;
    font-size: 32px !important;
}

.footer-box {
    background: linear-gradient(135deg, #2c1304 0%, #5c2a0e 100%);
    padding: 52px 40px;
    border-radius: 20px;
    margin-top: 56px;
    text-align: center;
}
.footer-box h3 {
    font-family: 'Playfair Display', serif;
    color: #f5d9b8 !important;
    font-size: 26px;
    margin-bottom: 16px;
}
.footer-box p {
    color: #c9a882 !important;
    font-size: 15px;
    margin: 6px 0;
    letter-spacing: 0.5px;
}
.footer-divider {
    width: 60px;
    height: 2px;
    background: #b5451b;
    margin: 12px auto 20px;
    border-radius: 2px;
}

.contact-detail {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid #f0e4d4;
}
.contact-detail:last-child { border-bottom: none; }
.contact-icon { font-size: 20px; margin-top: 2px; }
.contact-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #b5451b;
    margin-bottom: 2px;
}
.contact-value { font-size: 15px; color: #3b2010; }

.stButton > button {
    background: #b5451b !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Lato', sans-serif !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: 0.8px !important;
    padding: 10px 20px !important;
    transition: background 0.2s ease !important;
}
.stButton > button:hover {
    background: #912f0e !important;
}

.empty-cart {
    text-align: center;
    padding: 60px 20px;
    color: #9b7a60;
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

c1, c2, c3, c_space, c5, c6 = st.columns([1, 1, 1, 4, 1, 1])
with c1:
    if st.button("Home"):
        nav("Home")
with c2:
    if st.button("Shop"):
        nav("Shop")
with c3:
    if st.button("Contact"):
        nav("Contact")
with c5:
    if st.button("🔍"):
        nav("Search")
with c6:
    if st.button(f"🛒  {cart_count}"):
        nav("Cart")

st.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)

if st.session_state.page == "Home":

    st.markdown("""
    <div style='
        background-image:
            linear-gradient(rgba(20,8,0,0.55), rgba(20,8,0,0.55)),
            url("https://images.unsplash.com/photo-1653946402577-f2477b1002b7?auto=format&fit=crop&w=1600&q=80");
        background-size: cover;
        background-position: center;
        padding: 130px 20px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 52px;
    '>
        <p style="font-family:'Lato',sans-serif; font-size:13px; letter-spacing:4px;
                  text-transform:uppercase; color:#e8a45a; margin-bottom:16px;">
            Est. 1987 · Oneonta, New York
        </p>
        <h1 style="font-family:'Playfair Display',serif; font-size:64px;
                   color:#fff; margin:0 0 16px; line-height:1.1;">
            Luigi's Italian Bakery
        </h1>
        <p style="font-family:'Lato',sans-serif; font-size:20px;
                  font-style:italic; color:#c9a882; margin:0 0 36px;">
            Handcrafted with love since the very first loaf.
        </p>
        <div style="display:inline-block; background:#b5451b; color:white;
                    font-family:'Lato',sans-serif; font-weight:700; font-size:13px;
                    letter-spacing:1.5px; text-transform:uppercase;
                    padding:14px 36px; border-radius:8px; cursor:pointer;">
            Browse Our Menu
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Featured Favorites</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">A selection of our most beloved classics, baked fresh daily.</div>', unsafe_allow_html=True)

    home_items = [
        ("Cannoli", "Classic ricotta filled pastry", "$2.50", "Bestseller"),
        ("Italian Bread", "Fresh baked daily", "$4.00", "Daily Fresh"),
        ("Chocolate Cookies", "Soft and rich chocolate cookies", "$3.00", "Fan Favorite"),
        ("Cakes", "Custom cakes for any occasion", "$25+", "Custom Order"),
        ("Sfogliatelle", "Flaky Italian pastry with ricotta filling", "$3.50", "Traditional"),
        ("Rainbow Cookies", "Almond layered cookies with chocolate", "$2.75", "Colorful Classic"),
    ]

    for i in range(0, len(home_items), 3):
        cols = st.columns(3, gap="large")
        for j in range(3):
            if i + j < len(home_items):
                name, desc, price, badge = home_items[i + j]
                with cols[j]:
                    st.markdown(f"""
                    <div class="card">
                        <div class="badge">{badge}</div>
                        <h3>{name}</h3>
                        <p>{product_descriptions.get(name, desc)}</p>
                        <p class="price">{price}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Add to Cart — {name}", key=f"home_{name}"):
                        add_to_cart(name)
                        st.success(f"✓ {name} added to your cart!")

    st.markdown("""
    <div style='
        background: #fff;
        border-radius: 18px;
        padding: 48px 52px;
        margin-top: 48px;
        box-shadow: 0 4px 20px rgba(60,20,0,0.07);
    '>
        <p style="font-family:'Lato',sans-serif;font-size:11px;letter-spacing:3px;
                  text-transform:uppercase;color:#b5451b;font-weight:700;margin:0 0 10px;">
            Our Story
        </p>
        <h2 style="font-family:'Playfair Display',serif;font-size:30px;
                   color:#2c1304;margin:0 0 14px;">
            Made the Old-World Way
        </h2>
        <p style="font-family:'Lato',sans-serif;font-size:15px;color:#6b4b33;
                  line-height:1.75;max-width:680px;margin:0;">
            Every item in our bakery follows recipes passed down through generations.
            We use no shortcuts — just quality ingredients, patient hands, and a wood-fired
            oven that's been the heart of our shop since the day we opened.
            Come in, take your time, and taste the difference tradition makes.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer-box">
        <h3>Visit Us</h3>
        <div class="footer-divider"></div>
        <p>26 Watkins Avenue, Oneonta, NY 13820</p>
        <p style="margin-top:18px;font-size:13px;letter-spacing:2px;
                  text-transform:uppercase;color:#e8a45a;">Hours</p>
        <p>Monday – Saturday &nbsp;·&nbsp; 6:00 AM – 7:00 PM</p>
        <p>Sunday &nbsp;·&nbsp; 6:00 AM – 6:00 PM</p>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "Shop":
    st.markdown('<div class="section-title">Our Bakery</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Everything baked on-site, every single morning.</div>', unsafe_allow_html=True)

    for name in list(product_prices.keys()):
        qty = st.session_state.cart.get(name, 0)
        st.markdown(f"""
        <div class="card">
            <h2>{name}</h2>
            <p>{product_descriptions.get(name, "")}</p>
            <p class="price">${product_prices[name]:.2f}
                <span style="font-family:'Lato',sans-serif;font-size:13px;
                             color:#9b7a60;font-weight:400;margin-left:10px;">per piece</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

        minus_col, qty_col, plus_col, _ = st.columns([1, 1, 1, 6])
        with minus_col:
            if st.button("−", key=f"shop_minus_{name}"):
                remove_one(name)
                st.rerun()
        with qty_col:
            st.markdown(f"""
            <div style="text-align:center;font-family:'Playfair Display',serif;
                        font-size:22px;color:#2c1304;padding-top:6px;">{qty}</div>""",
                        unsafe_allow_html=True)
        with plus_col:
            if st.button("+", key=f"shop_plus_{name}"):
                add_to_cart(name)
                st.rerun()

    shop_total = sum(product_prices[i] * q for i, q in st.session_state.cart.items())

    st.markdown(f"""
    <div class="total-card">
        <h2>Order Total</h2>
        <p class="price">${shop_total:.2f}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(f"Proceed to Checkout  →  ${shop_total:.2f}", key="shop_checkout"):
        if shop_total == 0:
            st.warning("Your cart is empty — add some items first!")
        else:
            order_data = {"items": st.session_state.cart, "total": shop_total}
            res = requests.post(f"{SUPABASE_URL}/rest/v1/orders", headers=headers, json=order_data)
            if res.status_code == 201:
                st.success(f"🎉 Order placed! Thank you. Total: ${shop_total:.2f}")
                st.session_state.cart = {}
                st.rerun()
            else:
                st.error(f"Something went wrong saving your order (status {res.status_code}). Please try again.")

elif st.session_state.page == "Cart":
    st.markdown('<div class="section-title">Your Cart</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Review your selections before checkout.</div>', unsafe_allow_html=True)

    if not st.session_state.cart:
        st.markdown('<div class="empty-cart">Your cart is empty — head to the shop to fill it up.</div>',
                    unsafe_allow_html=True)
    else:
        total = 0
        for item, qty in list(st.session_state.cart.items()):
            price = product_prices[item]
            subtotal = price * qty
            total += subtotal

            st.markdown(f"""
            <div class="card">
                <h2>{item}</h2>
                <p>{product_descriptions.get(item, "")}</p>
                <p class="price">${price:.2f} <span style="font-family:'Lato',sans-serif;
                    font-size:13px;color:#9b7a60;font-weight:400;">each</span></p>
                <p style="margin-top:6px;">
                    <b>Subtotal:</b>
                    <span style="color:#b5451b;font-weight:700;"> ${subtotal:.2f}</span>
                    &nbsp;·&nbsp; Qty: {qty}
                </p>
            </div>
            """, unsafe_allow_html=True)

            minus_col, qty_col, plus_col, _ = st.columns([1, 1, 1, 6])
            with minus_col:
                if st.button("−", key=f"cart_minus_{item}"):
                    remove_one(item)
                    st.rerun()
            with qty_col:
                st.markdown(f"""
                <div style="text-align:center;font-family:'Playfair Display',serif;
                            font-size:22px;color:#2c1304;padding-top:6px;">{qty}</div>""",
                            unsafe_allow_html=True)
            with plus_col:
                if st.button("+", key=f"cart_plus_{item}"):
                    add_to_cart(item)
                    st.rerun()

        st.markdown(f"""
        <div class="total-card">
            <h2>Order Total</h2>
            <p class="price">${total:.2f}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Checkout  →  ${total:.2f}"):
            order_data = {"items": st.session_state.cart, "total": total}
            res = requests.post(f"{SUPABASE_URL}/rest/v1/orders", headers=headers, json=order_data)
            if res.status_code == 201:
                st.success(f"🎉 Order placed! Thank you. Total: ${total:.2f}")
                st.session_state.cart = {}
                st.rerun()
            else:
                st.error(f"Something went wrong saving your order (status {res.status_code}). Please try again.")

elif st.session_state.page == "Search":
    st.markdown('<div class="section-title">Search</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Looking for something specific? Find it here.</div>',
                unsafe_allow_html=True)

    query = st.text_input("", value=st.session_state.search_query,
                          placeholder="e.g. cannoli, tiramisu, bread…")
    st.session_state.search_query = query

    results = [i for i in product_prices if query.lower() in i.lower()] if query else []

    if query and not results:
        st.info("No items matched your search. Try a different term.")

    for r in results:
        st.markdown(f"""
        <div class="card">
            <h3>{r}</h3>
            <p>{product_descriptions.get(r, "")}</p>
            <p class="price">${product_prices[r]:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Add to Cart — {r}", key=f"search_add_{r}"):
            add_to_cart(r)
            st.success(f"✓ {r} added to your cart!")

elif st.session_state.page == "Contact":
    st.markdown('<div class="section-title">Get in Touch</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">We love hearing from our customers. Say hello!</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("""
        <p style="font-family:'Lato',sans-serif;font-size:11px;letter-spacing:3px;
                  text-transform:uppercase;color:#b5451b;font-weight:700;margin:0 0 10px;">
            Send a Message
        </p>
        <h3 style="font-family:'Playfair Display',serif;font-size:22px;color:#2c1304;margin:0 0 20px;">
            We'll get back to you as soon as possible
        </h3>
        """, unsafe_allow_html=True)

        name_col, last_col = st.columns(2)
        with name_col:
            first_name = st.text_input("First Name", key="contact_first")
        with last_col:
            last_name = st.text_input("Last Name", key="contact_last")

        phone_col, email_col = st.columns(2)
        with phone_col:
            phone = st.text_input("Phone", key="contact_phone")
        with email_col:
            email = st.text_input("Email", key="contact_email")

        subject = st.text_input("Subject", key="contact_subject")
        message = st.text_area("Message", height=140, key="contact_message")

        if st.button("Send Message →", key="contact_send"):
            if first_name and email and message:
                st.success("✓ Your message was sent! We'll be in touch soon.")
            else:
                st.warning("Please fill in your name, email, and message.")

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card" style="height:100%;">
            <p style="font-family:'Lato',sans-serif;font-size:11px;letter-spacing:3px;
                      text-transform:uppercase;color:#b5451b;font-weight:700;margin:0 0 10px;">
                Find Us
            </p>
            <h3 style="font-family:'Playfair Display',serif;font-size:22px;
                       color:#2c1304;margin:0 0 22px;">
                Luigi's Italian Bakery
            </h3>
            <div class="contact-detail">
                <div class="contact-icon">📍</div>
                <div>
                    <div class="contact-label">Address</div>
                    <div class="contact-value">26 Watkins Avenue<br>Oneonta, NY 13820</div>
                </div>
            </div>
            <div class="contact-detail">
                <div class="contact-icon">📞</div>
                <div>
                    <div class="contact-label">Phone</div>
                    <div class="contact-value">(493) 489-2933</div>
                </div>
            </div>
            <div class="contact-detail">
                <div class="contact-icon">📧</div>
                <div>
                    <div class="contact-label">Email</div>
                    <div class="contact-value">contactluigi@yahoo.com</div>
                </div>
            </div>
            <div class="contact-detail">
                <div class="contact-icon">🕐</div>
                <div>
                    <div class="contact-label">Hours</div>
                    <div class="contact-value">
                        Mon–Sat: 6:00 AM – 7:00 PM<br>
                        Sunday: 6:00 AM – 6:00 PM
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
