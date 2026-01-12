import streamlit as st
import time
import json
import pandas as pd

# -----------------------------------------------------------------------------
# CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EDITT Insurance Demo",
    page_icon="🛡️",
    layout="centered"
)

# Custom CSS to hide default Streamlit elements for a cleaner pitch look
st.markdown("""
    <style>
    .main { padding-top: 2rem; }
    h1 { color: #2C3E50; }
    .stButton>button { width: 100%; border-radius: 5px; font-weight: bold; }
    .metric-container { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MOCK DATA & LOGIC
# -----------------------------------------------------------------------------

# Hardcoded Borrower Profiles
# Scores are raw inputs (0-100 scale) to feed the formula
BORROWERS = {
    "1001": {
        "name": "Tunde Bakare (Good)",
        "repayment": 95, "severity": 90, "discipline": 85, "identity": 100, "context": 90,
        "network_flag": False
    },
    "1002": {
        "name": "Chidinma Okoro (Neutral)",
        "repayment": 70, "severity": 60, "discipline": 65, "identity": 80, "context": 60,
        "network_flag": False
    },
    "1003": {
        "name": "Emeka Johnson (Bad)",
        "repayment": 20, "severity": 10, "discipline": 30, "identity": 40, "context": 20,
        "network_flag": True
    }
}

def calculate_insurability(b):
    """
    Formula:
    (0.35 * Repayment) + (0.20 * Severity) + (0.15 * Discipline) 
    + (0.15 * Identity) + (0.15 * Context)
    """
    score = (
        (0.35 * b['repayment']) +
        (0.20 * b['severity']) +
        (0.15 * b['discipline']) +
        (0.15 * b['identity']) +
        (0.15 * b['context'])
    )
    return round(score, 1)

def get_risk_assessment(score, network_flag):
    if network_flag:
        return "REJECTED", "Network Blacklist", 0.0, "red"
    
    if 80 <= score <= 100:
        return "APPROVED", "Low Risk", 2.5, "green"
    elif 60 <= score <= 79:
        return "APPROVED", "Medium Risk", 5.0, "orange"
    elif 40 <= score <= 59:
        return "RESTRICTED", "High Risk", 12.0, "orange"
    else:
        return "REJECTED", "Critical Risk", 0.0, "red"

# -----------------------------------------------------------------------------
# SIDEBAR (Presenter Context)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("🕵️ Presenter Guide")
    st.info("Use these IDs to demo different scenarios:")
    st.markdown("**1001**: Good Borrower (Low Premium)")
    st.markdown("**1002**: Neutral Borrower (High Premium)")
    st.markdown("**1003**: Strategic Defaulter (Blacklisted)")
    st.divider()
    st.caption("EDITT System v1.0.4")

# -----------------------------------------------------------------------------
# MAIN UI
# -----------------------------------------------------------------------------

# Header
st.title("🛡️ EDITT Insurance")
st.markdown("### Insuring good loans so lenders can lend with confidence.")
st.markdown("---")

# SECTION 1: LOAN EVALUATION
st.header("1. Loan Evaluation")

col1, col2, col3 = st.columns(3)
with col1:
    borrower_id = st.text_input("Borrower ID", value="1001", help="Enter 1001, 1002, or 1003")
with col2:
    loan_amount = st.number_input("Loan Amount (₦)", value=50000, step=5000)
with col3:
    tenure = st.selectbox("Tenure", ["15 Days", "30 Days", "60 Days"])

evaluate_btn = st.button("👉 Evaluate Loan Eligibility")

# State management to keep results visible
if 'evaluation_done' not in st.session_state:
    st.session_state['evaluation_done'] = False

if evaluate_btn:
    # 1. Loading Simulation
    with st.spinner('Checking Network History... Calculating Risk...'):
        time.sleep(1.2) # Cinematic delay
    
    # 2. Logic
    profile = BORROWERS.get(borrower_id)
    
    if not profile:
        st.error("Borrower not found in database.")
        st.session_state['evaluation_done'] = False
    else:
        score = calculate_insurability(profile)
        decision, band, premium_pct, color = get_risk_assessment(score, profile['network_flag'])
        
        # Save to state
        st.session_state['evaluation_done'] = True
        st.session_state['score'] = score
        st.session_state['decision'] = decision
        st.session_state['band'] = band
        st.session_state['premium_pct'] = premium_pct
        st.session_state['color'] = color
        st.session_state['flag'] = profile['network_flag']
        st.session_state['loan_amount'] = loan_amount

# Display Results if evaluated
if st.session_state['evaluation_done']:
    
    # Visual Header for Decision
    if st.session_state['decision'] == "APPROVED":
        st.success(f"✅ LOAN INSURABLE: {st.session_state['band']}")
    elif st.session_state['decision'] == "RESTRICTED":
        st.warning(f"⚠️ PARTIAL COVERAGE: {st.session_state['band']}")
    else:
        st.error(f"❌ LOAN REJECTED: {st.session_state['band']}")

    # Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Insurability Score", f"{st.session_state['score']}/100")
    m2.metric("Risk Band", st.session_state['band'])
    
    premium_amt = (st.session_state['premium_pct']/100) * st.session_state['loan_amount']
    m3.metric("Premium Rate", f"{st.session_state['premium_pct']}%")
    m4.metric("Premium Cost", f"₦{premium_amt:,.0f}")

    # Network Flag Alert
    if st.session_state['flag']:
        st.error("🚨 NETWORK ALERT: This identity is flagged for previous strategic default.")

    # JSON Payload (Hidden/Optional)
    with st.expander("View API Simulation (JSON)"):
        st.json({
            "status": "success",
            "borrower_id": borrower_id,
            "score": st.session_state['score'],
            "risk_band": st.session_state['band'],
            "approved": st.session_state['decision'] == "APPROVED",
            "premium_ngn": premium_amt
        })

    st.markdown("---")

    # SECTION 2: DEFAULT SIMULATION (Only if approved/restricted)
    if st.session_state['decision'] != "REJECTED":
        st.header("2. Default Protection Simulation")
        st.caption("Demonstrate what happens if this borrower fails to repay.")
        
        simulate_btn = st.button("👉 Simulate Default Event")
        
        if simulate_btn:
            with st.spinner('Processing Claim... Verifying Default...'):
                time.sleep(1.0)
            
            payout = st.session_state['loan_amount'] * 0.80
            lender_loss = st.session_state['loan_amount'] - payout
            
            st.success("✅ Default Verified. Claim Approved.")
            
            # Payout Visualization
            d1, d2 = st.columns(2)
            d1.metric("Insurance Payout (80%)", f"₦{payout:,.0f}", delta="Recovered Capital")
            d2.metric("Lender Net Loss", f"₦{lender_loss:,.0f}", delta_color="inverse", delta="-80% Loss Reduction")
            
            st.info(f"ℹ️ **Network Action:** Borrower {borrower_id} has been flagged across the EDITT ecosystem to prevent revolving debt.")

            with st.expander("View Default API Event"):
                st.json({
                    "event": "loan_default",
                    "claim_status": "approved",
                    "payout_amount": payout,
                    "borrower_action": "flagged_global"
                })

# SECTION 3: NETWORK SUMMARY (Always Visible)
st.markdown("---")
st.header("3. Ecosystem Impact")

impact_data = {
    "Metric": ["Lender Default Loss", "Recovery Time", "Fraud Detection"],
    "Without EDITT": ["100% of Principal", "90+ Days", "Siloed Data"],
    "With EDITT": ["20% of Principal", "48 Hours", "Shared Network Intelligence"]
}
st.table(pd.DataFrame(impact_data))
