# Crypto Market Analytics Platform

An **interactive, real-time cryptocurrency analytics platform** built using Streamlit.  
This project provides **market-wide insights** as well as **coin-level analysis** for top cryptocurrencies in INR.  

## 🔹 Overview

This platform contains **two main dashboards**:

1. **Market Dashboard**
   - Live data for the top 50 cryptocurrencies
   - Key metrics: Market cap, price, volatility, trading volume
   - Visualizations: Prices, volatility charts, high vs low, price vs volume, market cap distribution, and correlation heatmaps
   - Market signals (Bullish / Neutral / Bearish) generated from real-time analysis

2. **Coin Dashboard**
   - Detailed analysis for a selected cryptocurrency
   - Coin-specific price history, volatility, and trends
   - Comparative charts and insights for deeper understanding
   - Enables focused analysis for investors or traders

## 🔹 Features

- Real-time cryptocurrency market data from **CoinMarketCap API**
- Multi-dashboard interface (Market & Coin dashboards) in **one Streamlit app**
- Volatility and market signal analysis
- Interactive charts with **Plotly**, **Seaborn**, and **Matplotlib**
- AI-powered market insights (summary interpretation of top coins)
- Clean, responsive UI with sidebar navigation

## 🔹 Tech Stack

- **Python** – Core language
- **Streamlit** – Interactive dashboard framework
- **Pandas & NumPy** – Data processing and feature engineering
- **Plotly, Seaborn & Matplotlib** – Data visualization
- **CoinMarketCap API** – Real-time crypto market data
- **OpenAI GPT (optional)** – AI-powered insights generation

## 🔹 How to Run

1. Clone the repository:
git clone https://github.com/RukeshPallinti/crypto-hub.git
2. Install Dependencies
pip install -r requirements.txt
3. Set your **COINMARKET API** Key 
CMC_API_KEY = "YOUR_KEY"
4. Run the Streamlit app.py
streamlit run app.py
5. Open the link in your browser. Use the sidebar to switch between Market Dashboard and Coin Dashboard.

🔹 Project Evolution

Version 1: Initial prototype using static CSV data for top cryptocurrencies

Version 2 (This Version): Full live data integration, multi-dashboard system, AI insights, and enhanced visualizations

**Screenshots / Previews**

Images of both dashboards are available in the screenshots/ folder to showcase the layout and interactive charts.
1. Market Dashboard
2. Coin Dashboard

🔹 Future Improvements

* Integration of alert systems (email/Telegram)
* Historical trend predictions using ML
* Dark mode / theme toggle
* Additional coin-specific analytics features

Author: Rukesh
GitHub: https://github.com/RukeshPallinti
