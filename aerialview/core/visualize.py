"""
Visualization utilities for AerialView.

This module provides stock charting functions using Plotly.
"""

import plotly.graph_objects as go
import pandas as pd


def candlestick_chart(df: pd.DataFrame, ticker: str) -> go.Figure:
    """
    Generate a candlestick chart with volume overlay.

    Args:
        df (pd.DataFrame): DataFrame with "date", "open", "high", "low", "close", "volume".
        ticker (str): Stock symbol for labeling.

    Returns:
        go.Figure: Interactive candlestick chart.
    """
    fig = go.Figure()

    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=df["date"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="Price",
        )
    )

    # Volume bar chart
    fig.add_trace(
        go.Bar(
            x=df["date"],
            y=df["volume"],
            name="Volume",
            marker_opacity=0.3,
            yaxis="y2",
        )
    )

    # Layout with dual y-axes
    fig.update_layout(
        title=f"{ticker} Candlestick Chart",
        yaxis=dict(title="Price"),
        yaxis2=dict(title="Volume", overlaying="y", side="right", showgrid=False),
        xaxis=dict(rangeslider=dict(visible=False)),
        legend=dict(orientation="h"),
        template="plotly_white",
    )

    return fig


def multi_ticker_comparison(data: dict) -> go.Figure:
    """
    Plot closing prices of multiple tickers for comparison.

    Args:
        data (dict): {ticker: DataFrame}

    Returns:
        go.Figure: Line chart with multiple tickers.
    """
    fig = go.Figure()

    for ticker, df in data.items():
        fig.add_trace(
            go.Scatter(
                x=df["date"],
                y=df["close"],
                mode="lines",
                name=ticker,
            )
        )

    fig.update_layout(
        title="Multi-Ticker Comparison",
        xaxis_title="Date",
        yaxis_title="Closing Price",
        template="plotly_white",
    )

    return fig