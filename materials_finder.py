import streamlit as st
import pandas as pd
from datetime import date
import urllib.parse
import json

# Page config
st.set_page_config(page_title="VLF Materials Finder & Calculator", page_icon="🔨", layout="wide")

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
    
    .stNumberInput label {
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
        <h1>🔨 VLF Materials Finder</h1>
        <p>Professional Tool for Construction Professionals</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<h3>🔒 Customer Access</h3>', unsafe_allow_html=True)
    st.markdown('<p>This is a premium tool for Virtual Labor Force clients ONLY!</p>', unsafe_allow_html=True)
    
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
        <li><strong>Solo Contractor:</strong> $10/month</li>
        <li><strong>Small Crew (3-5):</strong> $35/month</li>
        <li><strong>Company License:</strong> CALL FOR PRICING and more Customization (586)449-4640 Actual Human Will Answer, AI is to assist us all NOT to replace the HUMAN connection</li>
    </ul>
    """, unsafe_allow_html=True)
    
    st.markdown('<p style="color: #a0c4ff; font-weight: 600; margin-top: 1rem;">Contact Us:</p>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color: #a0c4ff;">
        📧 <strong>Email:</strong> virtualadmin@virtuallaborforce.com<br>
        📞 <strong>Phone:</strong> (586)449-4640<br>
        🌐 <strong>Web:</strong> www.virtuallaborforce.com
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown('<p style="color: #7c8db5; font-style: italic; margin-top: 1rem;">*We accept Cardano, Bitcoin, Zelle, and Invoice payments*</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ===== IF WE GET HERE, USER IS AUTHENTICATED =====
if 'material_list' not in st.session_state:
    st.session_state.material_list = []
if 'zip_code' not in st.session_state:
    st.session_state.zip_code = "48201"
if 'input_key' not in st.session_state:
    st.session_state.input_key = 0
if 'customer_name' not in st.session_state:
    st.session_state.customer_name = ""
if 'labor_hours' not in st.session_state:
    st.session_state.labor_hours = 0.0
if 'hourly_rate' not in st.session_state:
    st.session_state.hourly_rate = 0.0

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

# Helper function to calculate labor cost
def calculate_labor_cost(hours, rate):
    try:
        return float(hours) * float(rate)
    except (ValueError, TypeError):
        return 0

# Header with logout
col_head1, col_head2 = st.columns([5, 1])
with col_head1:
    st.markdown("""
    <div class="main-header">
        <h1>🔨 VLF Materials Finder</h1>
        <p>Save Time on the Job Site | Built by Virtual Labor Force, Detroit</p>
    </div>
    """, unsafe_allow_html=True)
with col_head2:
    st.write("")
    st.write("")
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.rerun()

# ===== CUSTOMER & JOB INFORMATION SECTION =====
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown("### 👤 Customer & Job Information")

col1, col2 = st.columns(2)
with col1:
    customer_name = st.text_input(
        "Customer Name", 
        value=st.session_state.customer_name,
        placeholder="Enter customer name for this job",
        key="customer_name_input"
    )
    if customer_name != st.session_state.customer_name:
        st.session_state.customer_name = customer_name

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

# ===== LABOR COSTS SECTION =====
st.markdown('<div class="section-box-purple">', unsafe_allow_html=True)
st.markdown("### ⏰ Labor Information")

col1, col2, col3 = st.columns([2, 2, 2])
with col1:
    labor_hours = st.number_input(
        "Hours", 
        min_value=0.0, 
        value=float(st.session_state.labor_hours),
        step=0.5,
        format="%.1f",
        help="Total hours for this job"
    )
    if labor_hours != st.session_state.labor_hours:
        st.session_state.labor_hours = labor_hours

with col2:
    hourly_rate = st.number_input(
        "Rate ($/hour)", 
        min_value=0.0, 
        value=float(st.session_state.hourly_rate),
        step=1.0,
        format="%.2f",
        help="Hourly rate for this specific job"
    )
    if hourly_rate != st.session_state.hourly_rate:
        st.session_state.hourly_rate = hourly_rate

with col3:
    labor_cost = calculate_labor_cost(labor_hours, hourly_rate)
    st.markdown(f"""
    <div style="background: rgba(184, 106, 255, 0.2); padding: 1rem; border-radius: 8px; margin-top: 25px;">
        <div style="color: #B86AFF; font-weight: bold; text-align: center;">Labor Cost</div>
        <div style="color: #fff; font-size: 1.4rem; font-weight: bold; text-align: center;">${labor_cost:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

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
            
            # Handle both old format (just materials) and new format (with customer/labor data)
            if isinstance(data, list):
                # Old format - just materials list
                st.session_state.material_list = data
                st.success(f"✅ Loaded {len(data)} items from {uploaded_file.name}")
            elif isinstance(data, dict):
                # New format - full job data
                if 'customer_name' in data:
                    st.session_state.customer_name = data.get('customer_name', '')
                if 'zip_code' in data:
                    st.session_state.zip_code = data.get('zip_code', '48201')
                if 'labor_hours' in data:
                    st.session_state.labor_hours = data.get('labor_hours', 0.0)
                if 'hourly_rate' in data:
                    st.session_state.hourly_rate = data.get('hourly_rate', 0.0)
                if 'materials' in data:
                    st.session_state.material_list = data.get('materials', [])
                    st.success(f"✅ Loaded complete job data: {len(data.get('materials', []))} items for {data.get('customer_name', 'customer')}")
                else:
                    st.session_state.material_list = data
                    st.success(f"✅ Loaded {len(data)} items from {uploaded_file.name}")
            st.rerun()
        elif uploaded_file.name.endswith('.csv'):
            # Load CSV
            df = pd.read_csv(uploaded_file)
            # Check if first row contains metadata
            if len(df) > 0 and str(df.iloc[0]['Item']).startswith('CUSTOMER:'):
                # Extract metadata from first row
                first_row = df.iloc[0]
                customer_data = str(first_row['Item']).replace('CUSTOMER: ', '')
                if customer_data != 'N/A':
                    st.session_state.customer_name = customer_data
                
                labor_hours_data = str(first_row['Qty']).replace('LABOR_HOURS: ', '')
                try:
                    st.session_state.labor_hours = float(labor_hours_data)
                except:
                    pass
                
                hourly_rate_data = str(first_row['Price']).replace('HOURLY_RATE: ', '')
                try:
                    st.session_state.hourly_rate = float(hourly_rate_data)
                except:
                    pass
                
                zip_data = str(first_row['Store']).replace('ZIP: ', '')
                if zip_data.isdigit() and len(zip_data) == 5:
                    st.session_state.zip_code = zip_data
                
                # Remove metadata row and load materials
                df = df.iloc[1:]
            
            # Ensure required columns exist for materials
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
                customer_msg = f" for {st.session_state.customer_name}" if st.session_state.customer_name else ""
                st.success(f"✅ Loaded {len(df)} items{customer_msg} from {uploaded_file.name}")
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
    💡 <strong>Tip:</strong> After searching for items below, come back here and enter the prices you find. 
    Check boxes to select items for deletion.
    </p>
    """, unsafe_allow_html=True)
    
    # Create columns to constrain table width
    col_spacer1, col_table, col_spacer2 = st.columns([0.5, 10, 0.5])
    
    with col_table:
        # Add checkboxes for selection
        if 'selected_items' not in st.session_state:
            st.session_state.selected_items = []
        
        df = pd.DataFrame(st.session_state.material_list)
        
        # Ensure all columns exist
        if 'Qty' not in df.columns:
            df['Qty'] = 1
        if 'Price' not in df.columns:
            df['Price'] = 0.0
        if 'Store' not in df.columns:
            df['Store'] = ""
        
        # Add selection column
        df.insert(0, 'Select', False)
        
        edited_df = st.data_editor(
            df, 
            use_container_width=True, 
            hide_index=True,
            height=180,
            disabled=["Added"],
            column_config={
                "Select": st.column_config.CheckboxColumn("☑️", width="small", default=False),
                "Item": st.column_config.TextColumn("Material Item", width="medium", required=True),
                "Qty": st.column_config.NumberColumn("Qty", width="small", min_value=1, default=1, step=1),
                "Price": st.column_config.NumberColumn("Price ($)", width="small", format="$%.2f", min_value=0, step=0.01),
                "Store": st.column_config.SelectboxColumn("Store", width="small", 
                    options=["", "Home Depot", "Lowe's", "Other"]),
                "Added": st.column_config.TextColumn("Date", width="small")
            },
            column_order=["Select", "Item", "Qty", "Price", "Store", "Added"]
        )
        
        # Update material list (remove Select column)
        temp_df = edited_df.drop(columns=['Select'])
        st.session_state.material_list = temp_df.to_dict('records')
        
        # Check if any items are selected
        selected_mask = edited_df['Select'] == True
        num_selected = selected_mask.sum()
        
        if num_selected > 0:
            col_del1, col_del2, col_del3 = st.columns([2, 1, 2])
            with col_del2:
                if st.button(f"🗑️ Delete ({num_selected}) Selected", type="primary", use_container_width=True):
                    # Keep only unselected items
                    st.session_state.material_list = edited_df[~selected_mask].drop(columns=['Select']).to_dict('records')
                    st.rerun()
    
    # Calculate and display total
    materials_total = calculate_total(st.session_state.material_list)
    labor_cost = calculate_labor_cost(st.session_state.labor_hours, st.session_state.hourly_rate)
    grand_total = materials_total + labor_cost
    
    if grand_total > 0:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                    padding: 2rem; border-radius: 12px; margin: 1rem 0;
                    border: 1px solid rgba(16, 185, 129, 0.5);
                    box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);">
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; text-align: center;">
                <div>
                    <h4 style="color: white; margin: 0; font-size: 1.2rem;">💰 Materials</h4>
                    <p style="color: white; margin: 0.5rem 0 0 0; font-size: 1.4rem; font-weight: bold;">${materials_total:,.2f}</p>
                </div>
                <div>
                    <h4 style="color: white; margin: 0; font-size: 1.2rem;">⏰ Labor</h4>
                    <p style="color: white; margin: 0.5rem 0 0 0; font-size: 1.4rem; font-weight: bold;">${labor_cost:,.2f}</p>
                </div>
                <div style="border-left: 2px solid rgba(255,255,255,0.3);">
                    <h4 style="color: white; margin: 0; font-size: 1.2rem;">🎯 TOTAL</h4>
                    <p style="color: white; margin: 0.5rem 0 0 0; font-size: 1.8rem; font-weight: bold;">${grand_total:,.2f}</p>
                </div>
            </div>
            <p style="color: rgba(255,255,255,0.9); margin: 1rem 0 0 0; text-align: center; font-size: 0.9rem;">
                {st.session_state.customer_name and f"Customer: {st.session_state.customer_name} • " or ""}Excludes tax & fees
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
        list_text = "=" * 60 + "\n"
        list_text += "VLF MATERIALS & LABOR ESTIMATE\n"
        list_text += "=" * 60 + "\n"
        list_text += f"Date: {date.today().strftime('%m/%d/%Y')}\n"
        if st.session_state.customer_name:
            list_text += f"Customer: {st.session_state.customer_name}\n"
        list_text += f"ZIP Code: {st.session_state.zip_code}\n"
        list_text += "=" * 60 + "\n\n"
        
        list_text += "MATERIALS:\n"
        list_text += "-" * 30 + "\n"
        materials_total = 0
        for idx, item in enumerate(st.session_state.material_list, 1):
            qty = item.get('Qty', 1)
            price = item.get('Price', 0)
            store = item.get('Store', '')
            item_total = float(qty) * float(price) if price else 0
            materials_total += item_total
            
            list_text += f"#{idx}. {item['Item']}\n"
            list_text += f"    Quantity: {qty}\n"
            list_text += f"    Price: ${price:.2f} each\n"
            if store:
                list_text += f"    Store: {store}\n"
            list_text += f"    Subtotal: ${item_total:.2f}\n"
            list_text += "\n"
        
        list_text += f"MATERIALS TOTAL: ${materials_total:,.2f}\n\n"
        
        # Add labor section
        labor_cost = calculate_labor_cost(st.session_state.labor_hours, st.session_state.hourly_rate)
        if labor_cost > 0:
            list_text += "LABOR:\n"
            list_text += "-" * 30 + "\n"
            list_text += f"Hours: {st.session_state.labor_hours}\n"
            list_text += f"Rate: ${st.session_state.hourly_rate:.2f}/hour\n"
            list_text += f"LABOR TOTAL: ${labor_cost:,.2f}\n\n"
        
        grand_total = materials_total + labor_cost
        list_text += "=" * 60 + "\n"
        list_text += f"GRAND TOTAL: ${grand_total:,.2f}\n"
        list_text += "=" * 60 + "\n"
        list_text += "\n(Excludes tax & fees)\n"
        
        filename = f"estimate_{st.session_state.customer_name.replace(' ', '_') if st.session_state.customer_name else 'materials'}_{date.today().strftime('%Y%m%d')}.txt"
        
        st.download_button("📋 Text List", list_text, 
                          filename, 
                          "text/plain", use_container_width=True)
    with col3:
        # Enhanced CSV with customer and labor data
        export_data = st.session_state.material_list.copy()
        if export_data:
            # Add metadata to first row
            metadata = {
                'Item': f"CUSTOMER: {st.session_state.customer_name or 'N/A'}",
                'Qty': f"LABOR_HOURS: {st.session_state.labor_hours}",
                'Price': f"HOURLY_RATE: {st.session_state.hourly_rate}",
                'Store': f"ZIP: {st.session_state.zip_code}",
                'Added': date.today().strftime('%m/%d/%Y')
            }
            export_data.insert(0, metadata)
        
        csv_data = pd.DataFrame(export_data).to_csv(index=False)
        filename_csv = f"estimate_{st.session_state.customer_name.replace(' ', '_') if st.session_state.customer_name else 'materials'}_{date.today().strftime('%Y%m%d')}.csv"
        st.download_button("📥 CSV Export", csv_data, 
                          filename_csv, 
                          "text/csv", use_container_width=True)
    with col4:
        # Enhanced JSON export with customer and labor data
        export_json = {
            'customer_name': st.session_state.customer_name,
            'zip_code': st.session_state.zip_code,
            'labor_hours': st.session_state.labor_hours,
            'hourly_rate': st.session_state.hourly_rate,
            'date_created': date.today().strftime('%m/%d/%Y'),
            'materials': st.session_state.material_list,
            'totals': {
                'materials_total': calculate_total(st.session_state.material_list),
                'labor_total': calculate_labor_cost(st.session_state.labor_hours, st.session_state.hourly_rate),
                'grand_total': calculate_total(st.session_state.material_list) + calculate_labor_cost(st.session_state.labor_hours, st.session_state.hourly_rate)
            }
        }
        json_data = json.dumps(export_json, indent=2)
        filename_json = f"estimate_{st.session_state.customer_name.replace(' ', '_') if st.session_state.customer_name else 'materials'}_{date.today().strftime('%Y%m%d')}.json"
        st.download_button("💾 JSON Export", json_data, 
                          filename_json,
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
    <p style="margin: 0.25rem 0;">⚙️ <strong style="color: #00D9FF;">Virtual Labor Force Detroit, MI</strong> | AI Solutions for Construction</p>
    <p style="margin: 0.25rem 0;">📧 Need help? Contact virtualadmin@virtuallaborforce.com</p>
    <p style="margin: 0.25rem 0;">📅 {date.today().strftime('%m/%d/%Y')}</p>
</div>
""", unsafe_allow_html=True)
