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

# ==========================================
# 1. PAGE & LAYOUT OPTIMIZATION
# ==========================================
st.set_page_config(
    page_title="Lattice: Local Exchange Loop", 
    page_icon="🕸️", 
    layout="centered"
)

# 1.5 Advanced Visual Theme Injection (Fresh Community Theme)
st.markdown("""
<style>
    /* Global Page Background & Clean Typography */
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

# ==========================================
# 2. STATE & MEMORY HUB INITIALIZATION
# ==========================================
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

# 2.5 Geo-Location Engine Utilities
import pgeocode
zip_database = pgeocode.GeoDistance('us')

def calculate_distance(user_zip, item_zip):
    if user_zip == item_zip:
        return 0.0
    try:
        distance_in_km = zip_database.query_postal_code(user_zip, item_zip)
        if math.isnan(distance_in_km):
            return "Unknown Node Zone"
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

# ==========================================
# 3. MAIN INTERFACE HEADER
# ==========================================
st.title("🕸️ Lattice Loop")
st.markdown("A decentralized framework for independent local supply chains.")
st.markdown("---")

# ==========================================
# 4. GLOBAL SIDEBAR UTILITIES & DASHBOARDS
# ==========================================
st.sidebar.markdown("### 🧮 Local Valuation Hub")
with st.sidebar.expander("Currency Calculator", expanded=False):
    usd_input = st.number_input("Enter Amount (USD $)", min_value=0.0, value=10.0, step=1.0)
    time_credits = usd_input / 20.0  
    lattice_tokens = usd_input / 1.50 
    
    st.markdown(f"**⏱️ Time Bank Value:** `{time_credits:.2f} Hours`")
    st.markdown(f"**🪙 Lattice Credits:** `{lattice_tokens:.1f} LTC`")

st.sidebar.markdown("---")

sub_cost = 0.00 if FREE_BETA_MODE else 5.00
platform_split = 0.00 if FREE_BETA_MODE else (sub_cost * 0.50)
charity_split = 0.00 if FREE_BETA_MODE else (sub_cost * 0.50)

if FREE_BETA_MODE:
    st.sidebar.info("🚀 **Alpha Beta Pass Active:** Platform access is completely free for early network nodes!")

st.sidebar.markdown("---")
st.sidebar.markdown("### 💳 System Royalty & Membership Hub")

REGIONAL_MUTUAL_AID_INDEX = {
    "782": ["San Antonio Collective Care", "Mootual Aid SATX", "Community Fridge SATX"], 
    "787": ["Austin Mutual Aid", "ATX Free Fridge", "Grounded in Solidarity"],            
    "770": ["Houston Mutual Aid", "Freedge Houston", "Solidarity Houston"],               
    "100": ["NYC Mutual Aid Pot", "Ridgewood Mutual Aid Project", "Bed-Stuy Strong"],     
    "606": ["Chicago Mutual Aid", "Brave Space Alliance", "Love Fridge Chicago"],         
    "900": ["LA Mutual Aid Network", "Ktown For All", "Food Not Bombs LA"]                
}

active_zip = st.session_state.get("global_zip", "78201")
user_prefix = active_zip[:3] if len(active_zip) >= 3 else "782"
available_collectives = REGIONAL_MUTUAL_AID_INDEX.get(user_prefix, ["National Mutual Aid Disaster Relief Fund"])
chosen_aid_group = st.sidebar.selectbox("Designated Mutual Aid Anchor:", available_collectives)

if chosen_aid_group not in st.session_state.charity_funds:
    st.session_state.charity_funds[chosen_aid_group] = 0.0

button_label = f"Claim Free Beta Membership Pass" if FREE_BETA_MODE else f"Subscribe (${sub_cost:.2f}/mo)"

if st.sidebar.button(button_label):
    st.session_state.subscriber_count += 1
    st.session_state.retained_capital += platform_split
    st.session_state.charity_funds[chosen_aid_group] += charity_split
    st.sidebar.success("Membership activated on the local node grid!")

# 5. MARKETPLACE DISPLAY & TRANSACTIONS
# ==========================================
st.subheader("📍 Your Node Location")
col_zip1, col_zip2 = st.columns(2)
with col_zip1:
    user_zip = st.text_input("Enter Your ZIP Code:", value="78201", max_chars=5, key="global_zip")

with col_zip2:
    st.write("") 
    st.markdown(f"**Connected Hub:** `{user_zip[:3]}...` | **Mutual Aid Anchor:** `{chosen_aid_group}`")

st.markdown("---")
st.subheader("🛒 Local Decentralized Inventory")

if not st.session_state.local_inventory:
    st.info("The local supply chain loop is currently empty. Be the first to list an item!")
else:
    for idx, item in enumerate(st.session_state.local_inventory):
        distance = calculate_distance(user_zip, item["zip"])
        dist_str = f"📍 {distance} miles away" if isinstance(distance, (int, float)) else f"🛑 {distance}"
        
        with st.container():
            col_img, col_details, col_actions = st.columns([1, 2, 1.5])
            
            with col_img:
                if item.get("image"):
                    st.image(item["image"], use_column_width=True)
                else:
                    icon = "🍎" if item["category"] == "Food" else "🧵" if item["category"] == "Goods" else "🛠️" if item["category"] == "Tools" else "💼"
                    st.markdown(f"<h1 style='text-align: center; font-size: 3.5rem; margin:0;'>{icon}</h1>", unsafe_allow_html=True)
            
            with col_details:
                st.markdown(f"### {item['item']}")
                st.markdown(f"**Seller:** `{item['seller']}` | {dist_str}")
                st.markdown(f"**Available Quantity:** `{item['qty']}` units")
                st.markdown(f"💰 **Value Matrix:** `${item['price']:.2f} USD` | `{(item['price']/20.0):.2f} Hrs` | `{(item['price']/1.50):.1f} LTC`")
            
            with col_actions:
                st.write("✨ **Checkout Framework:**")
                trade_btn = st.button(f"🤝 Request P2P Barter", key=f"barter_{item['id']}")
                
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
            
            if trade_btn:
                if item["qty"] > 0:
                    st.session_state.local_inventory[idx]["qty"] -= 1
                    timestamp = datetime.datetime.now().strftime("%H:%M")
                    new_msg = {
                        "zip": user_zip,
                        "alias": f"Node_{user_zip}",
                        "text": f"🚨 TRANSACTION: Requested 1x '{item['item']}' from {item['seller']}.",
                        "time": timestamp
                    }
                    st.session_state.secure_message_wall.insert(0, new_msg)
                    save_json_db(DB_INVENTORY_PATH, st.session_state.local_inventory)
                    save_json_db(DB_MESSAGES_PATH, st.session_state.secure_message_wall)
                    st.success(f"🎉 Order requested! Logs broadcasted to Message Wall.")
                    st.rerun()
                else:
                    st.error("Out of stock!")
                    
        st.markdown("<hr style='margin: 1em 0; border-style: dashed;'>", unsafe_allow_html=True)

# ==========================================
# 6. LOCAL COMMUNICATION WALL & LISTING FORM
# ==========================================
st.write("")
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("💬 Active Network Message Wall")
    for msg in st.session_state.secure_message_wall[:5]:
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
        
        submit_listing = st.form_submit_button("Broadcast to Lattice")
        
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

# ==========================================
# 7. REGIONAL NETWORK LEDGER & STATS
# ==========================================
st.markdown("---")
st.subheader("📊 System Mutual Aid Pools & Capital Overview")

col_stat1, col_stat2, col_stat3 = st.columns(3)
with col_stat1:
    st.metric("Total Node Registrations", f"{st.session_state.subscriber_count} Active Passes")
with col_stat2:
    st.metric("Retained Node Infrastructure Capital", f"${st.session_state.retained_capital:.2f} USD")
with col_stat3:
    current_aid_pool = st.session_state.charity_funds.get(chosen_aid_group, 0.0)
    st.metric("Anchor Mutual Aid Pool Balance", f"${current_aid_pool:.2f} USD")

with st.expander("🔎 View Complete Multi-Hub Ledger Matrix", expanded=False):
    ledger_data = []
    for group, amount in st.session_state.charity_funds.items():
        ledger_data.append({"Mutual Aid Entity": group, "Accrued Resources ($)": f"${amount:.2f}"})
    if ledger_data:
        st.dataframe(pd.DataFrame(ledger_data), use_container_width=True)
    else:
        st.info("No active mutual aid allocations recorded in this session loop yet.")

# ==========================================
# 8. DECENTRALIZED NODE AUTHENTICATION LINK (QR CODE)
# ==========================================
st.markdown("---")
st.subheader("🔗 Node Link & Shareable Network Matrix")

current_app_url = "https://streamlit.app"

try:
    qr_code_generator = segno.make(current_app_url)
    qr_buffer = io.BytesIO()
    qr_code_generator.save(qr_buffer, kind="png", scale=4, dark="#15803d", light="#fcfbf9")
    qr_buffer.seek(0)
    qr_b64 = base64.b64encode(qr_buffer.getvalue()).decode()
    
    col_qr_text, col_qr_img = st.columns()
    with col_qr_text:
        st.write("")
        st.markdown(f"""
        Neighbors can scan this direct secure access key with their mobile phone cameras to sync instantly into this grid location loop **(Hub {user_zip[:3]})**.
        
        *   **App Endpoint:** `{current_app_url}`
        *   **Active Target Grid:** Unincorporated Local Nodes
        """)
    with col_qr_img:
        st.markdown(f'<img src="data:image/png;base64,{qr_b64}" width="150" style="border-radius:8px; border: 1px solid #e2e4df;">', unsafe_allow_html=True)
except Exception as qr_error:
    st.info("Generating dynamic QR access node links... Plug in Segno 
