import streamlit as st
import pandas as pd
from datetime import date
import urllib.parse
import json

# Page config
st.set_page_config(page_title="VLF Materials Finder", page_icon="🔨", layout="wide")

# ===== PASSWORD - CHANGE THIS =====
ACCESS_PASSWORD = "VLF2025"

# ===== INITIALIZE SESSION STATE =====
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Custom CSS - MODERN DARK THEME WITH NEON ACCENTS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a1628 0%, #1a2332 50%, #0f1b2d 100%) !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
        padding: 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid rgba(0, 217, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 217, 255, 0.15);
    }
    
    .main-header h1 {
        color: #00D9FF !important;
        text-shadow: 0 0 20px rgba(0, 217, 255, 0.5);
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        color: #a0c4ff !important;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    .login-box {
        background: rgba(30, 58, 95, 0.6);
        backdrop-filter: blur(10px);
        padding: 2.5rem 3rem;
        border-radius: 16px;
        border: 1px solid rgba(0, 217, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        max-width: 500px;
        margin: 3rem auto;
    }
    
    .login-box h3 {
        color: #00D9FF !important;
        font-weight: 700 !important;
        text-shadow: 0 0 10px rgba(0, 217, 255, 0.3);
    }
    
    .login-box p {
        color: #a0c4ff !important;
    }
    
    .section-box {
        background: rgba(30, 58, 95, 0.4);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 16px;
        border-left: 4px solid #00D9FF;
        border: 1px solid rgba(0, 217, 255, 0.2);
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    }
    
    .section-box h3 {
        color: #00D9FF !important;
        font-weight: 700 !important;
        text-shadow: 0 0 10px rgba(0, 217, 255, 0.3);
    }
    
    .section-box-purple {
        background: rgba(75, 50, 110, 0.4);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 16px;
        border-left: 4px solid #B86AFF;
        border: 1px solid rgba(184, 106, 255, 0.3);
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    }
    
    .section-box-purple h3 {
        color: #B86AFF !important;
        font-weight: 700 !important;
        text-shadow: 0 0 10px rgba(184, 106, 255, 0.3);
    }
    
    .success-box {
        background: rgba(16, 185, 129, 0.15);
        border-left: 4px solid #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 1rem 0;
        color: #6ee7b7;
    }
    
    .info-box {
        background: rgba(0, 217, 255, 0.15);
        border-left: 4px solid #00D9FF;
        border: 1px solid rgba(0, 217, 255, 0.3);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 1rem 0;
        color: #a0c4ff;
    }
    
    .item-card {
        background: rgba(30, 58, 95, 0.5);
        backdrop-filter: blur(10px);
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border: 1px solid rgba(0, 217, 255, 0.2);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
        border: none;
    }
    
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #B86AFF 0%, #7C3AFF 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(184, 106, 255, 0.4);
    }
    
    .stButton>button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(184, 106, 255, 0.6);
    }
    
    .stButton>button:not([kind="primary"]) {
        background: rgba(0, 217, 255, 0.1);
        color: #00D9FF;
        border: 1px solid rgba(0, 217, 255, 0.3);
    }
    
    .stButton>button:not([kind="primary"]):hover {
        background: rgba(0, 217, 255, 0.2);
        border: 1px solid rgba(0, 217, 255, 0.5);
    }
    
    .stTextInput input {
        background-color: rgba(30, 58, 95, 0.6) !important;
        border: 1px solid rgba(0, 217, 255, 0.3) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
    }
    
    .stTextInput input:focus {
        border-color: #00D9FF !important;
        box-shadow: 0 0 10px rgba(0, 217, 255, 0.3) !important;
    }
    
    .stTextInput label {
        color: #00D9FF !important;
        font-weight: 600 !important;
    }
    
    .stSelectbox label {
        color: #00D9FF !important;
        font-weight: 600 !important;
    }
    
    .stMarkdown {
        color: #a0c4ff !important;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #00D9FF !important;
    }
    
    .stDataFrame {
        border: 1px solid rgba(0, 217, 255, 0.2);
        border-radius: 12px;
        overflow: hidden;
    }
    
    .marketing-box {
        background: rgba(30, 58, 95, 0.3);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid rgba(0, 217, 255, 0.2);
        margin-top: 2rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    }
    
    .marketing-box h3 {
        color: #B86AFF !important;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(184, 106, 255, 0.3);
    }
    
    .marketing-box p, .marketing-box li {
        color: #a0c4ff !important;
    }
    
    .marketing-box strong {
        color: #00D9FF !important;
    }
    
    @media (max-width: 768px) {
        .login-box {
            padding: 1.5rem;
            margin: 1rem;
        }
        .main-header {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ===== CHECK IF USER IS LOGGED IN =====
if not st.session_state.authenticated:
    # SHOW LOGIN SCREEN
    st.markdown("""
    <div class="main-header" style="text-align: center;">
        <h1>🔨 Virtual Labor Force Materials Finder and Calculator</h1>
        <p>Professional Tool for Construction Professionals</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<h3>🔒 Customer Access</h3>', unsafe_allow_html=True)
    st.markdown('<p>This is a premium tool for Virtual Laor Force customers.</p>', unsafe_allow_html=True)
    
    password_input = st.text_input("Enter Your Access Password:", type="password", key="login_pwd")
    
    if st.button("🔓 Login", type="primary", use_container_width=True):
        if password_input == ACCESS_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ Incorrect password. Contact VLF for access.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="marketing-box">', unsafe_allow_html=True)
    st.markdown('<h3>💼 Not a Customer Yet?</h3>', unsafe_allow_html=True)
    
    st.markdown('<p style="color: #a0c4ff; font-weight: 600;">Get instant access to:</p>', unsafe_allow_html=True)
    st.markdown("""
    <ul style="color: #a0c4ff;">
        <li>✅ Daily materials list builder with quantities</li>
        <li>✅ Price tracking & automatic estimate calculations</li>
        <li>✅ Save & reload lists anytime (JSON/CSV)</li>
        <li>✅ Instant search at Home Depot & Lowe's</li>
        <li>✅ Store locator with mapping</li>
        <li>✅ Export lists as formatted text, CSV, or JSON</li>
        <li>✅ Mobile-friendly on any device</li>
    </ul>
    """, unsafe_allow_html=True)
    
    st.markdown('<p style="color: #a0c4ff; font-weight: 600; margin-top: 1rem;">Subscription Plans:</p>', unsafe_allow_html=True)
    st.markdown("""
    <ul style="color: #a0c4ff;">
        <li><strong>Solo Contractor:</strong> $50/month</li>
        <li><strong>Small Crew (3-5):</strong> $100-150/month</li>
        <li><strong>Company License:</strong> $Call for Company Pricing (586)-449-4640</li>
    </ul>
    """, unsafe_allow_html=True)
    
    st.markdown('<p style="color: #a0c4ff; font-weight: 600; margin-top: 1rem;">Contact Us:</p>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color: #a0c4ff;">
        📧 <strong>Email:</strong> virtualadmin@virtuallaborforce.com<br>
        📞 <strong>Phone:</strong> (586)449-4640<br>
        🌐 <strong>Web:</strong> www.virtuallaborforce.com.com
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown('<p style="color: #7c8db5; font-style: italic; margin-top: 1rem;">*We accept CashApp, Cardano, Zelle, and Invoice payments*</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ===== IF WE GET HERE, USER IS AUTHENTICATED =====
if 'material_list' not in st.session_state:
    st.session_state.material_list = []
if 'zip_code' not in st.session_state:
    st.session_state.zip_code = "48201"
if 'input_key' not in st.session_state:
    st.session_state.input_key = 0

# Helper function to calculate total
def calculate_total(material_list):
    total = 0
    for item in material_list:
        price = item.get('Price', 0)
        qty = item.get('Qty', 1)
        if price and qty:
            try:
                total += float(price) * float(qty)
            except (ValueError, TypeError):
                pass
    return total

# Header with logout
col_head1, col_head2 = st.columns([5, 1])
with col_head1:
    st.markdown("""
    <div class="main-header">
        <h1>🔨 Virtual Labor Force Materials Finder and Calculator</h1>
        <p>Save Time on the Job Site | Built by Virtual Labor Force, Detroit, MI</p>
    </div>
    """, unsafe_allow_html=True)
with col_head2:
    st.write("")
    st.write("")
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.rerun()

# ===== ZIP CODE SECTION =====
st.markdown('<div class="section-box">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown("### 📍 Location")
with col2:
    subcol1, subcol2 = st.columns([2, 1])
    with subcol1:
        zip_input = st.text_input("ZIP Code", value=st.session_state.zip_code, 
                                  max_chars=5, label_visibility="collapsed",
                                  placeholder="Enter ZIP code", key="zip_input")
    with subcol2:
        if st.button("🔄 Update", use_container_width=True):
            if zip_input.isdigit() and len(zip_input) == 5:
                st.session_state.zip_code = zip_input
                st.success(f"✓ Updated to {zip_input}")
            else:
                st.error("Invalid ZIP")
st.markdown('</div>', unsafe_allow_html=True)

# ===== LOAD PREVIOUS LIST SECTION =====
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown("### 📂 Load Previous List")

uploaded_file = st.file_uploader("Import a previously saved list", type=['json', 'csv'], 
                                 label_visibility="collapsed",
                                 help="Upload a JSON or CSV file you previously exported")

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.json'):
            # Load JSON
            data = json.load(uploaded_file)
            st.session_state.material_list = data
            st.success(f"✅ Loaded {len(data)} items from {uploaded_file.name}")
            st.rerun()
        elif uploaded_file.name.endswith('.csv'):
            # Load CSV
            df = pd.read_csv(uploaded_file)
            # Ensure required columns exist
            if 'Item' not in df.columns:
                st.error("CSV must have an 'Item' column")
            else:
                # Fill missing columns with defaults
                if 'Qty' not in df.columns:
                    df['Qty'] = 1
                if 'Price' not in df.columns:
                    df['Price'] = 0.0
                if 'Store' not in df.columns:
                    df['Store'] = ""
                if 'Added' not in df.columns:
                    df['Added'] = date.today().strftime("%m/%d/%Y")
                
                st.session_state.material_list = df.to_dict('records')
                st.success(f"✅ Loaded {len(df)} items from {uploaded_file.name}")
                st.rerun()
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# ===== ADD MATERIALS SECTION =====
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown("### ➕ Add Materials")

col1, col2, col3 = st.columns([4, 1, 1])
with col1:
    new_item = st.text_input(
        "Item", 
        key=f"item_input_{st.session_state.input_key}",
        label_visibility="collapsed",
        placeholder="e.g., '4x30 wood door, 6 panel' or '10 3.5\" hinges'"
    )
with col2:
    new_qty = st.number_input("Quantity", min_value=1, value=1, step=1, 
                               label_visibility="collapsed", key=f"qty_input_{st.session_state.input_key}")
with col3:
    if st.button("➕ Add", type="primary", use_container_width=True):
        if new_item and new_item.strip():
            st.session_state.material_list.append({
                "Item": new_item.strip(),
                "Qty": new_qty,
                "Price": 0.0,
                "Store": "",
                "Added": date.today().strftime("%m/%d/%Y")
            })
            st.session_state.input_key += 1
            st.rerun()
        else:
            st.warning("⚠️ Please enter an item")

st.markdown('</div>', unsafe_allow_html=True)

# ===== MATERIALS LIST SECTION =====
if st.session_state.material_list:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown(f"### 📋 Today's List ({len(st.session_state.material_list)} items)")
    
    # Add instructions
    st.markdown("""
    <p style="color: #a0c4ff; font-size: 0.9rem; margin-bottom: 1rem;">
    💡 <strong>Tip:</strong> After searching for items below, come back here and enter the prices you find. The total estimate will calculate automatically!
    </p>
    """, unsafe_allow_html=True)
    
    df = pd.DataFrame(st.session_state.material_list)
    
    # Ensure all columns exist
    if 'Qty' not in df.columns:
        df['Qty'] = 1
    if 'Price' not in df.columns:
        df['Price'] = 0.0
    if 'Store' not in df.columns:
        df['Store'] = ""
    
    edited_df = st.data_editor(
        df, 
        num_rows="dynamic", 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Item": st.column_config.TextColumn("Material Item", width="large", required=True),
            "Qty": st.column_config.NumberColumn("Qty", width="small", min_value=1, default=1),
            "Price": st.column_config.NumberColumn("Price ($)", width="medium", format="$%.2f", min_value=0),
            "Store": st.column_config.SelectboxColumn("Store", width="medium", 
                options=["", "Home Depot", "Lowe's", "Other"]),
            "Added": st.column_config.TextColumn("Date", width="small")
        },
        column_order=["Item", "Qty", "Price", "Store", "Added"]
    )
    st.session_state.material_list = edited_df.to_dict('records')
    
    # Calculate and display total
    total = calculate_total(st.session_state.material_list)
    
    if total > 0:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                    padding: 1.5rem; border-radius: 12px; margin: 1rem 0;
                    border: 1px solid rgba(16, 185, 129, 0.5);
                    box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);">
            <h3 style="color: white; margin: 0; font-size: 1.8rem; text-align: center;">
                💰 Estimated Total: ${total:,.2f}
            </h3>
            <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; text-align: center; font-size: 0.9rem;">
                Based on prices entered • Excludes tax & fees
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.material_list = []
            st.rerun()
    with col2:
        # Better formatted text export
        list_text = "=" * 50 + "\n"
        list_text += "VLF MATERIALS LIST\n"
        list_text += f"Date: {date.today().strftime('%m/%d/%Y')}\n"
        list_text += f"ZIP Code: {st.session_state.zip_code}\n"
        list_text += "=" * 50 + "\n\n"
        
        for idx, item in enumerate(st.session_state.material_list, 1):
            qty = item.get('Qty', 1)
            price = item.get('Price', 0)
            store = item.get('Store', '')
            item_total = float(qty) * float(price) if price else 0
            
            list_text += f"#{idx}. {item['Item']}\n"
            list_text += f"    Quantity: {qty}\n"
            list_text += f"    Price: ${price:.2f} each\n"
            if store:
                list_text += f"    Store: {store}\n"
            list_text += f"    Subtotal: ${item_total:.2f}\n"
            list_text += "\n"
        
        list_text += "=" * 50 + "\n"
        list_text += f"TOTAL ESTIMATE: ${total:,.2f}\n"
        list_text += "=" * 50 + "\n"
        list_text += "\n(Excludes tax & fees)\n"
        
        st.download_button("📋 Text List", list_text, 
                          f"materials_list_{date.today().strftime('%Y%m%d')}.txt", 
                          "text/plain", use_container_width=True)
    with col3:
        csv = edited_df.to_csv(index=False)
        st.download_button("📥 CSV Export", csv, 
                          f"materials_list_{date.today().strftime('%Y%m%d')}.csv", 
                          "text/csv", use_container_width=True)
    with col4:
        # JSON export for perfect reload
        json_data = json.dumps(st.session_state.material_list, indent=2)
        st.download_button("💾 JSON Export", json_data, 
                          f"materials_list_{date.today().strftime('%Y%m%d')}.json",
                          "application/json", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="info-box">
        <p style="margin: 0; color: #a0c4ff;">💡 <strong>No materials added yet</strong> — start building your list above, or load a previously saved list!</p>
    </div>
    """, unsafe_allow_html=True)

# ===== STORE SEARCH SECTION =====
if st.session_state.material_list:
    st.markdown('<div class="section-box-purple">', unsafe_allow_html=True)
    st.markdown("### 🛒 Search at Stores")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        store_choice = st.selectbox("Select Store:", ["Home Depot", "Lowe's"], label_visibility="collapsed")
    with col2:
        if st.button("🔍 Generate Search Links", type="primary", use_container_width=True):
            st.session_state.show_results = True
            st.rerun()
    
    if st.session_state.get('show_results', False):
        zip_code = st.session_state.zip_code
        
        st.markdown(f"""
        <div class="success-box">
            <p style="margin: 0; color: #6ee7b7;"><strong>✓ Generated search links for {len(st.session_state.material_list)} items at {store_choice} near ZIP {zip_code}</strong><br>
            <small>Click any link below to open in new tab — prices and aisle info shown on store website</small></p>
        </div>
        """, unsafe_allow_html=True)
        
        results = []
        for item in st.session_state.material_list:
            query = urllib.parse.quote_plus(item['Item'])
            
            if store_choice == "Home Depot":
                search_url = f"https://www.homedepot.com/s/{query}?NCNI-5&searchRedirect=true&zip={zip_code}"
                store_locator = f"https://www.google.com/maps/search/Home+Depot+near+{zip_code}"
                color = "#F96302"
                icon = "🟠"
            else:
                search_url = f"https://www.lowes.com/search?searchTerm={query}"
                store_locator = f"https://www.google.com/maps/search/Lowes+near+{zip_code}"
                color = "#004990"
                icon = "🔵"
            
            results.append({
                "Item": item['Item'],
                "Search URL": search_url,
                "Store Locator": store_locator,
                "Color": color,
                "Icon": icon
            })
        
        for idx, result in enumerate(results, 1):
            st.markdown(f"""
            <div class="item-card" style="border-left: 4px solid {result['Color']};">
                <strong style="font-size: 1.1rem; color: #00D9FF;">{result['Icon']} #{idx} — {result['Item']}</strong>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**[🔍 Search This Item]({result['Search URL']})**")
            with col2:
                st.markdown(f"**[📍 Find Nearby Stores (Map)]({result['Store Locator']})**")
            
            st.markdown("<br>", unsafe_allow_html=True)
        
        with st.expander("💡 How to Find Aisle Locations & Prices"):
            st.markdown("""
            **Finding Items & Prices:**
            1. Click **"Search This Item"** to see all matching products
            2. Select the specific product you need
            3. **Note the price** displayed on the product page
            4. On product page, click **"Check Nearby Stores"**
            5. Choose your preferred store location
            6. View **aisle/bay number** and **real-time inventory**
            7. **Come back here** and enter the price in the "Price" column above
            
            **Building Your Estimate:**
            - Enter prices as you find them for each item
            - Select which store you found it at (optional)
            - The **Total Estimate** will calculate automatically
            - Download your complete list with prices for record-keeping
            
            **Finding Stores:**
            - Click **"Find Nearby Stores"** to see all locations on Google Maps
            - Shows distance, hours, and directions
            - Click any store to get directions or call
            
            **Pro tip:** Right-click links → "Open in New Tab" to keep your list visible while searching!
            """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===== FOOTER =====
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #7c8db5; padding: 1rem 0;">
    <p style="margin: 0.25rem 0;">⚙️ <strong style="color: #00D9FF;">Virtual Labor Force Detroit, Michigan an AI Custom Solutions Company</strong> | AI Tools for Construction</p>
    <p style="margin: 0.25rem 0;">📧 Need help? Contact virtualadmin@virtuallaborforce.com</p>
    <p style="margin: 0.25rem 0;">📅 {date.today().strftime('%m/%d/%Y')}</p>
</div>
""", unsafe_allow_html=True)
