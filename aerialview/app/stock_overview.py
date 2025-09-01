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
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[
            {'label': 'Apple (AAPL)', 'value': 'AAPL'},
            {'label': 'Microsoft (MSFT)', 'value': 'MSFT'},
            {'label': 'Tesla (TSLA)', 'value': 'TSLA'},
        ],
        value=default_ticker,
        clearable=False,
        style={'width': '300px', 'margin-bottom': '20px'}
    ),
    html.Div(id='stock-charts-placeholder', children=[
        dcc.Loading(
            type="default",
            children=dcc.Graph(
                id='candlestick-chart',
                figure=candlestick_chart
            )
        )
    ])
])

# Dash callback for interactive chart update
from dash import Input, Output, callback

@callback(
    Output('candlestick-chart', 'figure'),
    Input('ticker-dropdown', 'value')
)
def update_candlestick_chart(selected_ticker):
    df = fetch_stock_data(selected_ticker)
    return create_candlestick_chart(df)