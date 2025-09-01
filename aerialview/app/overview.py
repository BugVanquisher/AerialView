from dash import html, dcc

layout = html.Div([
    html.H1("Overview Page"),
    html.P("This page provides an overview of the application metrics."),
    html.Div(id='overview-charts-placeholder', children=[
        dcc.Loading(
            type="default",
            children=html.Div("Charts will be displayed here.")
        )
    ])
])
