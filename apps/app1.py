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

from app import app

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# yf.pdr_override() # <== that's all it takes :-)
# df = pdr.get_data_yahoo("AAPL", start="2017-01-01", end="2020-01-01")
# for col in df.columns:
#     df[col] = df[col].map(lambda x: '{0:.2f}'.format(x))
# df.reset_index(inplace=True)
# fig = px.line(df, x='Date', y = [col for col in df.columns if (col != 'Date' and col != 'Volume')])

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

layout = dbc.Container(html.Div([
    dcc.Store(id="ticker-info"),
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

    html.Div([

        dcc.Graph(id="polar-graph")
    ]),

    
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
    fig = px.line(df, x='Date', y = [col for col in df.columns if (col != 'Date' and col != 'Volume')])
    return fig

def get_ticker_info(ticker_name):
    try:
        data = yf.Ticker(ticker_name)
        return data.info
    except:
        return {}
    

@app.callback(
    [Output('line-graph', 'figure'),
    Output('ticker-info', 'data')],
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date'),
     Input('ticker_name', 'value')])
def update_output(start_date, end_date, ticker_name):
    fig = px.line()
    ticker_info = {}
    if start_date is not None:
        start_date = dt.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d')

    if end_date is not None:
        end_date = dt.strptime(re.split('T| ', end_date)[0], '%Y-%m-%d')

    if start_date and end_date and ticker_name:
        print (f"start date is: {start_date}")
        print (f"end date is: {end_date}")
        fig = get_period_data(ticker_name, start_date, end_date)
        fig.update_layout(transition_duration=500)

        ticker_info = get_ticker_info(ticker_name)
    return fig, ticker_info

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
    Output("polar-graph", 'figure'),
    [Input('ticker_name', 'value')]
)
def update_recommendations(ticker_name):
    try:
        data = yf.Ticker(ticker_name)
        recommends = data.recommendations

        value_counts = recommends['To Grade'].value_counts(dropna=True).to_dict()
        value_counts = {k: v for k, v in value_counts.items() if k}

        df = pd.DataFrame(dict(
                r = list(value_counts.values()), 
                theta = list(value_counts.keys())
            ))

        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        fig.update_traces(fill='toself')
        return fig
    except:
        return px.line_polar()