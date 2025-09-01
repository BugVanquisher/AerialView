from dash import html, dcc
import plotly.graph_objects as go
from aerialview.utils.visualizations import create_candlestick_chart
from aerialview.utils.data_fetch import fetch_stock_data

default_ticker = "AAPL"
df = fetch_stock_data(default_ticker)
candlestick_chart = create_candlestick_chart(df)

layout = html.Div([
    html.H1("Stock Overview"),
    html.P("This page provides an overview of a selected stock, including relevant charts and metrics."),
    html.Div(id='stock-charts-placeholder', children=[
        dcc.Loading(
            type="default",
            children=dcc.Graph(
                figure=candlestick_chart
            )
        )
    ])
])