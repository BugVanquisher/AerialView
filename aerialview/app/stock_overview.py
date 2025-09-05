from dash import html, dcc
from aerialview.core.visualize import multi_ticker_comparison

default_tickers = ["AAPL", "MSFT", "TSLA"]
figure = multi_ticker_comparison(default_tickers)

layout = html.Div([
    html.H1("Overview"),
    html.P("This page provides an overview of selected stocks, comparing their performance."),
    dcc.Dropdown(
        id='tickers-dropdown',
        options=[
            {'label': 'Apple (AAPL)', 'value': 'AAPL'},
            {'label': 'Microsoft (MSFT)', 'value': 'MSFT'},
            {'label': 'Tesla (TSLA)', 'value': 'TSLA'},
            {'label': 'Google (GOOGL)', 'value': 'GOOGL'},
        ],
        value=default_tickers,
        multi=True,
        clearable=False,
        style={'width': '400px', 'margin-bottom': '20px'}
    ),
    dcc.Loading(
        type="default",
        children=dcc.Graph(
            id='multi-ticker-chart',
            figure=figure
        )
    )
])

from dash import Input, Output, callback

@callback(
    Output('multi-ticker-chart', 'figure'),
    Input('tickers-dropdown', 'value')
)
def update_multi_ticker_chart(selected_tickers):
    if not selected_tickers:
        selected_tickers = default_tickers
    return multi_ticker_comparison(selected_tickers)