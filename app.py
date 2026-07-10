import streamlit as st
import pandas as pd
import base64
from PIL import Image
import io
import datetime
import json
import os
import segno
import math

# 1. Page & Layout Optimization
st.set_page_config(
    page_title="Lattice: Local Exchange Loop", 
    page_icon="🕸️", 
    layout="centered"
)

# 2. State & Memory Hub Initialization (JSON Flat-File Database Version)
DB_INVENTORY_PATH = "inventory_db.json"
DB_MESSAGES_PATH = "messages_db.json"

def load_json_db(file_path, default_data):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except:
            return default_data
    return default_data

def save_json_db(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

DEFAULT_INVENTORY = [
    {"id": 0, "seller": "Oak Street Collective", "item": "Organic Tomatoes", "category": "Food", "qty": 15, "price": 3.50, "zip": "78201", "image": None},
    {"id": 1, "seller": "Elena's Textiles", "item": "Handmade Wool Blanket", "category": "Goods", "qty": 3, "price": 65.00, "zip": "78201", "image": None},
    {"id": 2, "seller": "Community Tool Library", "item": "Rototiller Rental", "category": "Tools", "qty": 1, "price": 10.00, "zip": "78212", "image": None},
    {"id": 3, "seller": "Mendoza Farm", "item": "Free-Range Eggs (Dozen)", "category": "Food", "qty": 12, "price": 5.00, "zip": "78212", "image": None},
]

DEFAULT_MESSAGES = [
    {"zip": "78201", "alias": "AnonNode_1", "text": "Leaving seeds at the community box on Main St at noon.", "time": "10:15"},
    {"zip": "78212", "alias": "ToolShare_Alpha", "text": "Rototiller is cleaned, sanitized, and ready for pickup.", "time": "09:30"}
]

if "local_inventory" not in st.session_state:
    st.session_state.local_inventory = load_json_db(DB_INVENTORY_PATH, DEFAULT_INVENTORY)

if "secure_message_wall" not in st.session_state:
    st.session_state.secure_message_wall = load_json_db(DB_MESSAGES_PATH, DEFAULT_MESSAGES)

if "retained_capital" not in st.session_state:
    st.session_state.retained_capital = 0.0      

if "charity_funds" not in st.session_state:
    st.session_state.charity_funds = {            
        "San Antonio Collective Care": 0.0,
        "Mootual Aid SATX": 0.0,
        "Community Fridge SATX": 0.0
    }

if "subscriber_count" not in st.session_state:
    st.session_state.subscriber_count = 0        

FREE_BETA_MODE = True 

# Global Coordinate Directory Mapping Index (Expandable for expansion nodes)
ZIP_COORDINATE_DIRECTORY = {
    # San Antonio Base Core
    "78201": (29.4678, -98.5235), "78212": (29.4524, -98.4912), 
    "78207": (29.4312, -98.5312), "78209": (29.4891, -98.4513),
    # Austin Grid Expansion Samples
    "78701": (30.2729, -97.7444), "78704": (30.2451, -97.7641),
    # Houston Grid Expansion Samples
    "77002": (29.7568, -95.3659), "77006": (29.7423, -95.3921),
    # NY Grid Expansion Samples
    "10001": (40.7501, -73.9963), "10011": (40.7420, -74.0011)
}

# The Haversine Formula: Great-Circle Navigation Distance Calculator Engine
def calculate_distance(user_zip, item_zip):
    if user_zip == item_zip:
        return 0.0
        
    if user_zip not in ZIP_COORDINATE_DIRECTORY or item_zip not in ZIP_COORDINATE_DIRECTORY:
        return "Unknown Network Node Zone"
        
    lat1, lon1 = ZIP_COORDINATE_DIRECTORY[user_zip]
    lat2, lon2 = ZIP_COORDINATE_DIRECTORY[item_zip]
    
    # Earth Radius multiplier in standard English Survey Miles
    earth_radius_miles = 3958.8 
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = (math.sin(dlat / 2) ** 2 + 
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
         
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(earth_radius_miles * c, 1)

def process_uploaded_image(uploaded_file):
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image.thumbnail((300, 300)) 
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=70)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/jpeg;base64,{img_str}"
    return None

# 3. Main Interface Header
st.title("🕸️ Lattice Loop")
st.markdown("A decentralized framework for independent local supply chains.")
st.markdown("---")

# 4. Global Sidebar Utilities & Dashboards
st.sidebar.markdown("### 🧮 Local Valuation Hub")
with st.sidebar.expander("Currency Calculator", expanded=False):
    usd_input = st.number_input("Enter Amount (USD $)", min_value=0.0, value=10.0, step=1.0)
    time_credits = usd_input / 20.0  
    lattice_tokens = usd_input / 1.50 
    
    st.markdown(f"**⏱️ Time Bank Value:** `{time_credits:.2f} Hours`")
    st.markdown(f"**🪙 Lattice Credits:** `{lattice_tokens:.1f} LTC`")

st.sidebar.markdown("---")
st.sidebar.markdown("### 💳 System Royalty & Membership Hub")

sub_cost = 0.00 if FREE_BETA_MODE else 5.00
platform_split = 0.00 if FREE_BETA_MODE else (sub_cost * 0.50)
charity_split = 0.00 if FREE_BETA_MODE else (sub_cost * 0.50)

if FREE_BETA_MODE:
    st.sidebar.info("🚀 **Alpha Beta Pass Active:** Platform access is completely free for early network nodes!")

chosen_aid_group = st.sidebar.selectbox(
    "Designated Mutual Aid Anchor:", 
    ["San Antonio Collective Care", "Mootual Aid SATX", "Community Fridge SATX"]
)

button_label = f"Claim Free Beta Membership Pass" if FREE_BETA_MODE else f"Subscribe (${sub_cost:.2f}/mo)"

if st.sidebar.button(button_label):
    st.session_state.subscriber_count += 1
    st.session_state.retained_capital += platform_split
    st.session_state.charity_funds[chosen_aid_group] += charity_split
    
    success_text = "Free pass activated! Welcome to the local loop." if FREE_BETA_MODE else "Subscription processed! Proceeds distributed."
    st.sidebar.success(success_text)
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Network Treasury Dashboard")
st.sidebar.metric("Active Subscribed Nodes", f"{st.session_state.subscriber_count} Members")

if FREE_BETA_MODE:
    st.sidebar.caption("🔒 *Financial tracking metrics will activate once your pilot phase is complete.*")
else:
    st.sidebar.metric("Your Retained Royalties (50%)", f"${st.session_state.retained_capital:.2f}")
    st.sidebar.markdown("#### 🛰️ Direct Grassroots Distributions (50%)")
    for group, total_amount in st.session_state.charity_funds.items():
        st.sidebar.write(f" * **{group}:** `${total_amount:.2f}`")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📲 Share the Local Loop")
with st.sidebar.expander("Generate Network QR Code", expanded=False):
    app_url = "https://streamlit.app"
    qr = segno.make_qr(app_url)
    buffer = io.BytesIO()
    qr.save(buffer, kind="png", scale=5)
    buffer.seek(0)
    st.image(buffer, caption="Scan to join this neighborhood node!", use_container_width=True)
    st.caption("✨ Tip: Take a screenshot of this QR code to print on local flyers!")

# 5. Interface Action Selector
view_mode = st.radio(
    "Select System Action:", 
    ["Find Local Needs", "Register Local Supply", "Secure Community Wall"], 
    horizontal=True
)

st.markdown("---")

# 6. Controller Logic: Find Local Needs
if view_mode == "Find Local Needs":
    st.subheader("🔍 Local Network Query")
    user_zip = st.text_input("Enter Your Current ZIP Code Location", value="78201", max_chars=5).strip()
    
    col_search, col_cat = st.columns(2)
    with col_search:
        search_query = st.text_input("Search items by keyword...", value="").strip().lower()
    with col_cat:
        category_filter = st.selectbox("Category Filter", ["All", "Food", "Goods", "Tools", "Services"])
    
    current_items = st.session_state.local_inventory
    filtered_items = []
    
    for item in current_items:
        dist = calculate_distance(user_zip, item["zip"])
        item_copy = item.copy()
        item_copy["distance"] = dist
        filtered_items.append(item_copy)
            
    if category_filter != "All":
        filtered_items = [i for i in filtered_items if i["category"] == category_filter]
        
    if search_query:
        filtered_items = [
            i for i in filtered_items 
            if search_query in i["item"].lower() or search_query in i["seller"].lower()
        ]
        
    filtered_items = sorted(
        filtered_items, 
        key=lambda x: x["distance"] if isinstance(x["distance"], (int, float)) else 99999
    )
    
    if not filtered_items:
        st.info("No matching local supply nodes found within range.")
    else:
        st.write(f"### Matching Options ({len(filtered_items)} found):")
        for item in filtered_items:
            with st.container():
                col_img, col_info, col_action = st.columns(3)
                with col_img:
                    if item.get("image"):
                        st.image(item["image"], use_column_width=True)
                    else:
                        st.markdown("🖼️\n*(No Image)*")
                with col_info:
                    st.markdown(f"#### **{item['item']}**")
                    st.markdown(f"*By: {item['seller']}*")
                    
                    if item["distance"] == 0.0:
                        st.markdown("📍 **Distance:** `Right in your immediate ZIP!`")
                    elif isinstance(item["distance"], (int, float)):
                        st.markdown(f"📍 **Distance:** `{item['distance']} miles away`")
                    else:
                        st.markdown(f"📍 **Distance:** `{item['distance']}`")
                        
                    st.markdown(f"Category: `{item['category']}` | **Price:** ${item['price']:.2f}")
                with col_action:
                    st.write(f"Available: {item['qty']}") 
                    if item["qty"] <= 0:
                        st.button("Sold Out", key=f"dead_{item['id']}", disabled=True)
                    else:
                        if st.button(f"Acquire", key=f"buy_{item['id']}"):
                            for original_item in st.session_state.local_inventory:
                                if original_item["id"] == item["id"]:
                                    original_item["qty"] -= 1
                            save_json_db(DB_INVENTORY_PATH, st.session_state.local_inventory)
                            st.success(f"Acquired! 100% of revenue routed directly to {item['seller']}.")
                            st.rerun()
                st.markdown("---")

# 7. Controller Logic: Register Local Supply
elif view_mode == "Register Local Supply":
    st.subheader("🌾 Broadcast New Production Capacity")
    with st.form("inventory_form", clear_on_submit=True):
        new_seller = st.text_input("Seller / Collective Name").strip()
        new_item = st.text_input("Resource or Skill Provided").strip()
        new_cat = st.selectbox("Classification", ["Food", "Goods", "Tools", "Services"])
        new_qty = st.number_input("Available Stock Quantity", min_value=1, value=5, step=1)
        new_price = st.number_input("Resource Value ($ per unit)", min_value=0.01, value=1.00, step=0.50)
        new_zip = st.text_input("Local ZIP Coordinates", value="78201", max_chars=5).strip()
        uploaded_img = st.file_uploader("Upload or Snap a Photo of Your Item", type=["jpg", "jpeg", "png"], accept_multiple_files=False, help="Max file size: 2MB")
        
        submit_btn = st.form_submit_button("Broadcast to Grid")
        if submit_btn:
            if not new_seller or not new_item or not new_zip:
                st.error("All structural data fields must be populated.")
            else:
                base64_image = process_uploaded_image(uploaded_img)
                next_id = len(st.session_state.local_inventory)
                st.session_state.local_inventory.append({
                    "id": next_id, "seller": new_seller, "item": new_item, "category": new_cat,
                    "qty": int(new_qty), "price": float(new_price), "zip": new_zip, "image": base64_image
                })
                save_json_db(DB_INVENTORY_PATH, st.session_state.local_inventory)
                st.success(f"Successfully broadcasted {new_item}.")
                st.rerun()

# 8. Controller Logic: Secure Community Wall
elif view_mode == "Secure Community Wall":
    st.subheader("💬 Untraceable Neighborhood Broadcast Wall")
    st.markdown("🔒 *Messages exist solely in temporary server RAM. No storage disks or user profile data logged.*")
    user_zip = st.text_input("Enter Your Location ZIP to Filter Local Transmissions", value="78201", max_chars=5).strip()
    
    with st.form("message_form", clear_on_submit=True):
        col_alias, col_txt = st.columns()
        with col_alias:
            msg_alias = st.text_input("Temporary Alias", value="AnonNode", max_chars=15).strip()
        with col_txt:
            msg_text = st.text_input("Broadcast Message", placeholder="What's happening in your local loop?").strip()
            
        submit_msg = st.form_submit_button("Broadcast Secure Transmission")
        if submit_msg:
            if not msg_text:
                st.error("Cannot broadcast an empty message transmission.")
            else:
                now_str = datetime.datetime.now().strftime("%H:%M")
                st.session_state.secure_message_wall.insert(0, {
                    "zip": user_zip,
                    "alias": msg_alias if msg_alias else "AnonNode",
                    "text": msg_text,
                    "time": now_str
                })
                save_json_db(DB_MESSAGES_PATH, st.session_state.secure_message_wall)
                st.success("Transmission added to local RAM grid!")
                st.rerun()

    st.markdown("### 🛰️ Live Grid Transmissions")
    grid_messages = [m for m in st.session_state.secure_message_wall if m["zip"] == user_zip]
    
    if not grid_messages:
        st.info(f"No active local transmissions found on the wall for ZIP {user_zip}.")
    else:
        for msg in grid_messages:
            with st.chat_message("user", avatar="🕸️"):
                st.markdown(f"**{msg['alias']}** `[{msg['time']}]` (ZIP: {msg['zip']})")
                st.write(msg["text"])
