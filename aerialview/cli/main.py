#!/usr/bin/env python3
"""
AerialView CLI - Enhanced Command Line Interface
Advanced finance analytics from the command line
"""

import argparse
import sys
import os
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
import ta

class AerialViewCLI:
    def __init__(self):
        self.supported_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
        self.supported_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
        
    def fetch_data(self, ticker, start_date=None, end_date=None, period="1y", interval="1d"):
        """Fetch stock data using yfinance"""
        try:
            stock = yf.Ticker(ticker)
            
            if start_date and end_date:
                data = stock.history(start=start_date, end=end_date, interval=interval)
            else:
                data = stock.history(period=period, interval=interval)
            
            if data.empty:
                raise ValueError(f"No data found for ticker {ticker}")
            
            return data
        except Exception as e:
            print(f"❌ Error fetching data for {ticker}: {str(e)}")
            return None
    
    def add_technical_indicators(self, data):
        """Add technical indicators to the data"""
        # Moving averages
        data['MA_20'] = ta.trend.sma_indicator(data['Close'], window=20)
        data['MA_50'] = ta.trend.sma_indicator(data['Close'], window=50)
        
        # RSI
        data['RSI'] = ta.momentum.RSIIndicator(data['Close']).rsi()
        
        # MACD
        macd = ta.trend.MACD(data['Close'])
        data['MACD'] = macd.macd()
        data['MACD_Signal'] = macd.macd_signal()
        
        # Bollinger Bands
        data['BB_Upper'] = ta.volatility.bollinger_hband(data['Close'], window=20, window_dev=2)
        data['BB_Lower'] = ta.volatility.bollinger_lband(data['Close'], window=20, window_dev=2)
        
        return data
    
    def calculate_metrics(self, data):
        """Calculate performance metrics"""
        returns = data['Close'].pct_change().dropna()
        
        metrics = {
            'Current Price': data['Close'].iloc[-1],
            'Price Change': data['Close'].iloc[-1] - data['Close'].iloc[0],
            'Price Change %': ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100,
            'Total Return': ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100,
            'Volatility (Annual)': returns.std() * (252 ** 0.5) * 100,
            'Average Volume': data['Volume'].mean(),
            'Max Price': data['High'].max(),
            'Min Price': data['Low'].min(),
            'Current RSI': data['RSI'].iloc[-1] if 'RSI' in data.columns else None,
            'RSI Signal': self.get_rsi_signal(data['RSI'].iloc[-1]) if 'RSI' in data.columns else None
        }
        
        return metrics
    
    def get_rsi_signal(self, rsi_value):
        """Get RSI-based signal"""
        if rsi_value > 70:
            return "OVERBOUGHT (Sell Signal)"
        elif rsi_value < 30:
            return "OVERSOLD (Buy Signal)"
        else:
            return "NEUTRAL"
    
    def print_summary(self, ticker, data, metrics):
        """Print formatted summary"""
        print("\n" + "="*60)
        print(f"📈 AERIALVIEW ANALYSIS - {ticker.upper()}")
        print("="*60)
        
        # Price Information
        print(f"\n💰 PRICE INFORMATION")
        print(f"Current Price:     ${metrics['Current Price']:.2f}")
        print(f"Price Change:      ${metrics['Price Change']:+.2f}")
        print(f"Price Change %:    {metrics['Price Change %']:+.2f}%")
        print(f"Total Return:      {metrics['Total Return']:+.2f}%")
        
        # Technical Analysis
        print(f"\n📊 TECHNICAL ANALYSIS")
        if metrics['Current RSI']:
            print(f"RSI:               {metrics['Current RSI']:.2f}")
            print(f"RSI Signal:        {metrics['RSI Signal']}")
        
        # Volume & Volatility
        print(f"\n⚡ RISK METRICS")
        print(f"Volatility:        {metrics['Volatility (Annual)']:.2f}%")
        print(f"Average Volume:    {metrics['Average Volume']:,.0f}")
        
        # Price Range
        print(f"\n📊 PRICE RANGE")
        print(f"Max Price:         ${metrics['Max Price']:.2f}")
        print(f"Min Price:         ${metrics['Min Price']:.2f}")
        print(f"Current Price:     ${metrics['Current Price']:.2f}")
        
        # Trading Signals
        self.print_trading_signals(data)
        
        print("\n" + "="*60)
    
    def print_trading_signals(self, data):
        """Print trading signals based on technical indicators"""
        print(f"\n🚨 TRADING SIGNALS")
        
        # RSI Signal
        if 'RSI' in data.columns:
            rsi = data['RSI'].iloc[-1]
            if rsi > 70:
                print("⚠️  RSI: OVERBOUGHT - Consider selling")
            elif rsi < 30:
                print("✅ RSI: OVERSOLD - Consider buying")
            else:
                print("ℹ️  RSI: NEUTRAL")
        
        # MACD Signal
        if 'MACD' in data.columns and 'MACD_Signal' in data.columns:
            macd_bullish = data['MACD'].iloc[-1] > data['MACD_Signal'].iloc[-1]
            if macd_bullish:
                print("✅ MACD: BULLISH - Positive momentum")
            else:
                print("⚠️  MACD: BEARISH - Negative momentum")
        
        # Moving Average Signal
        if 'MA_20' in data.columns:
            above_ma20 = data['Close'].iloc[-1] > data['MA_20'].iloc[-1]
            if above_ma20:
                print("✅ MA20: Above moving average - Uptrend")
            else:
                print("⚠️  MA20: Below moving average - Downtrend")
    
    def save_chart(self, ticker, data, filename=None):
        """Save chart as HTML file"""
        if filename is None:
            filename = f"{ticker}_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        # Create subplot figure
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            subplot_titles=('Price & Volume', 'RSI', 'MACD'),
            row_heights=[0.6, 0.2, 0.2]
        )
        
        # Candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Price'
            ),
            row=1, col=1
        )
        
        # Moving averages
        if 'MA_20' in data.columns:
            fig.add_trace(
                go.Scatter(x=data.index, y=data['MA_20'], name='MA 20', line=dict(color='orange')),
                row=1, col=1
            )
        
        if 'MA_50' in data.columns:
            fig.add_trace(
                go.Scatter(x=data.index, y=data['MA_50'], name='MA 50', line=dict(color='blue')),
                row=1, col=1
            )
        
        # Volume
        colors = ['green' if close > open else 'red' for close, open in zip(data['Close'], data['Open'])]
        fig.add_trace(
            go.Bar(x=data.index, y=data['Volume'], name='Volume', marker_color=colors, opacity=0.3),
            row=1, col=1
        )
        
        # RSI
        if 'RSI' in data.columns:
            fig.add_trace(
                go.Scatter(x=data.index, y=data['RSI'], name='RSI', line=dict(color='purple')),
                row=2, col=1
            )
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
        
        # MACD
        if 'MACD' in data.columns:
            fig.add_trace(
                go.Scatter(x=data.index, y=data['MACD'], name='MACD', line=dict(color='blue')),
                row=3, col=1
            )
            fig.add_trace(
                go.Scatter(x=data.index, y=data['MACD_Signal'], name='Signal', line=dict(color='red')),
                row=3, col=1
            )
        
        fig.update_layout(
            title=f'{ticker.upper()} - Technical Analysis',
            xaxis_rangeslider_visible=False,
            height=800,
            template='plotly_dark'
        )
        
        fig.write_html(filename)
        print(f"📊 Chart saved as: {filename}")
    
    def compare_stocks(self, tickers, period="6mo"):
        """Compare multiple stocks"""
        print(f"\n📊 COMPARING STOCKS: {', '.join(tickers)}")
        print("="*60)
        
        comparison_data = {}
        
        for ticker in tickers:
            data = self.fetch_data(ticker, period=period)
            if data is not None:
                data = self.add_technical_indicators(data)
                metrics = self.calculate_metrics(data)
                comparison_data[ticker] = metrics
        
        if not comparison_data:
            print("❌ No data available for comparison")
            return
        
        # Print comparison table
        print(f"\n{'Ticker':<8} {'Price':<10} {'Change %':<10} {'RSI':<8} {'Volatility':<12}")
        print("-" * 60)
        
        for ticker, metrics in comparison_data.items():
            rsi_val = f"{metrics['Current RSI']:.1f}" if metrics['Current RSI'] else "N/A"
            print(f"{ticker:<8} ${metrics['Current Price']:<9.2f} {metrics['Price Change %']:<9.2f}% {rsi_val:<8} {metrics['Volatility (Annual)']:<11.1f}%")

