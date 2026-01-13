import streamlit as st
import os
from datetime import datetime

from services.menu_service import get_menu, get_item, reduce_stock
from services.order_service import save_order
from ai.gemini import ask_gemini

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI Restaurant",
    page_icon="🍽️",
    layout="wide"
)

# -------------------------------------------------
# CUSTOM CSS (RED BUTTONS + IMAGE STYLE)
# -------------------------------------------------
st.markdown("""
<style>
.stButton > button {
    background-color: #E63946;
    color: white;
    border-radius: 8px;
    height: 3em;
    font-size: 15px;
}
.stButton > button:hover {
    background-color: #C1121F;
}
img {
    border-radius: 12px;
    max-height: 180px;
    object-fit: cover;
}
</style>
""", unsafe_allow_html=True)

st.title("🍽️ AI Restaurant Manager")

# -------------------------------------------------
# CUSTOMER NAME
# -------------------------------------------------
customer_name = st.text_input("👤 Enter your name")

# -------------------------------------------------
# BASE DIRECTORY (ROBUST)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -------------------------------------------------
# EXPLICIT IMAGE FILE MAPPING (NO MAGIC)
# -------------------------------------------------
IMAGE_FILES = {
    "Masala Dosa": os.path.join(BASE_DIR, "assets", "images", "masala_dosa.png"),
    "Paneer Butter Masala": os.path.join(BASE_DIR, "assets", "images", "paneer_butter_masala.png"),
    "Chicken Biryani": os.path.join(BASE_DIR, "assets", "images", "chicken_biryani.png"),
    "Roti & Dal": os.path.join(BASE_DIR, "assets", "images", "roti_dal.png"),
    "Cold Coffee": os.path.join(BASE_DIR, "assets", "images", "cold_coffee.png"),
}

# -------------------------------------------------
# LOAD MENU (BACKEND ONLY)
# -------------------------------------------------
menu_df = get_menu()

# -------------------------------------------------
# ONE UNIFIED FOOD MENU GRID
# -------------------------------------------------
st.subheader("🍴 Our Menu")

cols_per_row = 3
rows = [menu_df[i:i + cols_per_row] for i in range(0, len(menu_df), cols_per_row)]

for row_items in rows:
    cols = st.columns(cols_per_row)

    for col, (_, item) in zip(cols, row_items.iterrows()):
        with col:
            image_path = IMAGE_FILES.get(item["Item_Name"])

            # -------- IMAGE --------
            if image_path and os.path.exists(image_path):
                st.image(image_path, use_container_width=True)
            else:
                st.error("Image file missing")

            # -------- FOOD INFO --------
            st.markdown(f"### {item['Item_Name']}")
            st.markdown(f"💰 **₹{item['Price']}**")

            # -------- QUANTITY --------
            qty = st.number_input(
                "Quantity",
                min_value=1,
                step=1,
                key=f"qty_{item['Item_Name']}"
            )

            # -------- ORDER BUTTON --------
            if st.button("Order", key=f"order_{item['Item_Name']}"):
                if not customer_name:
                    st.error("Please enter your name first")
                else:
                    item_db = get_item(item["Item_Name"])
                    stock = int(item_db.iloc[0]["Stock"])

                    if qty > stock:
                        st.error("Not enough stock available")
                    else:
                        save_order(
                            customer_name,
                            item["Item_Name"],
                            qty,
                            int(item["Price"])
                        )
                        reduce_stock(item["Item_Name"], qty)
                        st.success("Order placed successfully ✅")

# -------------------------------------------------
# AI SUGGESTION SECTION
# -------------------------------------------------
st.divider()
st.subheader("🤖 Ask the AI")

question = st.text_input(
    "Ask about spicy food, breakfast/lunch/dinner, or recommendations"
)

if st.button("Ask AI"):
    hour = datetime.now().hour
    meal_time = "Breakfast" if hour < 11 else "Lunch" if hour < 17 else "Dinner"

    menu_text = menu_df.to_string(index=False)

    prompt = f"""
You are a restaurant assistant.

Current meal time: {meal_time}

Menu data (hidden from user):
{menu_text}

User question:
{question}

Answer clearly and politely.
"""

    st.info(ask_gemini(prompt))
