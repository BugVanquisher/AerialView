from dash import html, dcc
import plotly.graph_objs as go
from aerialview.utils.visualizations import create_candlestick_chart
from aerialview.utils.data_fetch import fetch_stock_data

default_ticker = "AAPL"
stock_data = fetch_stock_data(default_ticker)
candlestick_chart = create_candlestick_chart(stock_data)

layout = html.Div([
    html.H1("Overview Page"),
    html.P("This page provides an overview of the application metrics."),
    html.Div(id='overview-charts-placeholder', children=[
        dcc.Loading(
            type="default",
            children=dcc.Graph(
                figure=candlestick_chart,
                id='candlestick-chart'
            )
        )
    ])
])
