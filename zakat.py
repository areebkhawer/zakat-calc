import streamlit as st
import yfinance as yf
import pandas as pd

# --- 1. PAGE CONFIG & STYLING ---
st.set_page_config(page_title="Zakat Pro-FinTech", page_icon="🌙", layout="centered")

# Custom CSS for the "Areeb Khawer" Footer
st.markdown("""
    <style>
    .main-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: #6c757d;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #e9ecef;
        z-index: 100;
    }
    </style>
    <div class="main-footer">Developed by <b>Areeb Khawer</b> | InvestPro Pakistan</div>
    """, unsafe_allow_html=True)

# --- 2. LIVE MARKET DATA FETCHING ---
@st.cache_data(ttl=3600)  # Updates prices once every hour
def fetch_market_rates():
    # Get USD to PKR Exchange Rate
    ex_rate = yf.Ticker("PKR=X").history(period="1d")['Close'].iloc[-1]
    
    # Get Gold (GC=F) and Silver (SI=F) Prices per ounce in USD
    gold_oz_usd = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
    silver_oz_usd = yf.Ticker("SI=F").history(period="1d")['Close'].iloc[-1]
    
    # Convert to PKR per Gram (1 Ounce = 31.1035 Grams)
    gold_pkr_gram = (gold_oz_usd / 31.1035) * ex_rate
    silver_pkr_gram = (silver_oz_usd / 31.1035) * ex_rate
    
    return ex_rate, gold_pkr_gram, silver_pkr_gram

# Load data with error handling
try:
    pkr_rate, gold_pkr, silver_pkr = fetch_market_rates()
    # Sharia Thresholds (Nisab)
    gold_nisab_pkr = gold_pkr * 87.48   # 87.48g Gold
    silver_nisab_pkr = silver_pkr * 612.36 # 612.36g Silver
except:
    st.error
