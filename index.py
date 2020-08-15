import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import yfinance as yf

from app import app
from pages import stock_overview, overview


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/aerial-view/stock-overview':
        return stock_overview.layout
    else:
        return overview.layout

if __name__ == '__main__':
    yf.pdr_override()
    app.run_server(debug=True)