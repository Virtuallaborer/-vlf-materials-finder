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
    
    .stDateInput label {
        color: #00D9FF !important;
        font-weight: 600 !important;
    }
    
    .stDateInput input {
        background-color: rgba(30, 58, 95, 0.6) !important;
        border: 1px solid rgba(184, 106, 255, 0.3) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
    }
    
    .stDateInput input:focus {
        border-color: #B86AFF !important;
        box-shadow: 0 0 10px rgba(184, 106, 255, 0.3) !important;
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
        <h1>🔨 VLF Materials Finder & Calculator</h1>
        <p>Professional Tool for Construction Professionals</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<h3>🔒 Customer Access</h3>', unsafe_allow_html=True)
    st.markdown('<p>This is a premium tool for Virtual Labor Force clients ONLY!</p>', unsafe_allow_html=True)
    
    password_input = st.text_input("Enter Your Access Password:", type="password", key="login_pwd")
    
    if st.button("🔑 Login", type="primary", width="stretch"):
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
        <li>✅ Construction calculators (square footage, roofing, concrete)</li>
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
if 'company_name' not in st.session_state:
    st.session_state.company_name = ""
if 'company_address' not in st.session_state:
    st.session_state.company_address = ""
if 'customer_address' not in st.session_state:
    st.session_state.customer_address = ""
if 'customer_phone' not in st.session_state:
    st.session_state.customer_phone = ""
if 'start_date' not in st.session_state:
    st.session_state.start_date = date.today()
if 'end_date' not in st.session_state:
    st.session_state.end_date = date.today()
if 'job_type' not in st.session_state:
    st.session_state.job_type = "Residential"
if 'permits' not in st.session_state:
    st.session_state.permits = ""
if 'job_manager' not in st.session_state:
    st.session_state.job_manager = ""
if 'job_notes' not in st.session_state:
    st.session_state.job_notes = ""

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
        <h1>🔨 VLF Materials Finder & Calculator</h1>
        <p>Save Time on the Job Site | Built by Virtual Labor Force, Detroit</p>
    </div>
    """, unsafe_allow_html=True)
with col_head2:
    st.write("")
    st.write("")
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.rerun()

# ===== COMPANY INFORMATION SECTION =====
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown("### 🏢 Company Information")

col1, col2 = st.columns(2)
with col1:
    company_name = st.text_input(
        "Company Name", 
        value=st.session_state.company_name,
        placeholder="Your construction company name",
        help="The company performing this job"
    )
    if company_name != st.session_state.company_name:
        st.session_state.company_name = company_name

with col2:
    company_address = st.text_area(
        "Company Address", 
        value=st.session_state.company_address,
        placeholder="123 Main St, Detroit, MI 48201",
        height=100,
        help="Your company's business address"
    )
    if company_address != st.session_state.company_address:
        st.session_state.company_address = company_address

st.markdown('</div>', unsafe_allow_html=True)

# ===== CUSTOMER & JOB INFORMATION SECTION =====
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown("### 👤 Customer & Job Information")

# Customer details row
col1, col2 = st.columns(2)
with col1:
    customer_name = st.text_input(
        "Customer Name", 
        value=st.session_state.customer_name,
        placeholder="Enter customer name for this job"
    )
    if customer_name != st.session_state.customer_name:
        st.session_state.customer_name = customer_name

with col2:
    customer_phone = st.text_input(
        "Customer Phone", 
        value=st.session_state.customer_phone,
        placeholder="(555) 123-4567",
        help="Customer contact number"
    )
    if customer_phone != st.session_state.customer_phone:
        st.session_state.customer_phone = customer_phone

# Customer address and ZIP
col1, col2 = st.columns([3, 1])
with col1:
    customer_address = st.text_area(
        "Customer Address", 
        value=st.session_state.customer_address,
        placeholder="456 Oak Street, Detroit, MI 48201",
        height=100,
        help="Job site address"
    )
    if customer_address != st.session_state.customer_address:
        st.session_state.customer_address = customer_address

with col2:
    st.markdown("**ZIP Code**")
    subcol1, subcol2 = st.columns([2, 1])
    with subcol1:
        zip_input = st.text_input("ZIP Code", value=st.session_state.zip_code, 
                                  max_chars=5, label_visibility="collapsed",
                                  placeholder="ZIP", key="zip_input")
    with subcol2:
        if st.button("🔄 Update", width="stretch"):
            if zip_input.isdigit() and len(zip_input) == 5:
                st.session_state.zip_code = zip_input
                st.success(f"✓ Updated to {zip_input}")
            else:
                st.error("Invalid ZIP")

st.markdown('</div>', unsafe_allow_html=True)

# ===== JOB DETAILS SECTION =====
st.markdown('<div class="section-box-purple">', unsafe_allow_html=True)
st.markdown("### 📅 Job Details")

# Job dates and type
col1, col2, col3 = st.columns(3)
with col1:
    start_date = st.date_input(
        "Start Date",
        value=st.session_state.start_date,
        help="Project start date"
    )
    if start_date != st.session_state.start_date:
        st.session_state.start_date = start_date

with col2:
    end_date = st.date_input(
        "End Date",
        value=st.session_state.end_date,
        help="Expected completion date"
    )
    if end_date != st.session_state.end_date:
        st.session_state.end_date = end_date

with col3:
    job_type = st.selectbox(
        "Job Type",
        options=["Residential", "Commercial"],
        index=0 if st.session_state.job_type == "Residential" else 1,
        help="Type of construction project"
    )
    if job_type != st.session_state.job_type:
        st.session_state.job_type = job_type

# Job manager and permits
col1, col2 = st.columns(2)
with col1:
    job_manager = st.text_input(
        "Job Manager",
        value=st.session_state.job_manager,
        placeholder="Project manager or foreman",
        help="Person responsible for this job"
    )
    if job_manager != st.session_state.job_manager:
        st.session_state.job_manager = job_manager

with col2:
    permits = st.text_input(
        "Permits Required",
        value=st.session_state.permits,
        placeholder="Building permit, electrical, etc.",
        help="Required permits for this job"
    )
    if permits != st.session_state.permits:
        st.session_state.permits = permits

# Job notes
job_notes = st.text_area(
    "Job Notes",
    value=st.session_state.job_notes,
    placeholder="Special instructions, customer preferences, site conditions, etc.",
    height=120,
    help="Any additional information about this job"
)
if job_notes != st.session_state.job_notes:
    st.session_state.job_notes = job_notes

# Clear all fields button
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if st.button("🔄 Clear All Job Fields", type="secondary", width="stretch", help="Reset all fields to start a new job"):
        # Reset ALL session state variables to original defaults
        for key in list(st.session_state.keys()):
            if key != 'authenticated':  # Keep login state
                del st.session_state[key]
        
        # Re-initialize with defaults
        st.session_state.material_list = []
        st.session_state.zip_code = "48201"
        st.session_state.input_key = 0
        st.session_state.customer_name = ""
        st.session_state.labor_hours = 0.0
        st.session_state.hourly_rate = 0.0
        st.session_state.company_name = ""
        st.session_state.company_address = ""
        st.session_state.customer_address = ""
        st.session_state.customer_phone = ""
        st.session_state.start_date = date.today()
        st.session_state.end_date = date.today()
        st.session_state.job_type = "Residential"
        st.session_state.permits = ""
        st.session_state.job_manager = ""
        st.session_state.job_notes = ""
        
        st.success("✅ All fields completely cleared! Ready for new job.")
        st.rerun()

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
                # New format - full job data - load ALL fields
                field_mapping = {
                    'customer_name': 'customer_name',
                    'company_name': 'company_name', 
                    'company_address': 'company_address',
                    'customer_address': 'customer_address',
                    'customer_phone': 'customer_phone',
                    'zip_code': 'zip_code',
                    'job_type': 'job_type',
                    'permits': 'permits',
                    'job_manager': 'job_manager',
                    'job_notes': 'job_notes'
                }
                
                # Load string fields
                for json_key, session_key in field_mapping.items():
                    if json_key in data:
                        setattr(st.session_state, session_key, data.get(json_key, ''))
                
                # Load numeric fields with error handling
                if 'labor_hours' in data:
                    try:
                        st.session_state.labor_hours = float(data.get('labor_hours', 0.0))
                    except (ValueError, TypeError):
                        st.session_state.labor_hours = 0.0
                        
                if 'hourly_rate' in data:
                    try:
                        st.session_state.hourly_rate = float(data.get('hourly_rate', 0.0))
                    except (ValueError, TypeError):
                        st.session_state.hourly_rate = 0.0
                
                # Load date fields with multiple format support
                if 'start_date' in data:
                    try:
                        from datetime import datetime
                        date_str = data.get('start_date')
                        # Try multiple date formats
                        for fmt in ['%m/%d/%Y', '%Y-%m-%d', '%m-%d-%Y']:
                            try:
                                st.session_state.start_date = datetime.strptime(date_str, fmt).date()
                                break
                            except:
                                continue
                        else:
                            st.session_state.start_date = date.today()
                    except:
                        st.session_state.start_date = date.today()
                        
                if 'end_date' in data:
                    try:
                        from datetime import datetime
                        date_str = data.get('end_date')
                        # Try multiple date formats
                        for fmt in ['%m/%d/%Y', '%Y-%m-%d', '%m-%d-%Y']:
                            try:
                                st.session_state.end_date = datetime.strptime(date_str, fmt).date()
                                break
                            except:
                                continue
                        else:
                            st.session_state.end_date = date.today()
                    except:
                        st.session_state.end_date = date.today()
                
                # Load materials list
                if 'materials' in data:
                    materials = data.get('materials', [])
                    # Clean and validate materials data
                    cleaned_materials = []
                    for item in materials:
                        if isinstance(item, dict) and 'Item' in item:
                            # Clean up complex quoted strings that can break the data editor
                            item_name = str(item.get('Item', '')).strip()
                            # Remove problematic quotes and normalize
                            item_name = item_name.replace('\"', '"').replace("'", "'")
                            if item_name.startswith('"') and item_name.endswith('"'):
                                item_name = item_name[1:-1]
                            
                            cleaned_item = {
                                'Item': item_name,
                                'Qty': int(item.get('Qty', 1)) if isinstance(item.get('Qty'), (int, float)) else 1,
                                'Price': float(item.get('Price', 0.0)) if isinstance(item.get('Price'), (int, float)) else 0.0,
                                'Store': str(item.get('Store', '')),
                                'Added': str(item.get('Added', date.today().strftime('%m/%d/%Y')))
                            }
                            cleaned_materials.append(cleaned_item)
                    
                    st.session_state.material_list = cleaned_materials
                    
                    # Show success but DON'T immediately rerun to prevent loop
                    st.success(f"✅ Loaded complete job data: {len(cleaned_materials)} materials for {data.get('customer_name', data.get('company_name', 'customer'))}")
                    
                    # Set a flag to prevent immediate rerun loop
                    st.session_state.just_imported = True
                else:
                    # Fallback - try to treat entire dict as single material item
                    if 'Item' in data:
                        st.session_state.material_list = [data]
                        st.success(f"✅ Loaded 1 item from {uploaded_file.name}")
                    else:
                        st.session_state.material_list = []
                        st.success(f"✅ Loaded job information (no materials) from {uploaded_file.name}")
                        
                    st.session_state.just_imported = True
            
            # Only rerun if not in an import loop
            if not st.session_state.get('just_imported', False):
                # Force UI refresh with small delay
                import time
                time.sleep(0.1)
                st.rerun()
            else:
                # Clear the flag after successful import
                st.session_state.just_imported = False
            
        elif uploaded_file.name.endswith('.csv'):
            # Load CSV
            df = pd.read_csv(uploaded_file)
            
            # Handle multiple metadata rows (first 3 rows contain job info)
            if len(df) >= 3:
                try:
                    # Parse first metadata row
                    row1 = df.iloc[0]
                    company_name = str(row1['Item']).replace('COMPANY: ', '') if 'COMPANY:' in str(row1['Item']) else ''
                    if company_name and company_name != 'N/A':
                        st.session_state.company_name = company_name
                    
                    company_address = str(row1['Qty']).replace('COMPANY_ADDRESS: ', '') if 'COMPANY_ADDRESS:' in str(row1['Qty']) else ''
                    if company_address and company_address != 'N/A':
                        st.session_state.company_address = company_address
                    
                    customer_name = str(row1['Price']).replace('CUSTOMER: ', '') if 'CUSTOMER:' in str(row1['Price']) else ''
                    if customer_name and customer_name != 'N/A':
                        st.session_state.customer_name = customer_name
                    
                    customer_phone = str(row1['Store']).replace('CUSTOMER_PHONE: ', '') if 'CUSTOMER_PHONE:' in str(row1['Store']) else ''
                    if customer_phone and customer_phone != 'N/A':
                        st.session_state.customer_phone = customer_phone
                    
                    # Parse second metadata row
                    row2 = df.iloc[1]
                    customer_address = str(row2['Item']).replace('CUSTOMER_ADDRESS: ', '') if 'CUSTOMER_ADDRESS:' in str(row2['Item']) else ''
                    if customer_address and customer_address != 'N/A':
                        st.session_state.customer_address = customer_address
                    
                    zip_code = str(row2['Qty']).replace('ZIP: ', '') if 'ZIP:' in str(row2['Qty']) else ''
                    if zip_code and zip_code.isdigit() and len(zip_code) == 5:
                        st.session_state.zip_code = zip_code
                    
                    job_type = str(row2['Price']).replace('JOB_TYPE: ', '') if 'JOB_TYPE:' in str(row2['Price']) else ''
                    if job_type and job_type != 'N/A':
                        st.session_state.job_type = job_type
                    
                    job_manager = str(row2['Store']).replace('JOB_MANAGER: ', '') if 'JOB_MANAGER:' in str(row2['Store']) else ''
                    if job_manager and job_manager != 'N/A':
                        st.session_state.job_manager = job_manager
                    
                    permits = str(row2['Added']).replace('PERMITS: ', '') if 'PERMITS:' in str(row2['Added']) else ''
                    if permits and permits != 'N/A':
                        st.session_state.permits = permits
                    
                    # Parse third metadata row
                    row3 = df.iloc[2]
                    try:
                        start_date_str = str(row3['Item']).replace('START_DATE: ', '') if 'START_DATE:' in str(row3['Item']) else ''
                        if start_date_str and start_date_str != 'N/A':
                            from datetime import datetime
                            st.session_state.start_date = datetime.strptime(start_date_str, '%m/%d/%Y').date()
                    except:
                        pass
                    
                    try:
                        end_date_str = str(row3['Qty']).replace('END_DATE: ', '') if 'END_DATE:' in str(row3['Qty']) else ''
                        if end_date_str and end_date_str != 'N/A':
                            from datetime import datetime
                            st.session_state.end_date = datetime.strptime(end_date_str, '%m/%d/%Y').date()
                    except:
                        pass
                    
                    try:
                        labor_hours_str = str(row3['Price']).replace('LABOR_HOURS: ', '') if 'LABOR_HOURS:' in str(row3['Price']) else ''
                        if labor_hours_str and labor_hours_str != 'N/A':
                            st.session_state.labor_hours = float(labor_hours_str)
                    except:
                        pass
                    
                    try:
                        hourly_rate_str = str(row3['Store']).replace('HOURLY_RATE: ', '') if 'HOURLY_RATE:' in str(row3['Store']) else ''
                        if hourly_rate_str and hourly_rate_str != 'N/A':
                            st.session_state.hourly_rate = float(hourly_rate_str)
                    except:
                        pass
                    
                    job_notes = str(row3['Added']).replace('JOB_NOTES: ', '') if 'JOB_NOTES:' in str(row3['Added']) else ''
                    if job_notes and job_notes != 'N/A':
                        st.session_state.job_notes = job_notes
                    
                    # Remove metadata rows and load materials (rows 3+)
                    df = df.iloc[3:]
                    
                except Exception as e:
                    st.error(f"Error parsing CSV metadata: {str(e)}")
                    # Continue with materials loading even if metadata fails
            
            # Ensure required columns exist for materials
            if len(df) > 0 and 'Item' in df.columns:
                # Fill missing columns with defaults
                if 'Qty' not in df.columns:
                    df['Qty'] = 1
                if 'Price' not in df.columns:
                    df['Price'] = 0.0
                if 'Store' not in df.columns:
                    df['Store'] = ""
                if 'Added' not in df.columns:
                    df['Added'] = date.today().strftime("%m/%d/%Y")
                
                # Convert to proper types and clean data
                df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce').fillna(1).astype(int)
                df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0.0)
                df['Store'] = df['Store'].fillna('')
                df['Added'] = df['Added'].fillna(date.today().strftime("%m/%d/%Y"))
                
                # Clean problematic Item strings that can break data editor
                df['Item'] = df['Item'].astype(str).str.strip()
                df['Item'] = df['Item'].str.replace('\"', '"').str.replace('"', "'")
                
                st.session_state.material_list = df.to_dict('records')
                customer_msg = f" for {st.session_state.customer_name}" if st.session_state.customer_name else ""
                st.success(f"✅ Loaded complete job data: {len(df)} materials{customer_msg} from {uploaded_file.name}")
                
                # Set flag to prevent rerun loop
                st.session_state.just_imported = True
            else:
                st.warning("No material data found in CSV file")
                st.session_state.just_imported = True
                
            # Only rerun if not in an import loop
            if not st.session_state.get('just_imported', False):
                # Force UI refresh
                import time
                time.sleep(0.1)
                st.rerun()
            else:
                # Clear the flag after successful import
                st.session_state.just_imported = False
                
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        st.error("Please check file format and try again.")

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
    if st.button("➕ Add", type="primary", width="stretch"):
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

# ===== CONSTRUCTION CALCULATORS SECTION =====
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown("### 🧮 Construction Calculators")
st.markdown('<p style="color: #a0c4ff; font-size: 0.9rem; margin-bottom: 1rem;">Professional calculators to determine material quantities. Results can be added directly to your materials list.</p>', unsafe_allow_html=True)

# Calculator selection tabs
calc_tab1, calc_tab2, calc_tab3 = st.tabs(["📐 Square Footage", "🏠 Roofing Squares", "🧱 Material Quantities"])

with calc_tab1:
    st.markdown("#### 📐 Square Footage Calculator")
    st.markdown('<p style="color: #a0c4ff; font-size: 0.9rem;">Calculate total square footage for flooring, painting, or general area measurements.</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        length_ft = st.number_input("Length (feet)", min_value=0.0, value=0.0, step=0.5, key="sq_length")
    with col2:
        width_ft = st.number_input("Width (feet)", min_value=0.0, value=0.0, step=0.5, key="sq_width")
    with col3:
        if st.button("🧮 Calculate", key="calc_sqft"):
            if length_ft > 0 and width_ft > 0:
                total_sqft = length_ft * width_ft
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                            padding: 1.5rem; border-radius: 12px; margin: 1rem 0;
                            border: 1px solid rgba(16, 185, 129, 0.5); text-align: center;">
                    <h4 style="color: white; margin: 0;">📐 Total Square Footage</h4>
                    <p style="color: white; margin: 0.5rem 0 0 0; font-size: 1.8rem; font-weight: bold;">{total_sqft:,.1f} sq ft</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Auto-add to materials list option
                col_add1, col_add2, col_add3 = st.columns([1, 2, 1])
                with col_add2:
                    if st.button(f"➕ Add '{total_sqft:,.1f} sq ft coverage' to Materials", key="add_sqft"):
                        st.session_state.material_list.append({
                            "Item": f"Coverage needed: {total_sqft:,.1f} sq ft ({length_ft}' x {width_ft}')",
                            "Qty": 1,
                            "Price": 0.0,
                            "Store": "",
                            "Added": date.today().strftime("%m/%d/%Y")
                        })
                        st.success("✅ Added to materials list!")
                        st.rerun()
            else:
                st.warning("⚠️ Please enter both length and width")

with calc_tab2:
    st.markdown("#### 🏠 Roofing Squares Calculator")
    st.markdown('<p style="color: #a0c4ff; font-size: 0.9rem;">Calculate roofing squares (1 square = 100 sq ft) with waste factor.</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    with col1:
        roof_length = st.number_input("Roof Length (feet)", min_value=0.0, value=0.0, step=0.5, key="roof_length")
    with col2:
        roof_width = st.number_input("Roof Width (feet)", min_value=0.0, value=0.0, step=0.5, key="roof_width")
    with col3:
        waste_factor = st.selectbox("Waste Factor", [10, 15, 20, 25], index=1, key="waste_factor", 
                                   help="10% = simple roof, 15% = standard, 20% = complex, 25% = very complex")
    with col4:
        if st.button("🧮 Calculate", key="calc_roof"):
            if roof_length > 0 and roof_width > 0:
                base_sqft = roof_length * roof_width
                waste_sqft = base_sqft * (waste_factor / 100)
                total_sqft = base_sqft + waste_sqft
                roofing_squares = total_sqft / 100
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #B86AFF 0%, #7C3AFF 100%); 
                            padding: 1.5rem; border-radius: 12px; margin: 1rem 0;
                            border: 1px solid rgba(184, 106, 255, 0.5);">
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; text-align: center;">
                        <div>
                            <h5 style="color: white; margin: 0;">Base Area</h5>
                            <p style="color: white; margin: 0.25rem 0; font-size: 1.2rem; font-weight: bold;">{base_sqft:,.0f} sq ft</p>
                        </div>
                        <div>
                            <h5 style="color: white; margin: 0;">+ {waste_factor}% Waste</h5>
                            <p style="color: white; margin: 0.25rem 0; font-size: 1.2rem; font-weight: bold;">{waste_sqft:,.0f} sq ft</p>
                        </div>
                        <div style="border-left: 2px solid rgba(255,255,255,0.3);">
                            <h5 style="color: white; margin: 0;">🏠 Roofing Squares</h5>
                            <p style="color: white; margin: 0.25rem 0; font-size: 1.4rem; font-weight: bold;">{roofing_squares:.1f} squares</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Auto-add to materials list option
                col_add1, col_add2, col_add3 = st.columns([1, 2, 1])
                with col_add2:
                    if st.button(f"➕ Add '{roofing_squares:.1f} roofing squares' to Materials", key="add_roof"):
                        st.session_state.material_list.append({
                            "Item": f"Roofing material needed: {roofing_squares:.1f} squares ({total_sqft:,.0f} sq ft w/ {waste_factor}% waste)",
                            "Qty": 1,
                            "Price": 0.0,
                            "Store": "",
                            "Added": date.today().strftime("%m/%d/%Y")
                        })
                        st.success("✅ Added to materials list!")
                        st.rerun()
            else:
                st.warning("⚠️ Please enter roof dimensions")

with calc_tab3:
    st.markdown("#### 🧱 Material Quantity Calculator")
    st.markdown('<p style="color: #a0c4ff; font-size: 0.9rem;">Quick calculations for common construction materials.</p>', unsafe_allow_html=True)
    
    # Simple material calculators
    material_type = st.selectbox("Material Type", 
        ["Concrete (cubic yards)", "Gravel/Sand (cubic yards)", "Paint Coverage (gallons)", "Roofing Shingles (bundles)", "Tile/Flooring (pieces)"],
        key="material_type")
    
    if material_type == "Concrete (cubic yards)":
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
        with col1:
            concrete_length = st.number_input("Length (feet)", min_value=0.0, value=0.0, step=0.5, key="concrete_length")
        with col2:
            concrete_width = st.number_input("Width (feet)", min_value=0.0, value=0.0, step=0.5, key="concrete_width")
        with col3:
            concrete_depth = st.number_input("Depth (inches)", min_value=0.0, value=4.0, step=0.5, key="concrete_depth")
        with col4:
            if st.button("🧮 Calculate", key="calc_concrete"):
                if concrete_length > 0 and concrete_width > 0 and concrete_depth > 0:
                    cubic_feet = concrete_length * concrete_width * (concrete_depth / 12)
                    cubic_yards = cubic_feet / 27
                    
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #00f0ff 0%, #00c0cc 100%); 
                                padding: 1.5rem; border-radius: 12px; margin: 1rem 0;
                                border: 1px solid rgba(0, 240, 255, 0.5); text-align: center; color: black;">
                        <h4 style="margin: 0;">🧱 Concrete Needed</h4>
                        <p style="margin: 0.5rem 0 0 0; font-size: 1.8rem; font-weight: bold;">{cubic_yards:.2f} cubic yards</p>
                        <p style="margin: 0.25rem 0 0 0; font-size: 0.9rem;">({cubic_feet:.1f} cubic feet)</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Auto-add option
                    col_add1, col_add2, col_add3 = st.columns([1, 2, 1])
                    with col_add2:
                        if st.button(f"➕ Add '{cubic_yards:.2f} cubic yards concrete' to Materials", key="add_concrete"):
                            st.session_state.material_list.append({
                                "Item": f"Concrete: {cubic_yards:.2f} cubic yards ({concrete_length}' x {concrete_width}' x {concrete_depth}\")",
                                "Qty": 1,
                                "Price": 0.0,
                                "Store": "",
                                "Added": date.today().strftime("%m/%d/%Y")
                            })
                            st.success("✅ Added to materials list!")
                            st.rerun()
                else:
                    st.warning("⚠️ Please enter all dimensions")
    
    elif material_type == "Paint Coverage (gallons)":
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            paint_sqft = st.number_input("Total Square Feet", min_value=0.0, value=0.0, step=10.0, key="paint_sqft")
        with col2:
            coverage_per_gallon = st.number_input("Coverage per Gallon", min_value=200, value=400, step=25, key="coverage", 
                                                help="Typical: 300-450 sq ft per gallon. Premium paint = 400+ sq ft")
        with col3:
            coats = st.selectbox("Number of Coats", [1, 2, 3], index=1, key="coats")
        
        if st.button("🧮 Calculate", key="calc_paint"):
            if paint_sqft > 0:
                total_coverage_needed = paint_sqft * coats
                gallons_needed = total_coverage_needed / coverage_per_gallon
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                            padding: 1.5rem; border-radius: 12px; margin: 1rem 0;
                            border: 1px solid rgba(16, 185, 129, 0.5); text-align: center;">
                    <h4 style="color: white; margin: 0;">🎨 Paint Needed</h4>
                    <p style="color: white; margin: 0.5rem 0 0 0; font-size: 1.8rem; font-weight: bold;">{gallons_needed:.1f} gallons</p>
                    <p style="color: white; margin: 0.25rem 0 0 0; font-size: 0.9rem;">({paint_sqft:,.0f} sq ft × {coats} coats @ {coverage_per_gallon} sq ft/gal)</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Auto-add option
                col_add1, col_add2, col_add3 = st.columns([1, 2, 1])
                with col_add2:
                    if st.button(f"➕ Add '{gallons_needed:.1f} gallons paint' to Materials", key="add_paint"):
                        st.session_state.material_list.append({
                            "Item": f"Paint: {gallons_needed:.1f} gallons ({paint_sqft:,.0f} sq ft, {coats} coats @ {coverage_per_gallon}/gal)",
                            "Qty": 1,
                            "Price": 0.0,
                            "Store": "",
                            "Added": date.today().strftime("%m/%d/%Y")
                        })
                        st.success("✅ Added to materials list!")
                        st.rerun()
            else:
                st.warning("⚠️ Please enter square footage")
    
    elif material_type == "Roofing Shingles (bundles)":
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            shingle_sqft = st.number_input("Roof Square Feet", min_value=0.0, value=0.0, step=10.0, key="shingle_sqft")
        with col2:
            coverage_per_bundle = st.number_input("Coverage per Bundle", min_value=20, value=33, step=1, key="bundle_coverage", 
                                                help="Standard: 33.33 sq ft per bundle (1/3 of a roofing square)")
        with col3:
            waste_percent = st.selectbox("Waste Factor", [10, 15, 20], index=1, key="shingle_waste", 
                                       help="15% is standard for most roofs")
        
        if st.button("🧮 Calculate", key="calc_shingles"):
            if shingle_sqft > 0:
                # Add waste factor
                total_sqft_needed = shingle_sqft * (1 + waste_percent / 100)
                bundles_needed = total_sqft_needed / coverage_per_bundle
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #B86AFF 0%, #7C3AFF 100%); 
                            padding: 1.5rem; border-radius: 12px; margin: 1rem 0;
                            border: 1px solid rgba(184, 106, 255, 0.5); text-align: center;">
                    <h4 style="color: white; margin: 0;">🏠 Shingles Needed</h4>
                    <p style="color: white; margin: 0.5rem 0 0 0; font-size: 1.8rem; font-weight: bold;">{bundles_needed:.1f} bundles</p>
                    <p style="color: white; margin: 0.25rem 0 0 0; font-size: 0.9rem;">({shingle_sqft:,.0f} sq ft + {waste_percent}% waste @ {coverage_per_bundle} sq ft/bundle)</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Auto-add option
                col_add1, col_add2, col_add3 = st.columns([1, 2, 1])
                with col_add2:
                    if st.button(f"➕ Add '{bundles_needed:.1f} shingle bundles' to Materials", key="add_shingles"):
                        st.session_state.material_list.append({
                            "Item": f"Roofing shingles: {bundles_needed:.1f} bundles ({shingle_sqft:,.0f} sq ft + {waste_percent}% waste)",
                            "Qty": 1,
                            "Price": 0.0,
                            "Store": "",
                            "Added": date.today().strftime("%m/%d/%Y")
                        })
                        st.success("✅ Added to materials list!")
                        st.rerun()
            else:
                st.warning("⚠️ Please enter roof square footage")

st.markdown('</div>', unsafe_allow_html=True)

# ===== MATERIALS LIST SECTION =====
if st.session_state.material_list:
    # Safety check - ensure all materials have required fields
    safe_materials = []
    for item in st.session_state.material_list:
        if isinstance(item, dict):
            safe_item = {
                'Item': str(item.get('Item', 'Unknown Item')).strip()[:100],  # Limit length
                'Qty': max(1, int(item.get('Qty', 1))),  # Ensure positive quantity
                'Price': max(0.0, float(item.get('Price', 0.0))),  # Ensure non-negative price
                'Store': str(item.get('Store', ''))[:50],  # Limit store name length
                'Added': str(item.get('Added', date.today().strftime('%m/%d/%Y')))
            }
            safe_materials.append(safe_item)
    
    # Update with cleaned data
    if safe_materials != st.session_state.material_list:
        st.session_state.material_list = safe_materials
    
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
            width="stretch", 
            hide_index=True,
            height=180,
            disabled=["Added"],
            key="materials_editor",
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
                if st.button(f"🗑️ Delete ({num_selected}) Selected", type="primary", width="stretch"):
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
        if st.button("🗑️ Clear All", width="stretch"):
            st.session_state.material_list = []
            st.rerun()
    with col2:
        # Better formatted text export
        list_text = "=" * 60 + "\n"
        list_text += "VLF MATERIALS & LABOR ESTIMATE\n"
        list_text += "=" * 60 + "\n"
        list_text += f"Date: {date.today().strftime('%m/%d/%Y')}\n"
        
        if st.session_state.company_name:
            list_text += f"Company: {st.session_state.company_name}\n"
        if st.session_state.company_address:
            list_text += f"Company Address: {st.session_state.company_address}\n"
        
        if st.session_state.customer_name:
            list_text += f"Customer: {st.session_state.customer_name}\n"
        if st.session_state.customer_phone:
            list_text += f"Customer Phone: {st.session_state.customer_phone}\n"
        if st.session_state.customer_address:
            list_text += f"Job Site: {st.session_state.customer_address}\n"
        
        list_text += f"ZIP Code: {st.session_state.zip_code}\n"
        
        if st.session_state.job_manager:
            list_text += f"Job Manager: {st.session_state.job_manager}\n"
        if st.session_state.permits:
            list_text += f"Permits: {st.session_state.permits}\n"
        if st.session_state.job_notes:
            list_text += f"Job Notes: {st.session_state.job_notes}\n"
        
        list_text += f"Job Dates: {st.session_state.start_date.strftime('%m/%d/%Y')} to {st.session_state.end_date.strftime('%m/%d/%Y')}\n"
        list_text += f"Job Type: {st.session_state.job_type}\n"
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
                          "text/plain", width="stretch")
    with col3:
        # Enhanced CSV with customer and labor data
        export_data = st.session_state.material_list.copy()
        if export_data:
            # Add metadata to first few rows
            metadata_rows = [
                {
                    'Item': f"COMPANY: {st.session_state.company_name or 'N/A'}",
                    'Qty': f"COMPANY_ADDRESS: {st.session_state.company_address or 'N/A'}",
                    'Price': f"CUSTOMER: {st.session_state.customer_name or 'N/A'}",
                    'Store': f"CUSTOMER_PHONE: {st.session_state.customer_phone or 'N/A'}",
                    'Added': date.today().strftime('%m/%d/%Y')
                },
                {
                    'Item': f"CUSTOMER_ADDRESS: {st.session_state.customer_address or 'N/A'}",
                    'Qty': f"ZIP: {st.session_state.zip_code}",
                    'Price': f"JOB_TYPE: {st.session_state.job_type}",
                    'Store': f"JOB_MANAGER: {st.session_state.job_manager or 'N/A'}",
                    'Added': f"PERMITS: {st.session_state.permits or 'N/A'}"
                },
                {
                    'Item': f"START_DATE: {st.session_state.start_date.strftime('%m/%d/%Y')}",
                    'Qty': f"END_DATE: {st.session_state.end_date.strftime('%m/%d/%Y')}",
                    'Price': f"LABOR_HOURS: {st.session_state.labor_hours}",
                    'Store': f"HOURLY_RATE: {st.session_state.hourly_rate}",
                    'Added': f"JOB_NOTES: {st.session_state.job_notes or 'N/A'}"
                }
            ]
            # Insert metadata at the beginning
            for i, metadata in enumerate(metadata_rows):
                export_data.insert(i, metadata)
        
        csv_data = pd.DataFrame(export_data).to_csv(index=False)
        filename_csv = f"estimate_{st.session_state.customer_name.replace(' ', '_') if st.session_state.customer_name else 'materials'}_{date.today().strftime('%Y%m%d')}.csv"
        st.download_button("📥 CSV Export", csv_data, 
                          filename_csv, 
                          "text/csv", width="stretch")
    with col4:
        # Enhanced JSON export with customer and labor data
        export_json = {
            'company_name': st.session_state.company_name,
            'company_address': st.session_state.company_address,
            'customer_name': st.session_state.customer_name,
            'customer_address': st.session_state.customer_address,
            'customer_phone': st.session_state.customer_phone,
            'zip_code': st.session_state.zip_code,
            'start_date': st.session_state.start_date.strftime('%m/%d/%Y'),
            'end_date': st.session_state.end_date.strftime('%m/%d/%Y'),
            'job_type': st.session_state.job_type,
            'permits': st.session_state.permits,
            'job_manager': st.session_state.job_manager,
            'job_notes': st.session_state.job_notes,
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
                          "application/json", width="stretch")
    
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
        if st.button("🔍 Generate Search Links", type="primary", width="stretch"):
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
