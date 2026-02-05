import streamlit as st
import random
import pandas as pd

# CONFIGURATION & MY STYLING
st.set_page_config(page_title="Visa Sentinel", page_icon="🛡️", layout="wide")

# Putting Dark Theme looks good with me
st.markdown("""
<style>
    /* Force dark theme adjustments */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    /* Style the sidebar */
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }
    /* Success/Error/Warning box styling */
    .stAlert {
        border-radius: 8px;
    }
    /* Custom headers */
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions which i consider the brain of this app.

def luhn_check(card_num):
    """Returns True if valid, False if invalid, and the sum."""
    digits = [int(d) for d in str(card_num)]
    check_digit = digits.pop()
    digits.reverse()
    doubled_digits = []
    
    for i, d in enumerate(digits):
        if i % 2 == 0:
            val = d * 2
            if val > 9: val -= 9
            doubled_digits.append(val)
        else:
            doubled_digits.append(d)
            
    total_sum = sum(doubled_digits) + check_digit
    return (total_sum % 10 == 0), total_sum, doubled_digits

def generate_fake_visa():
    """Generates a 16-digit number that starts with 4 and passes Luhn."""
    prefix = "4"
    # To generage 14 random digits
    middle = "".join([str(random.randint(0, 9)) for _ in range(14)])
    temp_card = prefix + middle
    
    # Calculating required checksum and finding a digit that makes it valid 
    
    for i in range(10):
        full_card = temp_card + str(i)
        is_valid, _, _ = luhn_check(full_card)
        if is_valid:
            return full_card
    return None

# app layout starts here

# Top Navigation Bar
st.sidebar.title("🛡️ Visa Sentinel")
st.sidebar.caption("FinTech Security Suite v1.0")
mode = st.sidebar.radio("Select Module:", 
    ["1. Algorithm Validator", 
     "2. Limitation Demo (Hacker Mode)", 
     "3. Advanced Security Suite"])

st.sidebar.markdown("---")
st.sidebar.info("Designed for: **Fraud Detection Assignment**")


# MODULE 1: THE VALIDATOR (Matches Top-Left Image)

if mode == "1. Algorithm Validator":
    st.title("🛡️ Visa Sentinel Validator")
    st.write("Analyze card structure and mathematical integrity.")
    
    # Input
    card_input = st.text_input("Enter Visa Card Number for Inspection:", max_chars=19)
    
    if card_input:
        # Clean input (remove spaces)
        clean_num = card_input.replace(" ", "").replace("-", "")
        
        if not clean_num.isdigit():
            st.error("⚠️ Error: Input must contain numbers only.")
        else:
            # 1. Prefix Check
            col1, col2, col3 = st.columns(3)
            is_visa = clean_num.startswith("4")
            if is_visa:
                col1.success("✅ Prefix: Starts with 4")
            else:
                col1.error("❌ Prefix: Not Visa")
            
            # 2. Length Check
            is_len = len(clean_num) in [13, 16, 19]
            if is_len:
                col2.success(f"✅ Length: {len(clean_num)} digits")
            else:
                col2.error(f"❌ Length: {len(clean_num)} (Invalid)")
            
            # 3. Luhn Check (The Math)
            is_valid, total_sum, processed_digits = luhn_check(clean_num)
            
            if is_valid:
                st.success(f"✅ Structural Validity: PASSED (Luhn Sum: {total_sum})")
                st.metric(label="Validation Status", value="VALID", delta="Verified")
            else:
                st.error(f"❌ Structural Validity: FAILED (Luhn Sum: {total_sum})")
                st.metric(label="Validation Status", value="INVALID", delta="- Rejected", delta_color="inverse")

            # 4. The Visualizer (Showing the Math)
            with st.expander("Show Mathematical Calculation Details"):
                st.write("Breakdown of the Luhn Algorithm processing:")
                # Create a simple visual representation
                digits_list = [d for d in clean_num]
                df = pd.DataFrame([digits_list], columns=[f"D{i+1}" for i in range(len(digits_list))])
                st.dataframe(df, hide_index=True)
                st.caption("Each digit is processed (doubled/subtracted) and summed to check divisibility by 10.")


# MODULE 2: LIMITATIONS / HACKER MODE (Matches Top-Right Image)

elif mode == "2. Limitation Demo (Hacker Mode)":
    st.title("⚠️ Limitation Demonstration")
    
    st.markdown("""
    <div style="background-color: #721c24; padding: 20px; border-radius: 10px; border: 1px solid #f5c6cb;">
        <h3 style="color: #f8d7da; margin:0;">WARNING: SYSTEM VULNERABILITY DETECTED</h3>
        <p style="color: #f8d7da;">The Luhn Algorithm only checks <b>syntax</b>, not <b>authenticity</b>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("Simulate 'Ghost' Card Generation")
    st.write("Click below to generate a card number that passes ALL structural tests but is completely fake.")
    
    if st.button("Generate FAKE but VALID Card", type="primary"):
        fake_card = generate_fake_visa()
        
        # Display large card number
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background-color: #222; border-radius: 10px; margin: 20px 0;">
            <h1 style="font-family: monospace; color: #00ff00; letter-spacing: 5px;">
                {' '.join([fake_card[i:i+4] for i in range(0, len(fake_card), 4)])}
            </h1>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        col1.warning(f"Luhn Check: ✅ PASSED")
        col2.warning(f"Bank Database: ❌ NOT FOUND")
        
        st.info("Explanation: This number satisfies the math formula (Sum % 10 == 0), proving that algorithmic validity does not equal financial existence.")


# MODULE 3: SECURITY SUITE (Matches Bottom Image)

elif mode == "3. Advanced Security Suite":
    st.title("🛡️ Advanced Security Layer")
    st.write("Proposed solution to fix the limitations shown in Part 2.")
    
    col_tech, col_org = st.columns(2)
    
    # Technical Layers Panel
    with col_tech:
        st.subheader("Technical Layers")
        with st.container(border=True):
            st.toggle("Geolocation Match (IP vs GPS)", value=True)
            st.toggle("Velocity Check (Trans/min)", value=True)
            st.toggle("Device Fingerprinting", value=False)
            st.toggle("Behavioral Biometrics", value=True)
            st.caption("These checks happen in milliseconds during the transaction.")

    # Organizational Layers Panel
    with col_org:
        st.subheader("Organizational Layers")
        with st.container(border=True):
            st.checkbox("KYC (Know Your Customer) Review", value=True)
            st.checkbox("Manual Review for >$10k", value=True)
            st.checkbox("3D Secure (OTP) Enforcement", value=False)
            st.caption("These checks involve policy and human oversight.")

    # System Status Footer
    st.write("---")
    status_col, _ = st.columns([3,1])
    status_col.success("System Status: SECURE - Multi-Layer Protection Active")