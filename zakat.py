import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Zakat Pro-FinTech", page_icon="🌙")

# --- CUSTOM CSS FOR THE "AREEB KHAWER" SIGNATURE ---
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: grey;
        text-align: center;
        padding: 10px;
        font-size: 12px;
    }
    </style>
    <div class="footer">Developed by Areeb Khawer</div>
    """, unsafe_allow_html=True)

 1. User selects the unit
unit = st.sidebar.radio("Select Gold Unit:", ["Grams", "KG"])

# 2. User inputs the weight
weight_input = st.sidebar.number_input(f"Enter Gold Weight in {unit}", min_value=0.0, step=0.1)

# 3. Logic to convert to grams for the calculation
if unit == "KG":
    gold_weight = weight_input * 1000  # Convert KG to Grams
else:
    gold_weight = weight_input
st.title("🌙 Zakat & Wealth Intelligence (PKR)")
st.write("Live market-linked Zakat calculator for the Pakistani financial landscape.")

# 1. FETCH LIVE DATA (GOLD & EXCHANGE RATE)
@st.cache_data(ttl=3600) # Updates every hour
def get_live_market_data():
    # Get USD/PKR Exchange Rate
    ex_rate = yf.Ticker("PKR=X").history(period="1d")['Close'].iloc[-1]
    
    # Get Gold price per gram in USD
    gold_usd_oz = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
    gold_pkr_gram = (gold_usd_oz / 31.1035) * ex_rate
    
    return ex_rate, gold_pkr_gram





try:
    pkr_rate, gold_pkr = get_live_market_data()
    nisab_pkr = gold_pkr * 87.48 # Nisab threshold (87.48g of gold)
except:
    st.error("Market data currently unavailable. Using estimates.")
    pkr_rate, gold_pkr, nisab_pkr = 280.0, 22000.0, 1900000.0

# 2. MARKET METRICS
col1, col2 = st.columns(2)
col1.metric("USD / PKR", f"Rs. {pkr_rate:.2f}")
col2.metric("Gold Price (1g)", f"Rs. {gold_pkr:,.0f}")

# 3. USER INPUTS
st.subheader("Asset Declaration")
cash = st.number_input("Total Cash (Bank + Hand)", min_value=0.0, step=1000.0)
gold_weight = st.number_input("Gold Weight in Grams", min_value=0.0, step=1.0)
investments = st.number_input("Stocks / Crypto / Business Assets", min_value=0.0, step=1000.0)

# 4. CALCULATION LOGIC
total_wealth = cash + (gold_weight * gold_pkr) + investments

st.divider()

if total_wealth >= nisab_pkr:
    zakat_payable = total_wealth * 0.025
    st.success(f"### Your Wealth: Rs. {total_wealth:,.2f}")
    st.info(f"*Nisab Threshold:* Rs. {nisab_pkr:,.2f}")
    st.header(f"Zakat Due: Rs. {zakat_payable:,.2f}")
    
    # Visual Breakdown
    data = {
        "Category": ["Cash", "Gold Value", "Investments"],
        "Amount": [cash, (gold_weight * gold_pkr), investments]
    }
    df = pd.DataFrame(data)
    st.bar_chart(df.set_index("Category"))
else:
    st.warning(f"Your wealth (Rs. {total_wealth:,.2f}) is below the Nisab (Rs. {nisab_pkr:,.2f}). No Zakat is due.")

st.sidebar.markdown("### About this Tool")
st.sidebar.write("This FinTech application uses real-time market data from Yahoo Finance to calculate Zakat accurately based on the current value of Gold in Pakistan.")

