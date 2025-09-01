from dash import dcc, html
from dash.dependencies import Input, Output
import yfinance as yf
from dash import Dash

from pages import stock_overview, overview

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/stock-overview':
        return stock_overview.layout
    elif pathname == '/overview':
        return overview.layout
    else:
        return overview.layout

if __name__ == '__main__':
    # Override pandas datareader with yfinance to fix Yahoo Finance API issues
    yf.pdr_override()
    app.run_server(debug=True)