from dash import html, dcc
import dash_bootstrap_components as dbc

def Header(logo_url, learn_more_url="#", title="App Title", full_view_url="#", menu_items=None):
    if menu_items is None:
        menu_items = []
    return html.Div([get_header(logo_url, learn_more_url, title, full_view_url), html.Br(), get_menu(menu_items)])

def get_header(logo_url, learn_more_url, title, full_view_url):
    header = dbc.Row(
        [
            html.Div(
                [
                    html.Img(
                        src=logo_url,
                        style={'height':'20%', 'width':'10%'},
                        className="logo",
                    ),
                    html.A(
                        html.Button("Learn More", id="learn-more-button"),
                        href=learn_more_url,
                    ),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [html.H5(title)],
                        className="seven columns main-title",
                    ),
                    html.Div(
                        [
                            dcc.Link(
                                "Full View",
                                href=full_view_url,
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

def get_menu(menu_items):
    links = []
    for i, item in enumerate(menu_items):
        class_name = "tab first" if i == 0 else "tab"
        links.append(
            dcc.Link(
                item.get("label", ""),
                href=item.get("href", "#"),
                className=class_name,
            )
        )
    menu = html.Div(
        links,
        className="row all-tabs",
    )
    return menu