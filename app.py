import streamlit as st
from market_dashboard import run_market_dashboard
from coin_dashboard import run_coin_dashboard

st.set_page_config(
    page_title="Crypto Analytics Platform",
    layout="wide"
)

st.sidebar.title("🧭 Navigation")

page = st.sidebar.radio(
    "Go to",
    ["📊 Market Dashboard", "🪙 Coin Dashboard"]
)

if page == "📊 Market Dashboard":
    run_market_dashboard()

elif page == "🪙 Coin Dashboard":
    run_coin_dashboard()