def main():
    parser = argparse.ArgumentParser(
        description="AerialView CLI - Advanced Finance Analytics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m aerialview --ticker AAPL
  python -m aerialview --ticker AAPL --period 6mo --save-chart
  python -m aerialview --compare AAPL,GOOGL,MSFT
  python -m aerialview --ticker AAPL --start 2023-01-01 --end 2023-12-31
        """
    )
    
    parser.add_argument('--ticker', '-t', type=str, help='Stock ticker symbol (e.g., AAPL)')
    parser.add_argument('--compare', '-c', type=str, help='Compare multiple tickers (comma-separated)')
    parser.add_argument('--period', '-p', type=str, default='1y',
                       help='Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)')
    parser.add_argument('--start', type=str, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', type=str, help='End date (YYYY-MM-DD)')
    parser.add_argument('--interval', type=str, default='1d',
                       help='Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)')
    parser.add_argument('--save-chart', action='store_true', help='Save chart as HTML file')
    parser.add_argument('--output', '-o', type=str, help='Output filename for chart')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.ticker and not args.compare:
        parser.error("Either --ticker or --compare must be specified")
    
    cli = AerialViewCLI()
    
    try:
        # Compare multiple stocks
        if args.compare:
            tickers = [t.strip().upper() for t in args.compare.split(',')]
            cli.compare_stocks(tickers, period=args.period)
            return
        
        # Single stock analysis
        ticker = args.ticker.upper()
        print(f"🚀 Fetching data for {ticker}...")
        
        # Fetch data
        if args.start and args.end:
            data = cli.fetch_data(ticker, start_date=args.start, end_date=args.end, interval=args.interval)
        else:
            data = cli.fetch_data(ticker, period=args.period, interval=args.interval)
        
        if data is None:
            sys.exit(1)
        
        # Add technical indicators
        data = cli.add_technical_indicators(data)
        
        # Calculate metrics
        metrics = cli.calculate_metrics(data)
        
        # Print summary
        cli.print_summary(ticker, data, metrics)
        
        # Save chart if requested
        if args.save_chart:
            cli.save_chart(ticker, data, args.output)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()