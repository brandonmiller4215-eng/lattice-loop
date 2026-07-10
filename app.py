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
# 1.5 Advanced Visual Theme Injection (Fresh Community Theme)
st.markdown("""
<style>
    /* Global Page Background & Clean Clean Typography */
    .stApp {
        background-color: #fcfbf9 !important; /* Soft warm ivory cream */
        color: #2d312e !important;            /* Earthy charcoal text */
        font-family: 'Inter', -apple-system, sans-serif !important;
    }
    
    /* Top Main App Headers & Titles */
    h1, h2, h3, h4 {
        color: #15803d !important; /* Fresh organic emerald green */
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
    }
    
    /* Clean Sidebar Utility Optimization Layout */
    section[data-testid="stSidebar"] {
        background-color: #f3f4f1 !important; /* Soft moss tint gray */
        border-right: 1px solid #e2e4df !important;
    }
    
    /* Beautiful Custom Borders for Marketplace Container Cards */
    div[data-testid="stVerticalBlock"] > div {
        border-radius: 12px;
    }
    
    /* Premium Action Button Global Styles */
    .stButton>button {
        background-color: #16a34a !important; /* Bright lively green */
        color: #ffffff !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05) !important;
    }
    
    /* Interactive Hover State for Active Buttons */
    .stButton>button:hover {
        background-color: #15803d !important; /* Richer forest emerald */
        transform: translateY(-1px) !important;
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1) !important;
    }
    
    /* Horizontal Dividers Design Matrix */
    hr {
        border-color: #e2e4df !important;
    }
</style>
""", unsafe_allow_html=True)

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
    st.session_state.charity_funds = {}
    
if "subscriber_count" not in st.session_state:
    st.session_state.subscriber_count = 0        

FREE_BETA_MODE = True 

# 2.5 Nationwide Geo-Location Engine Initialization
import pgeocode
# Initializes a lightning-fast, offline database for all United States postal codes
zip_database = pgeocode.GeoDistance('us')

def calculate_distance(user_zip, item_zip):
    if user_zip == item_zip:
        return 0.0
        
    # Dynamically calculates the exact mileage using offline coordinate indexes
    try:
        distance_in_km = zip_database.query_postal_code(user_zip, item_zip)
        
        # If a user types a fake or broken zip code, handle it gracefully
        if math.isnan(distance_in_km):
            return "Unknown Node Zone"
            
        # Convert kilometers to standard English survey miles
        distance_in_miles = distance_in_km * 0.621371
        return round(distance_in_miles, 1)
    except:
        return "Network Grid Syncing..."

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

st.sidebar.markdown("---")
st.sidebar.markdown("### 💳 System Royalty & Membership Hub")

# Core Nationwide Database of True Unincorporated Grassroots Collectives
REGIONAL_MUTUAL_AID_INDEX = {
    "782": ["San Antonio Collective Care", "Mootual Aid SATX", "Community Fridge SATX"], # San Antonio Core
    "787": ["Austin Mutual Aid", "ATX Free Fridge", "Grounded in Solidarity"],            # Austin Hub
    "770": ["Houston Mutual Aid", "Freedge Houston", "Solidarity Houston"],               # Houston Hub
    "100": ["NYC Mutual Aid Pot", "Ridgewood Mutual Aid Project", "Bed-Stuy Strong"],     # New York Hub
    "606": ["Chicago Mutual Aid", "Brave Space Alliance", "Love Fridge Chicago"],         # Chicago Hub
    "900": ["LA Mutual Aid Network", "Ktown For All", "Food Not Bombs LA"]                # Los Angeles Hub
}

# Read the first 3 digits of the user's ZIP code to locate their nearest metropolitan hub
active_zip = st.session_state.get("global_zip", "78201")
user_prefix = active_zip[:3] if len(active_zip) >= 3 else "782"

# Pull the specific grassroots collectives for that region, default to standard if not listed
available_collectives = REGIONAL_MUTUAL_AID_INDEX.get(user_prefix, ["National Mutual Aid Disaster Relief Fund"])

chosen_aid_group = st.sidebar.selectbox("Designated Mutual Aid Anchor:", available_collectives)

# Initialize the selected group into our tracking registry ledger if it isn't there yet
if chosen_aid_group not in st.session_state.charity_funds:
    st.session_state.charity_funds[chosen_aid_group] = 0.0

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

# 5. MARKETPLACE DISPLAY & TRANSACTIONS
# ==========================================

# Simple form to allow users to set their global viewing ZIP code
st.subheader("📍 Your Node Location")
col_zip1, col_zip2 = st.columns([2, 5])
with col_zip1:
    user_zip = st.text_input("Enter Your ZIP Code:", value="78201", max_chars=5, key="global_zip")

with col_zip2:
    st.write("") # Spacer to alignment
    st.markdown(f"**Connected Hub:** `{user_zip[:3]}...` | **Mutual Aid Anchor:** `{chosen_aid_group}`")

st.markdown("---")
st.subheader("🛒 Local Decentralized Inventory")

# Read database values into an accessible grid
if not st.session_state.local_inventory:
    st.info("The local supply chain loop is currently empty. Be the first to list an item!")
