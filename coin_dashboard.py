def run_coin_dashboard():
    # ------------------------------------------
    # Coin Analysis Dashboard (INR)
    # Deep dive analysis for a selected cryptocurrency
    # ------------------------------------------

    import streamlit as st
    import pandas as pd
    import numpy as np
    import requests
    import plotly.express as px
    import datetime as dt
    # -----------------------------
    # PAGE CONFIG
    # -----------------------------
    st.set_page_config(
        page_title="Coin Analysis Dashboard",
        page_icon="🔍",
        layout="wide"
    )

    # -----------------------------
    # API CONFIG (CoinMarketCap)
    # -----------------------------
    CMC_API_KEY = "9181d58fd8e44fda883b320bb6be1a2c"

    API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    HEADERS = {
        "X-CMC_PRO_API_KEY": CMC_API_KEY,
        "Accept": "application/json"
    }

    PARAMS = {
        "start": "1",
        "limit": "50",
        "convert": "INR"
    }

    # -----------------------------
    # LOAD MARKET DATA
    # -----------------------------
    @st.cache_data(ttl=300)
    def load_data():
        response = requests.get(API_URL, headers=HEADERS, params=PARAMS, timeout=10)
        response.raise_for_status()
        data = response.json()["data"]

        rows = []
        for coin in data:
            q = coin["quote"]["INR"]
            rows.append({
                "coin": coin["name"],
                "symbol": coin["symbol"],
                "price": q["price"],
                "market_cap": q["market_cap"],
                "volume": q["volume_24h"],
                "change_24h": q["percent_change_24h"]
            })

        return pd.DataFrame(rows)

    df = load_data()

    # -----------------------------
    # FETCH 3-DAY PRICE (CoinGecko)
    # -----------------------------
    @st.cache_data(ttl=300)
    def fetch_3day_price(symbol):
        symbol_map = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "BNB": "binancecoin",
            "SOL": "solana",
            "XRP": "ripple",
            "ADA": "cardano",
            "DOGE": "dogecoin"
        }

        if symbol not in symbol_map:
            return None

        coin_id = symbol_map[symbol]

        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"

        params = {
            "vs_currency": "inr",
            "days": 3
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (CryptoDashboard/1.0)"
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()

        prices = pd.DataFrame(
            response.json()["prices"],
            columns=["timestamp", "price"]
        )
        prices["timestamp"] = pd.to_datetime(prices["timestamp"], unit="ms")

        return prices

    # -----------------------------
    # SIDEBAR – COIN SELECTOR
    # -----------------------------
    st.sidebar.header("🔎 Select Coin")

    selected_coin = st.sidebar.selectbox(
        "Choose a Cryptocurrency",
        df["coin"]
    )

    coin_df = df[df["coin"] == selected_coin].iloc[0]

    # -----------------------------
    # DASHBOARD TITLE
    # -----------------------------
    st.title(f"🔍 {selected_coin} – Detailed Analysis (INR)")
    st.caption("Single-coin deep analysis dashboard")

    # -----------------------------
    # KPI CARDS
    # -----------------------------
    st.subheader("📌 Key Metrics")

    k1, k2, k3, k4, k5 = st.columns(5)

    k1.metric("Current Price (INR)", f"₹{coin_df['price']:,.2f}")
    k2.metric("24h Change (%)", f"{coin_df['change_24h']:.2f}%")
    k3.metric("Market Cap (INR)", f"₹{coin_df['market_cap']:,.0f}")
    k4.metric("Trading Volume (INR)", f"₹{coin_df['volume']:,.0f}")

    vol = abs(coin_df["change_24h"])
    if vol < 2:
        risk = "🟢 Low"
    elif vol < 5:
        risk = "🟡 Medium"
    else:
        risk = "🔴 High"

    k5.metric("Volatility Level", risk)

    # -----------------------------
    # LAST 3 DAYS PRICE LINE CHART
    # -----------------------------
    st.subheader("📈 Price Trend – Last 3 Days")

    price_df = fetch_3day_price(coin_df["symbol"])

    if price_df is not None:
        fig_line = px.line(
            price_df,
            x="timestamp",
            y="price",
            title=f"{selected_coin} Price Movement (Last 3 Days)",
            labels={"price": "Price (INR)", "timestamp": "Time"}
        )
        fig_line.update_traces(line_width=3)
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.warning("⚠️ 3-day price data not available for this coin.")

    # -----------------------------
    # COIN VS MARKET COMPARISON
    # -----------------------------
    st.subheader("📊 Coin vs Market Average")

    comparison_df = pd.DataFrame({
        "Metric": ["Price", "Market Cap", "Volume", "24h Change"],
        "Selected Coin": [
            coin_df["price"],
            coin_df["market_cap"],
            coin_df["volume"],
            coin_df["change_24h"]
        ],
        "Market Average": [
            df["price"].mean(),
            df["market_cap"].mean(),
            df["volume"].mean(),
            df["change_24h"].mean()
        ]
    })

    fig_compare = px.bar(
        comparison_df,
        x="Metric",
        y=["Selected Coin", "Market Average"],
        barmode="group",
        title="Performance Comparison"
    )
    st.plotly_chart(fig_compare, use_container_width=True)

    # -----------------------------
    # LIQUIDITY POSITION
    # -----------------------------
    st.subheader("💧 Liquidity Position")

    fig_liquidity = px.scatter(
        df,
        x="market_cap",
        y="volume",
        size="volume",
        log_x=True,
        log_y=True,
        color=df["coin"] == selected_coin,
        labels={"color": "Selected Coin"},
        title="Liquidity vs Market Size"
    )
    st.plotly_chart(fig_liquidity, use_container_width=True)

    # -----------------------------
    # SUMMARY INSIGHT
    # -----------------------------
    st.subheader("🧠 Insight Summary")

    st.info(
        f"""
        **{selected_coin}** currently shows a **{risk.lower()} volatility profile**.
        It has a market capitalization of **₹{coin_df['market_cap']:,.0f}**
        and a 24-hour trading volume of **₹{coin_df['volume']:,.0f}**.
        """
    )
