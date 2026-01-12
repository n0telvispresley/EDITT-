import streamlit as st
import time
import pandas as pd

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EDITT | Default Protection",
    page_icon="🛡️",
    layout="centered"
)

# -----------------------------------------------------------------------------
# 2. CUSTOM CSS (Dark Mode Proof & Beautified)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Global Settings - Force Light Theme for Consistency */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #f8f9fa; 
        color: #1f2937; /* Force dark text generally */
    }

    /* Remove top padding for a cleaner header */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    /* HEADER STYLES */
    h1 {
        color: #111827 !important;
        font-weight: 700;
        letter-spacing: -0.025em;
    }
    
    h2 {
        color: #374151 !important;
        font-weight: 600;
        font-size: 1.25rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    p, li, label {
        color: #374151 !important;
    }

    /* CARD DESIGN SYSTEM */
    .st-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #e5e7eb;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        text-align: center;
        height: 100%;
    }
    
    .st-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    .st-card-title {
        color: #6b7280 !important;
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }

    .st-card-value {
        color: #111827; 
        font-size: 2rem;
        font-weight: 700;
    }

    .st-card-subtitle {
        color: #9ca3af !important;
        font-size: 0.875rem;
        margin-top: 4px;
    }

    /* Dynamic Colors */
    .text-green { color: #059669 !important; }
    .text-orange { color: #d97706 !important; }
    .text-red { color: #dc2626 !important; }
    .text-blue { color: #2563eb !important; }

    /* Button Styling - STRICT WHITE TEXT ENFORCEMENT */
    .stButton > button {
        background-color: #2563eb;
        color: #ffffff !important; /* Force White Text */
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        width: 100%;
        transition: background-color 0.2s;
    }
    
    .stButton > button p {
        color: #ffffff !important; 
    }

    .stButton > button:hover {
        background-color: #1d4ed8;
        color: #ffffff !important;
    }

    /* Alert Boxes */
    .success-box {
        background-color: #ecfdf5;
        border-left: 5px solid #059669;
        padding: 1rem;
        border-radius: 4px;
        color: #065f46 !important;
        margin-bottom: 1rem;
    }
    .warning-box {
        background-color: #fffbeb;
        border-left: 5px solid #d97706;
        padding: 1rem;
        border-radius: 4px;
        color: #92400e !important;
        margin-bottom: 1rem;
    }
    .error-box {
        background-color: #fef2f2;
        border-left: 5px solid #dc2626;
        padding: 1rem;
        border-radius: 4px;
        color: #991b1b !important;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. MOCK DATA & LOGIC
# -----------------------------------------------------------------------------
BORROWERS = {
    "1001": { "name": "Tunde Bakare", "repayment": 95, "severity": 90, "discipline": 85, "identity": 100, "context": 90, "network_flag": False },
    "1002": { "name": "Chidinma Okoro", "repayment": 70, "severity": 60, "discipline": 65, "identity": 80, "context": 60, "network_flag": False },
    "1003": { "name": "Emeka Johnson", "repayment": 20, "severity": 10, "discipline": 30, "identity": 40, "context": 20, "network_flag": True }
}

def calculate_insurability(b):
    return round((0.35 * b['repayment']) + (0.20 * b['severity']) + (0.15 * b['discipline']) + (0.15 * b['identity']) + (0.15 * b['context']), 1)

def get_risk_assessment(score, network_flag):
    if network_flag:
        return "REJECTED", "Network Blacklist", 0.0, "text-red"
    if 80 <= score <= 100:
        return "APPROVED", "Low Risk", 2.5, "text-green"
    elif 60 <= score <= 79:
        return "APPROVED", "Medium Risk", 5.0, "text-orange"
    elif 40 <= score <= 59:
        return "RESTRICTED", "High Risk", 12.0, "text-orange"
    else:
        return "REJECTED", "Critical Risk", 0.0, "text-red"

# -----------------------------------------------------------------------------
# 4. SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2454/2454269.png", width=50) 
    st.title("Admin Controls")
    st.markdown("**Demo IDs:**")
    st.code("1001")
    st.caption("Good Borrower (Low Rate)")
    st.code("1002")
    st.caption("Neutral (High Rate)")
    st.code("1003")
    st.caption("Fraudster (Blacklisted)")
    st.divider()
    st.caption("EDITT System v2.0")

# -----------------------------------------------------------------------------
# 5. MAIN UI
# -----------------------------------------------------------------------------

# Hero Section
st.title("🛡️ EDITT Insurance")
st.markdown("""
<div style='background-color: #eff6ff; padding: 15px; border-radius: 10px; border: 1px solid #dbeafe; color: #1e40af;'>
    <strong>Value Proposition:</strong> We insure qualified B2B loans so lenders can scale with confidence.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------------------
# SECTION 1: EVALUATION
# ---------------------------
st.header("1. Loan Underwriting")

c1, c2, c3 = st.columns(3)
with c1:
    borrower_id = st.text_input("Borrower ID", value="1001")
with c2:
    loan_amount = st.number_input("Principal (₦)", value=50000, step=5000)
with c3:
    tenure = st.selectbox("Tenure", ["15 Days", "30 Days", "60 Days"])

if st.button("👉 Analyze Risk & Eligibility"):
    # Spinner
    with st.spinner('Querying Network Database...'):
        time.sleep(1.0)
    
    profile = BORROWERS.get(borrower_id)
    
    if not profile:
        st.error("ID not found.")
    else:
        score = calculate_insurability(profile)
        decision, band, premium_pct, color_class = get_risk_assessment(score, profile['network_flag'])
        
        # Save to session state
        st.session_state.update({
            'run': True, 'score': score, 'decision': decision,
            'band': band, 'premium_pct': premium_pct,
            'color': color_class, 'flag': profile['network_flag'],
            'amt': loan_amount, 'bid': borrower_id
        })

# Display Results
if st.session_state.get('run'):
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Status Banner
    decision = st.session_state['decision']
    band = st.session_state['band']
    
    if decision == "APPROVED":
        st.markdown(f'<div class="success-box">✅ <strong>APPROVED:</strong> This loan is eligible for Default Protection ({band}).</div>', unsafe_allow_html=True)
    elif decision == "RESTRICTED":
        st.markdown(f'<div class="warning-box">⚠️ <strong>RESTRICTED:</strong> Partial coverage only ({band}).</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="error-box">⛔ <strong>REJECTED:</strong> {band}. Do not lend.</div>', unsafe_allow_html=True)

    # CARD LAYOUT
    col1, col2, col3 = st.columns(3)
    
    # Card 1: Score
    with col1:
        st.markdown(f"""
        <div class="st-card">
            <div class="st-card-title">Insurability Score</div>
            <div class="st-card-value {st.session_state['color']}">{st.session_state['score']}</div>
            <div class="st-card-subtitle">Out of 100</div>
        </div>
        """, unsafe_allow_html=True)
        
    # Card 2: Premium
    premium_amt = (st.session_state['premium_pct']/100) * st.session_state['amt']
    with col2:
        st.markdown(f"""
        <div class="st-card">
            <div class="st-card-title">Insurance Premium</div>
            <div class="st-card-value">₦{premium_amt:,.0f}</div>
            <div class="st-card-subtitle">Rate: {st.session_state['premium_pct']}%</div>
        </div>
        """, unsafe_allow_html=True)

    # Card 3: Coverage Cap
    coverage = st.session_state['amt'] * 0.80 if decision != "REJECTED" else 0
    with col3:
        st.markdown(f"""
        <div class="st-card">
            <div class="st-card-title">Max Coverage</div>
            <div class="st-card-value text-blue">₦{coverage:,.0f}</div>
            <div class="st-card-subtitle">80% of Principal</div>
        </div>
        """, unsafe_allow_html=True)

    # Network Flag Warning
    if st.session_state['flag']:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background-color: #fee2e2; padding: 15px; border-radius: 10px; border: 1px solid #fca5a5; color: #991b1b; display: flex; align-items: center;">
            <span style="font-size: 20px; margin-right: 10px;">🚨</span>
            <div>
                <strong>NETWORK MATCH FOUND:</strong> This identity is linked to a previous strategic default in the EDITT ecosystem.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # API SIMULATION
    with st.expander("🔌 View API Simulation (JSON)"):
        st.json({
            "status": "success",
            "borrower_id": st.session_state['bid'],
            "score": st.session_state['score'],
            "risk_band": st.session_state['band'],
            "decision": st.session_state['decision'],
            "premium_ngn": premium_amt
        })

    # ---------------------------
    # SECTION 2: DEFAULT SIMULATION
    # ---------------------------
    if decision != "REJECTED":
        st.markdown("---")
        st.header("2. Default Protection Event")
        st.info("Demonstration: Click below to simulate if this borrower fails to repay.")
        
        if st.button("👉 Simulate Borrower Default"):
            with st.spinner('Processing Claim...'):
                time.sleep(1.5)
            
            payout = st.session_state['amt'] * 0.80
            loss_without = st.session_state['amt']
            loss_with = st.session_state['amt'] - payout
            
            st.markdown(f'<div class="success-box">✅ <strong>CLAIM APPROVED:</strong> Payout processed instantly.</div>', unsafe_allow_html=True)
            
            # Comparison Cards
            d1, d2 = st.columns(2)
            
            with d1:
                st.markdown(f"""
                <div class="st-card" style="border: 2px solid #f87171;">
                    <div class="st-card-title">Loss WITHOUT Editt</div>
                    <div class="st-card-value text-red" style="text-decoration: line-through;">-₦{loss_without:,.0f}</div>
                    <div class="st-card-subtitle">100% Capital Lost</div>
                </div>
                """, unsafe_allow_html=True)
                
            with d2:
                st.markdown(f"""
                <div class="st-card" style="border: 2px solid #34d399; background-color: #ecfdf5;">
                    <div class="st-card-title">Loss WITH Editt</div>
                    <div class="st-card-value text-green">-₦{loss_with:,.0f}</div>
                    <div class="st-card-subtitle">Only 20% Risk Exposure</div>
                </div>
                """, unsafe_allow_html=True)
                
            # API SIMULATION DEFAULT
            with st.expander("🔌 View Webhook Payload (JSON)"):
                st.json({
                    "event": "loan_default",
                    "claim_id": "CLM-99283",
                    "payout_amount": payout,
                    "borrower_action": "flagged_global",
                    "network_update": "blacklisted"
                })

# ---------------------------
# SECTION 3: ECOSYSTEM
# ---------------------------
st.markdown("---")
st.header("3. Network Impact")

# CHANGED: Header Background is now Light Blue (#dbeafe), Text is Dark Blue (#1e3a8a)
impact_html = """
<div style="overflow-x: auto;">
  <table style="width:100%; border-collapse: collapse; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <tr style="background-color: #dbeafe; border-bottom: 2px solid #2563eb; text-align: left;">
      <th style="padding: 12px 15px; color: #1e3a8a !important; font-weight: bold;">Metric</th>
      <th style="padding: 12px 15px; color: #1e3a8a !important; font-weight: bold;">Without EDITT</th>
      <th style="padding: 12px 15px; color: #1e3a8a !important; font-weight: bold;">With EDITT</th>
    </tr>
    <tr style="background-color: white; border-bottom: 1px solid #e5e7eb;">
      <td style="padding: 12px 15px; font-weight: bold; color: #1f2937;">Lender Loss on Default</td>
      <td style="padding: 12px 15px; color: #dc2626; font-weight: bold;">100% of Principal</td>
      <td style="padding: 12px 15px; color: #059669; font-weight: bold;">20% of Principal</td>
    </tr>
    <tr style="background-color: #f9fafb; border-bottom: 1px solid #e5e7eb;">
      <td style="padding: 12px 15px; font-weight: bold; color: #1f2937;">Recovery Speed</td>
      <td style="padding: 12px 15px; color: #1f2937;">90+ Days</td>
      <td style="padding: 12px 15px; color: #2563eb; font-weight: bold;">48 Hours</td>
    </tr>
    <tr style="background-color: white;">
      <td style="padding: 12px 15px; font-weight: bold; color: #1f2937;">Fraud Prevention</td>
      <td style="padding: 12px 15px; color: #1f2937;">Internal Data Only</td>
      <td style="padding: 12px 15px; font-weight: bold; color: #1f2937;">Shared Network Blacklist</td>
    </tr>
  </table>
</div>
"""
st.markdown(impact_html, unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)
