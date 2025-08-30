"""
Data fetching utilities for AerialView.

This module handles stock market data retrieval from external sources
(e.g., Yahoo Finance). Additional providers can be added easily by
extending the `fetch_stock_data` function.
"""

import logging
import yfinance as yf
import pandas as pd
from typing import List, Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def fetch_stock_data(
    ticker: str, start: str, end: str, interval: str = "1d"
) -> Optional[pd.DataFrame]:
    """
    Fetch historical stock data from Yahoo Finance.

    Args:
        ticker (str): Stock symbol, e.g., "AAPL".
        start (str): Start date in "YYYY-MM-DD".
        end (str): End date in "YYYY-MM-DD".
        interval (str, optional): Data interval ("1d", "1wk", "1mo"). Defaults to "1d".

    Returns:
        pd.DataFrame: Historical OHLCV data with datetime index.
                      None if fetching fails.
    """
    try:
        logger.info(f"Fetching {ticker} from {start} to {end}...")
        df = yf.download(ticker, start=start, end=end, interval=interval, progress=False)

        if df.empty:
            logger.warning(f"No data returned for {ticker}.")
            return None

        df.reset_index(inplace=True)
        df.rename(columns=str.lower, inplace=True)
        return df

    except Exception as e:
        logger.error(f"Error fetching {ticker}: {e}")
        return None


def fetch_multiple_stocks(
    tickers: List[str], start: str, end: str, interval: str = "1d"
) -> dict:
    """
    Fetch data for multiple stock tickers.

    Args:
        tickers (List[str]): List of stock symbols.
        start (str): Start date.
        end (str): End date.
        interval (str, optional): Interval ("1d", "1wk", "1mo").

    Returns:
        dict: {ticker: DataFrame} mapping of ticker symbols to data.
    """
    data = {}
    for t in tickers:
        df = fetch_stock_data(t, start, end, interval)
        if df is not None:
            data[t] = df
    return data