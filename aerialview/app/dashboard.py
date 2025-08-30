"""
Streamlit dashboard for AerialView.

This app provides an interactive interface to explore stock market data
with candlestick charts, comparisons, and more.
"""

import streamlit as st
import pandas as pd
from aerialview.core.data_fetch import fetch_stock_data, fetch_multiple_stocks
from aerialview.core.visualize import candlestick_chart, multi_ticker_comparison


# -------------------------------
# Streamlit Page Setup
# -------------------------------
st.set_page_config(
    page_title="AerialView - Stock Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -------------------------------
# Sidebar Controls
# -------------------------------
st.sidebar.title("📊 AerialView Controls")

# Input tickers
tickers = st.sidebar.text_input(
    "Enter stock ticker(s) separated by commas",
    value="AAPL, MSFT",
).replace(" ", "").split(",")

# Date range
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
with col2:
    end_date = st.date_input("End Date", pd.to_datetime("today"))

# Interval selection
interval = st.sidebar.selectbox(
    "Interval", ["1d", "1wk", "1mo"], index=0
)

# Chart type selection
chart_type = st.sidebar.radio(
    "Select Chart Type", ["Candlestick", "Multi-Ticker Comparison"]
)


# -------------------------------
# Main Dashboard
# -------------------------------
st.title("📈 AerialView: Stock Market Dashboard")

if st.sidebar.button("Generate Visualization"):
    if chart_type == "Candlestick" and len(tickers) == 1:
        df = fetch_stock_data(tickers[0], str(start_date), str(end_date), interval)
        if df is not None:
            fig = candlestick_chart(df, tickers[0])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"No data available for {tickers[0]}.")

    elif chart_type == "Multi-Ticker Comparison" and len(tickers) > 1:
        data = fetch_multiple_stocks(tickers, str(start_date), str(end_date), interval)
        if data:
            fig = multi_ticker_comparison(data)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for the selected tickers.")
    else:
        st.info("ℹ️ For candlestick, please select only one ticker.")