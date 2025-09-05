import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="AerialView - Advanced Finance Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(45deg, #fff, #e0e0e0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .alert {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid;
    }
    
    .alert-success {
        background-color: rgba(46, 125, 50, 0.1);
        border-left-color: #2e7d32;
        color: #2e7d32;
    }
    
    .alert-warning {
        background-color: rgba(255, 152, 0, 0.1);
        border-left-color: #ff9800;
        color: #ff9800;
    }
    
    .alert-error {
        background-color: rgba(244, 67, 54, 0.1);
        border-left-color: #f44336;
        color: #f44336;
    }
</style>
""", unsafe_allow_html=True)

class SimpleFinanceAnalyzer:
    def __init__(self):
        self.cache_duration = 300  # 5 minutes cache
        
    @st.cache_data(ttl=300)
    def fetch_stock_data(_self, ticker, period="1y", interval="1d"):
        """Fetch stock data with caching and error handling"""
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period=period, interval=interval)
            
            if data.empty:
                st.error(f"No data found for ticker {ticker}")
                return None
                
            # Add technical indicators
            data = _self.add_technical_indicators(data)
            return data
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {str(e)}")
            return None
    
    def calculate_rsi(self, prices, window=14):
        """Calculate RSI using pandas"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calculate MACD using pandas"""
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        macd_signal = macd.ewm(span=signal).mean()
        macd_histogram = macd - macd_signal
        return macd, macd_signal, macd_histogram
    
    def calculate_bollinger_bands(self, prices, window=20, std_dev=2):
        """Calculate Bollinger Bands using pandas"""
        middle = prices.rolling(window=window).mean()
        std = prices.rolling(window=window).std()
        upper = middle + (std * std_dev)
        lower = middle - (std * std_dev)
        return upper, middle, lower
    
    def calculate_stochastic(self, high, low, close, k_window=14, d_window=3):
        """Calculate Stochastic Oscillator using pandas"""
        lowest_low = low.rolling(window=k_window).min()
        highest_high = high.rolling(window=k_window).max()
        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d_percent = k_percent.rolling(window=d_window).mean()
        return k_percent, d_percent
    
    def add_technical_indicators(self, data):
        """Add comprehensive technical indicators using pandas"""
        # Moving averages
        data['MA_20'] = data['Close'].rolling(window=20).mean()
        data['MA_50'] = data['Close'].rolling(window=50).mean()
        data['MA_200'] = data['Close'].rolling(window=200).mean()
        
        # Bollinger Bands
        data['BB_Upper'], data['BB_Middle'], data['BB_Lower'] = self.calculate_bollinger_bands(data['Close'])
        
        # RSI
        data['RSI'] = self.calculate_rsi(data['Close'])
        
        # MACD
        data['MACD'], data['MACD_Signal'], data['MACD_Histogram'] = self.calculate_macd(data['Close'])
        
        # Stochastic
        data['Stoch_K'], data['Stoch_D'] = self.calculate_stochastic(data['High'], data['Low'], data['Close'])
        
        # Volume indicators
        data['Volume_MA'] = data['Volume'].rolling(window=20).mean()
        
        # Calculate OBV manually
        data['OBV'] = 0.0
        data.loc[data.index[0], 'OBV'] = data['Volume'].iloc[0]
        for i in range(1, len(data)):
            if data['Close'].iloc[i] > data['Close'].iloc[i-1]:
                data.loc[data.index[i], 'OBV'] = data['OBV'].iloc[i-1] + data['Volume'].iloc[i]
            elif data['Close'].iloc[i] < data['Close'].iloc[i-1]:
                data.loc[data.index[i], 'OBV'] = data['OBV'].iloc[i-1] - data['Volume'].iloc[i]
            else:
                data.loc[data.index[i], 'OBV'] = data['OBV'].iloc[i-1]
        
        data['Volume_OBV'] = data['OBV']
        
        return data
    
    def calculate_risk_metrics(self, data, risk_free_rate=0.02):
        """Calculate advanced risk metrics"""
        returns = data['Close'].pct_change().dropna()
        
        metrics = {
            'Total Return': (data['Close'].iloc[-1] / data['Close'].iloc[0] - 1) * 100,
            'Volatility': returns.std() * np.sqrt(252) * 100,
            'Sharpe Ratio': (returns.mean() * 252 - risk_free_rate) / (returns.std() * np.sqrt(252)),
            'Max Drawdown': ((data['Close'] / data['Close'].cummax()) - 1).min() * 100,
            'VaR (95%)': np.percentile(returns, 5) * 100,
            'Current Price': data['Close'].iloc[-1],
            'Daily Change': (data['Close'].iloc[-1] / data['Close'].iloc[-2] - 1) * 100 if len(data) > 1 else 0
        }
        
        return metrics
    
    def create_advanced_candlestick_chart(self, data, ticker):
        """Create an advanced candlestick chart with multiple indicators"""
        fig = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            subplot_titles=('Price & Volume', 'RSI', 'MACD', 'Stochastic'),
            row_heights=[0.5, 0.2, 0.2, 0.1]
        )
        
        # Candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Price',
                increasing_line_color='#00ff88',
                decreasing_line_color='#ff4444'
            ),
            row=1, col=1
        )
        
        # Moving averages
        fig.add_trace(
            go.Scatter(x=data.index, y=data['MA_20'], name='MA 20', 
                      line=dict(color='orange', width=1)), row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=data.index, y=data['MA_50'], name='MA 50', 
                      line=dict(color='blue', width=1)), row=1, col=1
        )
        
        # Bollinger Bands
        fig.add_trace(
            go.Scatter(x=data.index, y=data['BB_Upper'], name='BB Upper', 
                      line=dict(color='gray', width=1, dash='dash'), 
                      fill=None), row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=data.index, y=data['BB_Lower'], name='BB Lower', 
                      line=dict(color='gray', width=1, dash='dash'),
                      fill='tonexty', fillcolor='rgba(128,128,128,0.1)'), row=1, col=1
        )
        
        # Volume
        colors = ['green' if close > open else 'red' for close, open in zip(data['Close'], data['Open'])]
        fig.add_trace(
            go.Bar(x=data.index, y=data['Volume'], name='Volume', 
                  marker_color=colors, opacity=0.3, yaxis='y2'), row=1, col=1
        )
        
        # RSI
        fig.add_trace(
            go.Scatter(x=data.index, y=data['RSI'], name='RSI', 
                      line=dict(color='purple', width=2)), row=2, col=1
        )
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
        
        # MACD
        fig.add_trace(
            go.Scatter(x=data.index, y=data['MACD'], name='MACD', 
                      line=dict(color='blue', width=2)), row=3, col=1
        )
        fig.add_trace(
            go.Scatter(x=data.index, y=data['MACD_Signal'], name='Signal', 
                      line=dict(color='red', width=1)), row=3, col=1
        )
        fig.add_trace(
            go.Bar(x=data.index, y=data['MACD_Histogram'], name='Histogram', 
                  marker_color='gray', opacity=0.5), row=3, col=1
        )
        
        # Stochastic
        fig.add_trace(
            go.Scatter(x=data.index, y=data['Stoch_K'], name='%K', 
                      line=dict(color='orange', width=2)), row=4, col=1
        )
        fig.add_trace(
            go.Scatter(x=data.index, y=data['Stoch_D'], name='%D', 
                      line=dict(color='blue', width=1)), row=4, col=1
        )
        
        # Update layout
        fig.update_layout(
            title=f'{ticker} - Advanced Technical Analysis',
            xaxis_rangeslider_visible=False,
            height=900,
            showlegend=True,
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        # Update y-axes
        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_yaxes(title_text="RSI", row=2, col=1)
        fig.update_yaxes(title_text="MACD", row=3, col=1)
        fig.update_yaxes(title_text="Stoch", row=4, col=1)
        
        return fig
    
    def create_correlation_heatmap(self, tickers, period="6mo"):
        """Create correlation heatmap for multiple tickers"""
        data = {}
        for ticker in tickers:
            stock_data = self.fetch_stock_data(ticker, period=period)
            if stock_data is not None:
                data[ticker] = stock_data['Close']
        
        if not data:
            return None
            
        df = pd.DataFrame(data)
        correlation_matrix = df.corr()
        
        fig = px.imshow(
            correlation_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale='RdBu',
            title="Stock Correlation Matrix"
        )
        
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def get_market_news(self, ticker):
        """Simulate getting market news"""
        return [
            {"title": f"Latest {ticker} earnings report shows strong growth", "sentiment": "Positive"},
            {"title": f"{ticker} announces new strategic partnership", "sentiment": "Positive"},
            {"title": f"Market volatility affects {ticker} trading", "sentiment": "Neutral"}
        ]

def main():
    analyzer = SimpleFinanceAnalyzer()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📈 AerialView</h1>
        <p>Advanced Finance Analytics & Market Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("🎛️ Control Panel")
        
        # Theme toggle
        theme = st.selectbox("🎨 Theme", ["Dark", "Light"])
        
        # Stock selection
        st.subheader("📊 Stock Analysis")
        ticker = st.text_input("Enter Stock Ticker", value="AAPL", help="e.g., AAPL, GOOGL, MSFT")
        
        # Time period
        period = st.selectbox("📅 Time Period", 
                             ["1mo", "3mo", "6mo", "1y", "2y", "5y"], 
                             index=3)
        
        # Analysis type
        analysis_type = st.selectbox("📈 Analysis Type", 
                                   ["Technical Analysis", "Risk Metrics", "Correlation Analysis"])
        
        # Additional tickers for correlation
        if analysis_type == "Correlation Analysis":
            additional_tickers = st.text_area("Additional Tickers (comma-separated)", 
                                            value="GOOGL,MSFT,TSLA,AMZN")
        
        # Fetch data button
        if st.button("🚀 Analyze", type="primary"):
            st.session_state.fetch_data = True
    
    # Main content
    if hasattr(st.session_state, 'fetch_data') and st.session_state.fetch_data:
        ticker = ticker.upper()
        
        with st.spinner(f"Fetching data for {ticker}..."):
            data = analyzer.fetch_stock_data(ticker, period=period)
        
        if data is not None:
            # Display current metrics
            col1, col2, col3, col4 = st.columns(4)
            
            metrics = analyzer.calculate_risk_metrics(data)
            
            with col1:
                change_color = "green" if metrics['Daily Change'] > 0 else "red"
                st.markdown(f"""
                <div class="metric-card">
                    <h3>💰 Current Price</h3>
                    <h2>${metrics['Current Price']:.2f}</h2>
                    <p style="color: {change_color};">
                        {metrics['Daily Change']:+.2f}% today
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>📈 Total Return</h3>
                    <h2>{metrics['Total Return']:+.1f}%</h2>
                    <p>Period: {period}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>⚡ Volatility</h3>
                    <h2>{metrics['Volatility']:.1f}%</h2>
                    <p>Annualized</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🎯 Sharpe Ratio</h3>
                    <h2>{metrics['Sharpe Ratio']:.2f}</h2>
                    <p>Risk-adjusted return</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Analysis based on selected type
            if analysis_type == "Technical Analysis":
                st.subheader(f"📊 Technical Analysis - {ticker}")
                
                # Advanced candlestick chart
                fig = analyzer.create_advanced_candlestick_chart(data, ticker)
                st.plotly_chart(fig, use_container_width=True)
                
                # Trading signals
                st.subheader("🚨 Trading Signals")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if not pd.isna(data['RSI'].iloc[-1]):
                        latest_rsi = data['RSI'].iloc[-1]
                        if latest_rsi > 70:
                            st.markdown('<div class="alert alert-warning">⚠️ RSI Overbought (Sell Signal)</div>', unsafe_allow_html=True)
                        elif latest_rsi < 30:
                            st.markdown('<div class="alert alert-success">✅ RSI Oversold (Buy Signal)</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="alert">ℹ️ RSI Neutral</div>', unsafe_allow_html=True)
                
                with col2:
                    if not pd.isna(data['MACD'].iloc[-1]) and not pd.isna(data['MACD_Signal'].iloc[-1]):
                        if data['MACD'].iloc[-1] > data['MACD_Signal'].iloc[-1]:
                            st.markdown('<div class="alert alert-success">✅ MACD Bullish</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="alert alert-error">❌ MACD Bearish</div>', unsafe_allow_html=True)
                
                with col3:
                    if not pd.isna(data['MA_20'].iloc[-1]):
                        if data['Close'].iloc[-1] > data['MA_20'].iloc[-1]:
                            st.markdown('<div class="alert alert-success">✅ Above MA20</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="alert alert-error">❌ Below MA20</div>', unsafe_allow_html=True)
            
            elif analysis_type == "Risk Metrics":
                st.subheader(f"⚠️ Risk Analysis - {ticker}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Max Drawdown", f"{metrics['Max Drawdown']:.2f}%")
                    st.metric("Value at Risk (95%)", f"{metrics['VaR (95%)']:.2f}%")
                    st.metric("Sharpe Ratio", f"{metrics['Sharpe Ratio']:.3f}")
                
                with col2:
                    risk_level = "Low" if metrics['Volatility'] < 20 else "Medium" if metrics['Volatility'] < 40 else "High"
                    risk_color = "green" if risk_level == "Low" else "orange" if risk_level == "Medium" else "red"
                    
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>🎚️ Risk Level</h3>
                        <h2 style="color: {risk_color};">{risk_level}</h2>
                        <p>Based on volatility: {metrics['Volatility']:.1f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            elif analysis_type == "Correlation Analysis":
                if 'additional_tickers' in locals():
                    tickers_list = [ticker] + [t.strip().upper() for t in additional_tickers.split(',')]
                    st.subheader("🔄 Correlation Analysis")
                    
                    fig = analyzer.create_correlation_heatmap(tickers_list, period=period)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
            
            # Market news section
            st.subheader(f"📰 Market News - {ticker}")
            news = analyzer.get_market_news(ticker)
            
            for item in news:
                sentiment_color = "green" if item['sentiment'] == 'Positive' else "orange" if item['sentiment'] == 'Neutral' else "red"
                st.markdown(f"""
                <div class="alert">
                    <strong>{item['title']}</strong><br>
                    <small style="color: {sentiment_color};">Sentiment: {item['sentiment']}</small>
                </div>
                """, unsafe_allow_html=True)
    
    else:
        # Welcome screen
        st.markdown("""
        ## 🚀 Welcome to AerialView 2.0
        
        Your advanced finance analytics dashboard with cutting-edge features:
        
        ### ✨ Key Features
        - **Advanced Technical Analysis** - RSI, MACD, Bollinger Bands, Stochastic
        - **Risk Management** - VaR, Sharpe Ratio, Maximum Drawdown
        - **Real-time Insights** - Live data with intelligent caching
        - **Correlation Analysis** - Multi-asset correlation matrices
        - **Modern UI** - Responsive design with dark/light themes
        - **Trading Signals** - Automated buy/sell recommendations
        
        ### 🎯 Getting Started
        1. Enter a stock ticker in the sidebar (e.g., AAPL, GOOGL, MSFT)
        2. Select your preferred time period
        3. Choose analysis type
        4. Click **Analyze** to get started!
        
        ### 📊 Supported Analysis Types
        - **Technical Analysis**: Complete charting with indicators
        - **Risk Metrics**: Comprehensive risk assessment
        - **Correlation Analysis**: Multi-stock correlation studies
        """)

    # Footer
    st.markdown("""
    ---
    <div style="text-align: center; color: #666; padding: 2rem;">
        Made with ❤️ by BugVanquisher | Powered by Streamlit & Plotly
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()