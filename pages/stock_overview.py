import requests
import flask
import yfinance as yf
from pandas_datareader import data as pdr
import dash_table
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from datetime import datetime as dt
from datetime import date
import re
import plotly.express as px
import dash_table

from app import app
from utils import Header

layout = dbc.Container(html.Div([
    Header(app),
    dcc.Store(id="ticker-info"),
    dcc.Store(id="ticker-stock-prices"),
    dbc.Row([
        
        # Left Config
        dbc.Col([
            html.I("Please enter a ticker name"),
            html.Br(),
            dcc.Input(id="ticker_name", type="text", placeholder="", debounce=True),
            # html.Div(id="output"),
        ]),

        # Right Config
        dbc.Col([
            
            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=dt(1995, 8, 5),
                max_date_allowed=date.today(),
                initial_visible_month=dt(2017, 8, 5),
                end_date=date.today(),
                
    ),
        ])
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),


    # Left Graph
    html.Div([
        dcc.Graph(id="line-graph")
    ]),

    # html.Div(id="ticker-info-summary", style={'display':'none'}, children=[

    # ])
    html.Details([
        html.Summary('Business Summary'),
        html.Div(id="ticker-info-summary")
    ]),

    dbc.Row([
        dbc.Col([dcc.Graph(id="polar-graph-1")]),
        dbc.Col([dcc.Graph(id="polar-graph-2")])
        ]),
        

    html.Div([
        dash_table.DataTable(
            id='datatable-row-ids',
            columns=[{'name': 'Date', 'id': 'Date', 'deletable': True}, {'name': 'Open', 'id': 'Open', 'deletable': True}, {'name': 'High', 'id': 'High', 'deletable': True}, {'name': 'Low', 'id': 'Low', 'deletable': True}, {'name': 'Close', 'id': 'Close', 'deletable': True}, {'name': 'Adj Close', 'id': 'Adj Close', 'deletable': True}, {'name': 'Volume', 'id': 'Volume', 'deletable': True}],
            page_current=0,
            page_size=10,
            page_action='custom'
            )
    ])

    
#     # Right Graph
#     html.Div([
#         dcc.Graph(id='x-time-series'),
#         dcc.Graph(id='y-time-series'),
#     ], style={'display': 'inline-block', 'width': '49%'}),

    # Slider
    # html.Div(dcc.Slider(
    #     id='crossfilter-year--slider',
    #     min=df['Year'].min(),
    #     max=df['Year'].max(),
    #     value=df['Year'].max(),
    #     marks={str(year): str(year) for year in df['Year'].unique()},
    #     step=None
    # ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
]))


def get_period_data(ticker_name, start_date, end_date):
    # download dataframe
    df = pdr.get_data_yahoo(ticker_name, start=start_date, end=end_date)
    for col in df.columns:
        df[col] = df[col].map(lambda x: '{0:.2f}'.format(x))
    df.reset_index(inplace=True)
    fig = px.line(df, x='Date', y = [col for col in df.columns if (col != 'Date' and col != 'Volume')], title= f"Stock Price for {ticker_name.upper()}")
    return fig, df.to_dict('records')

def get_ticker_info(ticker_name):
    try:
        data = yf.Ticker(ticker_name)
        return data.info
    except:
        return {}
    

@app.callback(
    [Output('line-graph', 'figure'),
    Output('ticker-info', 'data'),
    Output('ticker-stock-prices', 'data')],
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date'),
     Input('ticker_name', 'value')])
def update_output(start_date, end_date, ticker_name):
    fig = px.line()
    ticker_info = {}
    stock_prices = {}
    if start_date is not None:
        start_date = dt.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d')

    if end_date is not None:
        end_date = dt.strptime(re.split('T| ', end_date)[0], '%Y-%m-%d')

    if start_date and end_date and ticker_name:
        print (f"start date is: {start_date}")
        print (f"end date is: {end_date}")
        fig, stock_prices = get_period_data(ticker_name, start_date, end_date)
        fig.update_layout(transition_duration=500)

        ticker_info = get_ticker_info(ticker_name)
    return fig, ticker_info, stock_prices

@app.callback(
    Output('ticker-info-summary', 'children'),
    [Input('ticker-info', 'data')]
)
def update_summary(data):
    if data:
        if 'longBusinessSummary' in data:
            return data['longBusinessSummary']
        else:
            return "Summary Not Available"
    else:
        return ""

@app.callback(
    [Output("polar-graph-1", 'figure'),
    Output("polar-graph-2", 'figure')],
    [Input('ticker_name', 'value')]
)
def update_recommendations(ticker_name):
    try:
        ticker_name = ticker_name.upper()
        data = yf.Ticker(ticker_name)
        recommends = data.recommendations

        one_month_recommends = recommends[recommends.index >= date.today() - pd.DateOffset(months=1)]
        three_month_recommends = recommends[recommends.index >= date.today() - pd.DateOffset(months=3)]

        one_month_value_counts = one_month_recommends['To Grade'].value_counts(dropna=True).to_dict()
        one_month_value_counts = {k: v for k, v in one_month_value_counts.items() if k}

        one_month_df = pd.DataFrame(dict(
                r = list(one_month_value_counts.values()), 
                theta = list(one_month_value_counts.keys())
            ))
    
        one_month_fig = px.line_polar(one_month_df, r='r', theta='theta', line_close=True, title= f'1 Month Recommendations for {ticker_name}')
        one_month_fig.update_traces(fill='toself')

        three_month_value_counts = three_month_recommends['To Grade'].value_counts(dropna=True).to_dict()
        three_month_value_counts = {k: v for k, v in three_month_value_counts.items() if k}

        three_month_df = pd.DataFrame(dict(
                r = list(three_month_value_counts.values()), 
                theta = list(three_month_value_counts.keys())
            ))
    
        three_month_fig = px.line_polar(three_month_df, r='r', theta='theta', line_close=True, title= f'3 Months Recommendations for {ticker_name}')
        three_month_fig.update_traces(fill='toself')


        return one_month_fig, three_month_fig
    except:
        return px.line_polar(), px.line_polar()

@app.callback(
    Output("datatable-row-ids", 'data'),
    [Input('ticker-stock-prices', 'data'),
     Input('datatable-row-ids', "page_current"),
     Input('datatable-row-ids', "page_size")]
)
def update_table(data, page_current, page_size):
    try:
        if data:
            return data[page_current*page_size:(page_current+ 1)*page_size]
    except:
        return []
