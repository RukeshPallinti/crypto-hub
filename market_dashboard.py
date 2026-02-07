def run_market_dashboard():
    # ------------------------------------------
    # Cryptocurrency Dashboard (INR) – Top 50 Coins (LIVE DATA)
    # ------------------------------------------

    import streamlit as st
    import pandas as pd
    import numpy as np
    import requests
    import plotly.express as px
    import seaborn as sns
    import matplotlib.pyplot as plt
    import os

    st.set_page_config(
        page_title="Crypto Market Dashboard",
        layout="wide"
    )

    # -----------------------------
    # API CONFIG
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
    # LOAD LIVE DATA
    # -----------------------------
    @st.cache_data(ttl=300)
    def load_crypto_data():
        response = requests.get(API_URL, headers=HEADERS, params=PARAMS, timeout=10)
        response.raise_for_status()
        data = response.json()["data"]

        rows = []
        for coin in data:
            quote = coin["quote"]["INR"]
            rows.append({
                "coin": coin["name"],
                "price_in_inr": quote["price"],
                "market_cap": quote["market_cap"],
                "trading_volume_inr": quote["volume_24h"],
                "price_change_percentage_24h": quote["percent_change_24h"],
                "high_24h": quote["price"] * (1 + quote["percent_change_24h"] / 100),
                "low_24h": quote["price"] * (1 - abs(quote["percent_change_24h"]) / 100)
            })

        return pd.DataFrame(rows)

    df = load_crypto_data()

    if df.empty:
        st.error("⚠️ Failed to load crypto data")
        st.stop()

    # -----------------------------
    # FEATURE ENGINEERING
    # -----------------------------
    df["trading_volume_millions"] = df["trading_volume_inr"] / 1_000_000
    df["volatility_score"] = df["price_change_percentage_24h"].abs()

    # -----------------------------
    # MARKET SIGNAL
    # -----------------------------
    def generate_market_signal(row):
        avg_volume = df["trading_volume_millions"].mean()
        if row["price_change_percentage_24h"] > 2 and row["trading_volume_millions"] > avg_volume:
            return "🟢 Bullish"
        elif row["price_change_percentage_24h"] < -2 and row["volatility_score"] > 10:
            return "🔴 Bearish"
        return "🟡 Neutral"

    df["market_signal"] = df.apply(generate_market_signal, axis=1)

    # -----------------------------
    # SIDEBAR FILTERS
    # -----------------------------
    st.sidebar.header("🔎 Market Filters")

    change_range = st.sidebar.slider(
        "24h % Change",
        -20.0, 20.0, (-5.0, 5.0)
    )

    signal_filter = st.sidebar.multiselect(
        "Market Signal",
        options=df["market_signal"].unique(),
        default=df["market_signal"].unique()
    )

    filtered_df = df[
        (df["price_change_percentage_24h"].between(change_range[0], change_range[1])) &
        (df["market_signal"].isin(signal_filter))
        ]

    # -----------------------------
    # TITLE
    # -----------------------------
    st.title("📊 Cryptocurrency Market Dashboard (INR)")
    st.markdown("Live analysis of **Top 50 cryptocurrencies** using CoinMarketCap data.")

    # -----------------------------
    # MARKET REGIME
    # -----------------------------
    def market_regime(df):
        avg = df["price_change_percentage_24h"].mean()
        vol = df["volatility_score"].mean()

        if avg > 1 and vol < 8:
            return "🟢 Bull Market"
        elif avg < -1 and vol > 10:
            return "🔴 Bear Market"
        return "🟡 Sideways Market"

    st.subheader(f"📌 Market Regime: {market_regime(df)}")

    # -----------------------------
    # KEY METRICS
    # -----------------------------
    st.subheader("🔑 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Market Cap (INR)", f"{df['market_cap'].sum():,.0f}")
    col2.metric("Avg 24h Change (%)", f"{df['price_change_percentage_24h'].mean():.2f}")
    col3.metric("Avg Volatility (%)", f"{df['volatility_score'].mean():.2f}")
    col4.metric("Total Volume (M INR)", f"{df['trading_volume_millions'].sum():,.0f}")

    # -----------------------------
    # TOP MOVERS
    # -----------------------------
    st.subheader("🚀 Top Gainers & Losers")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### 🚀 Top Gainers")
        st.dataframe(
            df.sort_values("price_change_percentage_24h", ascending=False)
            .head(5)[["coin", "price_in_inr", "price_change_percentage_24h", "market_signal"]],
            use_container_width=True
        )

    with c2:
        st.markdown("### 💀 Top Losers")
        st.dataframe(
            df.sort_values("price_change_percentage_24h")
            .head(5)[["coin", "price_in_inr", "price_change_percentage_24h", "market_signal"]],
            use_container_width=True
        )

    # -----------------------------
    # PRICE CHART
    # -----------------------------
    st.subheader("💰 Current Prices")

    fig_price = px.bar(
        filtered_df.sort_values("market_cap", ascending=False),
        x="coin",
        y="price_in_inr",
        color="market_signal",
        hover_data=["market_cap", "trading_volume_millions"],
        title="Cryptocurrency Prices (INR)"
    )
    st.plotly_chart(fig_price, use_container_width=True)

    # -----------------------------
    # VOLATILITY
    # -----------------------------
    st.subheader("⚡ 24-Hour Volatility")

    fig_vol = px.bar(
        filtered_df,
        x="coin",
        y="volatility_score",
        color="market_signal",
        title="24h Volatility (%)"
    )
    st.plotly_chart(fig_vol, use_container_width=True)

    # -----------------------------
    # MARKET CAP DISTRIBUTION
    # -----------------------------
    st.subheader("🏛 Market Cap Distribution")

    fig_mc = px.pie(
        df,
        values="market_cap",
        names="coin",
        hole=0.4
    )
    st.plotly_chart(fig_mc, use_container_width=True)

    # -----------------------------
    # HIGH VS LOW
    # -----------------------------
    st.subheader("📈 24h High vs Low")

    melted = df.melt(
        id_vars="coin",
        value_vars=["high_24h", "low_24h"],
        var_name="Metric",
        value_name="Price"
    )

    fig_hl = px.bar(
        melted,
        x="coin",
        y="Price",
        color="Metric",
        barmode="group"
    )
    st.plotly_chart(fig_hl, use_container_width=True)

    # -----------------------------
    # PRICE VS VOLUME
    # -----------------------------
    st.subheader("📊 Price vs Volume")

    fig_scatter = px.scatter(
        filtered_df,
        x="price_in_inr",
        y="trading_volume_millions",
        size="market_cap",
        color="market_signal",
        log_x=True,
        log_y=True
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # -----------------------------
    # CORRELATION HEATMAP
    # -----------------------------
    st.subheader("📊 Correlation Heatmap")

    numeric_cols = [
        "price_in_inr",
        "market_cap",
        "trading_volume_inr",
        "price_change_percentage_24h",
        "volatility_score"
    ]

    corr = df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)
