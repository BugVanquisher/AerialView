

from dash import html, dcc

layout = html.Div([
    html.H1("Stock Overview"),
    html.P("This page provides an overview of a selected stock, including relevant charts and metrics."),
    html.Div(id='stock-charts-placeholder', children=[
        dcc.Loading(
            type="default",
            children=html.Div("Stock-specific charts will be displayed here.")
        )
    ])
])