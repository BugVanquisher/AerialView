from dash import html, dcc, Input, Output
import plotly.graph_objs as go
from aerialview.utils.data_fetch import fetch_stock_data
from aerialview.core.visualize import multi_ticker_comparison
from aerialview.app import app

default_tickers = ["AAPL", "MSFT", "TSLA", "GOOGL"]

layout = html.Div([
    html.H1("Overview Page"),
    html.P("This page provides an overview of the application metrics."),
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': ticker, 'value': ticker} for ticker in default_tickers],
        value=default_tickers,
        multi=True
    ),
    html.Div(id='overview-charts-placeholder', children=[
        dcc.Loading(
            type="default",
            children=dcc.Graph(
                id='comparison-chart'
            )
        )
    ])
])

@app.callback(
    Output('comparison-chart', 'figure'),
    Input('ticker-dropdown', 'value')
)
def update_comparison_chart(selected_tickers):
    if not selected_tickers:
        selected_tickers = default_tickers
    data = {ticker: fetch_stock_data(ticker) for ticker in selected_tickers}
    fig = multi_ticker_comparison(data)
    return fig
