import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from app import app

def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])

def get_header(app):
    header = dbc.Row(
        [
            html.Div(
                [
                    html.Img(
                        src=app.get_asset_url("logo.jpg"),
                        style={'height':'20%', 'width':'10%'},
                        className="logo",
                    ),
                    html.A(
                        html.Button("Learn More", id="learn-more-button"),
                        href="https://plot.ly/dash/pricing/",
                    ),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [html.H5("Aerial View")],
                        className="seven columns main-title",
                    ),
                    html.Div(
                        [
                            dcc.Link(
                                "Full View",
                                href="/dash-financial-report/full-view",
                                className="full-view-link",
                            )
                        ],
                        className="five columns",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header

def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Overview",
                href="/aerial-view/overview",
                className="tab first",
            ),
            dcc.Link(
                "Stock Overview",
                href="/aerial-view/stock-overview",
                className="tab",
            )
        ],
        className="row all-tabs",
    )
    return menu