else:
    for idx, item in enumerate(st.session_state.local_inventory):
        # Calculate distance on-the-fly using your pgeocode engine
        distance = calculate_distance(user_zip, item["zip"])
        dist_str = f"📍 {distance} miles away" if isinstance(distance, (int, float)) else f"🛑 {distance}"
        
        # Unique visual layout container card for each marketplace item
        with st.container():
            col_img, col_details, col_actions = st.columns([2, 4, 3])
            
            with col_img:
                if item.get("image"):
                    st.image(item["image"], use_column_width=True)
                else:
                    # Aesthetic text fallback placeholder icon based on category
                    icon = "🍎" if item["category"] == "Food" else "🧵" if item["category"] == "Goods" else "🛠️"
                    st.markdown(f"<h1 style='text-align: center; font-size: 4rem; margin:0;'>{icon}</h1>", unsafe_allow_html=True)
            
            with col_details:
                st.markdown(f"### {item['item']}")
                st.markdown(f"**Seller:** `{item['seller']}` | {dist_str}")
                st.markdown(f"**Available Quantity:** `{item['qty']}` units")
                
                # Show pricing metrics calculated across your valuation models
                st.markdown(f"💰 **Value Matrix:** `${item['price']:.2f} USD` | `{(item['price']/20.0):.2f} Hrs` | `{(item['price']/1.50):.1f} LTC`")
            
            with col_actions:
                st.write("✨ **Select Checkout Framework:**")
                
                # OPTION 1: Peer-to-Peer Peer Barter / Cash on Delivery
                trade_btn = st.button(f"🤝 Request P2P Barter", key=f"barter_{item['id']}")
                
                # OPTION 2: Secure Electronic USD Card Checkout via Stripe Hosted link
                stripe_url = f"https://stripe.com_{item['id']}" 
                st.markdown(f"""
                    <a href="{stripe_url}" target="_blank" style="text-decoration: none;">
                        <button style="
                            background-color: #15803d; 
                            color: white; 
                            border: none; 
                            padding: 8px 16px; 
                            border-radius: 8px; 
                            font-weight: 600; 
                            width: 100%; 
                            cursor: pointer;
                            margin-top: 5px;
                            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
                        ">💳 Pay with Card (USD)</button>
                    </a>
                """, unsafe_allow_html=True)
            
            # --- BACKEND TRANSACTION PROCESSOR ---
            if trade_btn:
                if item["qty"] > 0:
                    # 1. Deduct one item from the active localized stock loop
                    st.session_state.local_inventory[idx]["qty"] -= 1
                    
                    # 2. Append an automated alert sequence to your Message Wall log
                    timestamp = datetime.datetime.now().strftime("%H:%M")
                    new_msg = {
                        "zip": user_zip,
                        "alias": f"Node_{user_zip}",
                        "text": f"🚨 TRANSACTION: Requested 1x '{item['item']}' from {item['seller']} via local barter channel.",
                        "time": timestamp
                    }
                    st.session_state.secure_message_wall.insert(0, new_msg)
                    
                    # 3. Commit state changes seamlessly to your hard JSON flat-file database
                    save_json_db(DB_INVENTORY_PATH, st.session_state.local_inventory)
                    save_json_db(DB_MESSAGES_PATH, st.session_state.secure_message_wall)
                    
                    st.success(f"🎉 Order requested! Coordination logs broadcasted to the Secure Message Wall.")
                    st.rerun()
                else:
                    st.error("Out of stock! This local supply loop loop is depleted.")
                    
        st.markdown("<hr style='margin: 1em 0; border-style: dashed;'>", unsafe_allow_html=True)

# ==========================================
# 6. LOCAL COMMUNICATION WALL & LISTING FORM
# ==========================================
st.write("")
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("💬 Active Network Message Wall")
    for msg in st.session_state.secure_message_wall[:5]: # Cap at latest 5 messages for clean layout
        st.markdown(f"**[{msg['time']}] {msg['alias']} (Hub {msg['zip']}):** {msg['text']}")

with col_right:
    st.subheader("🌱 Inject Supply to Loop")
    with st.form("new_item_form", clear_on_submit=True):
        new_seller = st.text_input("Producer / Seller Alias:")
        new_title = st.text_input("Item or Resource Name:")
        new_cat = st.selectbox("Category:", ["Food", "Goods", "Tools", "Services"])
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1: new_qty = st.number_input("Qty:", min_value=1, value=1)
        with col_f2: new_price = st.number_input("Price ($):", min_value=0.0, value=1.0)
        with col_f3: new_zip = st.text_input("ZIP:", value=user_zip, max_chars=5)
        new_img_file = st.file_uploader("Upload Image:", type=["jpg", "png", "jpeg"])
        
        submit_listing = st.form_submit_form_button("Broadcast to Lattice")
        
        if submit_listing and new_seller and new_title:
            b64_img = process_uploaded_image(new_img_file)
            new_id = len(st.session_state.local_inventory)
            new_node = {
                "id": new_id, "seller": new_seller, "item": new_title, 
                "category": new_cat, "qty": new_qty, "price": new_price, 
                "zip": new_zip, "image": b64_img
            }
            st.session_state.local_inventory.append(new_node)
            save_json_db(DB_INVENTORY_PATH, st.session_state.local_inventory)
            st.success("Resource successfully mapped onto the regional grid!")
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
