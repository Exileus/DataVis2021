# Because I have to learn Dash


# run with python chess_app.py and visit

# http://127.0.0.1:8050/ in your web browser.


# Import all the libraries

import dash

import ast


import dash_core_components as dcc

import dash_html_components as html

import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State


import pandas as pd

import numpy as np

import plotly.express as px


# Read the .csv file with the preprocessed data.

df = pd.read_csv("/Users/rupeshbaradi/DataVis2021/DataVis2021/Project 2/Dataset/Kaggle Lichess dataset/chess_app.csv", dtype={"pawns": int, "knights": int, "bishops": int,

                                                                                                                              "rooks": int, "queens": int},

                 converters={"wKing_sqr": ast.literal_eval, "bKing_sqr": ast.literal_eval})


# Define function to output an 8*8 dataframe based on a vector of coordinates.


def board_output(vector):


brd = np.zeros((8, 8))

for tup in vector:

brd[tup] += 1


return pd.DataFrame(brd)


# Optionally, produces a .csv of such a dataframe.

# board_output(wKing_sqr).to_csv("wKing_Heatmap.csv")

df_king = board_output(df["wKing_sqr"])

# passing the data for heatmap

fig = px.imshow(df_king, color_continuous_scale=px.colors.sequential.Burgyl, labels=dict(

    x="", y="", color="No of checkmates"),

    x=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],

    y=['1', '2', '3', '4', '5', '6', '7', '8'])

#logo in header

PLOTLY_LOGO = "/assets/chess-app.jpg"

# Set stylesheets and app.

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "Chess Analytics"


# Defining app layout

nav_item = dbc.NavItem(dbc.NavLink("Link", href="#"))


# make a reuseable dropdown for the different examples

dropdown = dbc.DropdownMenu(

    children=[

        dbc.DropdownMenuItem("Entry 1"),

        dbc.DropdownMenuItem("Entry 2"),

        dbc.DropdownMenuItem(divider=True),

        dbc.DropdownMenuItem("Entry 3"),

    ],

    nav=True,

    in_navbar=True,

    label="Menu",

)

# this example that adds a logo to the navbar brand

logo = dbc.Navbar(

    dbc.Container(

        [

            html.A(

                # Use row and col to control vertical alignment of logo / brand

                dbc.Row(

                    [

                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),

                        dbc.Col(dbc.NavbarBrand(

                            "Chess Analytics", className="ml-2")),

                    ],

                    align="center",

                    no_gutters=True,

                ),

                href="https://plot.ly",

            ),

            dbc.NavbarToggler(id="navbar-toggler2"),

            dbc.Collapse(

                dbc.Nav(

                    [nav_item, dropdown], className="ml-auto", navbar=True

                ),

                id="navbar-collapse2",

                navbar=True,

            ),

        ]

    ),

    color="#950740",

    dark=True,

    className="mb-5",

)

AppFunction = html.Div([

    html.Div([

        html.Label('Please choose the selection'),

        html.Label('Victory By'),

        dcc.Tabs([

            dcc.Tab(label='Check Mate', children=[

                html.Div(

                    [html.P([html.Br()])]),

                html.Div(

                    [html.P([html.Br()])]),

                html.Div([

                    dbc.Button("Position of king checkmated", outline=True,

                               color="success", className="mr-1"),

                ])  # classname for buttons

            ]),

            dcc.Tab(label='Resign', children=[

                html.Div(

                    [html.P([html.Br()])]),

                html.Div(

                    [html.P([html.Br()])]),

                html.Div(

                    [

                        dbc.Button("Position of king checkmated when resigned", outline=True,

                                   color="warning", className="mr-1"),

                    ]

                )

            ]),

            dcc.Tab(label='Draw', children=[

            ]),

        ])

    ])

])


HeatMap = dcc.Graph(id="kings_chess", figure=fig)


app.layout = html.Div([logo,

                       dbc.Row([

                           dbc.Col(AppFunction, width=6),

                           dbc.Col(HeatMap, width=6),

                       ])

                       ], className='container'

                      )


# we use a callback to toggle the collapse on small screens


def toggle_navbar_collapse(n, is_open):


if n:

return not is_open

return is_open


# the same function (toggle_navbar_collapse) is used in all three callbacks

for i in [1, 2, 3]:

app.callback(

    Output(f"navbar-collapse{i}", "is_open"),

    [Input(f"navbar-toggler{i}", "n_clicks")],

    [State(f"navbar-collapse{i}", "is_open")],

)(toggle_navbar_collapse)

# Statring the dash app

if __name__ == '__main__':

app.run_server(debug=True, port=8050)


''' 

row = html.Div([ 

dbc.Row([ 

dbc.Col(html.Div("One of three columns")), 

dbc.Col(html.Div("One of three columns")), 

]), 

] 

) 

'''


''' 

# producing heatmap with imshow(should consider changing it with go) 

fig = px.imshow(df_king, color_continuous_scale=px.colors.sequential.Burgyl, labels=dict( 

x="", y="", color="No of checkmates"), 

x=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'], 

y=['1', '2', '3', '4', '5', '6', '7', '8']) 

 
 

# Defining app layout 

app.layout = html.Div([ 

 
 

html.Div([ 

html.H2("Chess App"), 

html.Img(src="/assets/chess-app.jpg"), 

], className="banner"), 

 
 

html.Div([ 

html.Div([ 

html.Label('Please choose the selection'), 

html.Label('Victory By'), 

dcc.Tabs([ 

dcc.Tab(label='Check Mate', children=[ 

html.Div( 

[html.P([html.Br()])]), 

html.Div( 

[html.P([html.Br()])]), 

html.Div([ 

dbc.Button("Position of king checkmated", outline=True, 

color="success", className="mr-1"), 

], className="layout") # classname for buttons 

]), 

dcc.Tab(label='Resign', children=[ 

html.Div( 

[html.P([html.Br()])]), 

html.Div( 

[html.P([html.Br()])]), 

html.Div( 

[ 

dbc.Button("Position of king checkmated when resigned", outline=True, 

color="warning", className="mr-1"), 

] 

) 

], className='layout'), 

dcc.Tab(label='Draw', children=[ 

]), 

]) 

], className="layout"), 

html.Div([ 

dcc.Graph(id="kings_chess", figure=fig) 

], className="layout"), 

 
 

], className="row"), 

]) 

# Statring the dash app 

if __name__ == '__main__': 

app.run_server(debug=True) 

'''

''' 

app.layout = html.Div([ 

html.Label('Range Slider'), 

dcc.RangeSlider( 

id="rangeslider", 

marks={i: 'label {}'.format(i) for i in range(0, 5)}, 

min=0, 

max=5, 

value=[0, 1], 

step=1 

), 

]) 

'''

''' 

fig = px.imshow(df_test, color_continuous_scale=px.colors.sequential.Burgyl, labels=dict( 

x="", y="", color="No of checkmates"), 

x=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'], 

y=['1', '2', '3', '4', '5', '6', '7', '8']) 

'''

''' 

html.Div([ 

html.Button( 

html.Img(src='/assets/knight-app.jpg'), id='btn-nclicks-1', n_clicks=0), 

html.Button( 

html.Img(src='/assets/king-app.jpg'), id='btn-nclicks-2', n_clicks=0), 

html.Button( 

html.Img(src='/assets/queen-app.jpg'), id='btn-nclicks-3', n_clicks=0), 

html.Div( 

[html.P([html.Br()])]), 

html.Button( 

html.Img(src='/assets/pawn-app.jpg'), id='btn-nclicks-4', n_clicks=0), 

html.Button( 

html.Img(src='/assets/rook-app.jpg'), id='btn-nclicks-5', n_clicks=0), 

html.Button( 

html.Img(src='/assets/bishop-app.jpg'), id='btn-nclicks-6', n_clicks=0), 

html.Div(id='container-button-timestamp') 

], className="chessimages") 

'''

''' 

html.Button( 

'button 1', id='btn-nclicks-1', n_clicks=0), 

html.Button( 

'button 2', id='btn-nclicks-2', n_clicks=0), 

html.Button( 

'button 3', id='btn-nclicks-3', n_clicks=0), 

html.Div(id='container-button-timestamp') 

'''

''' 

jumbotron = dbc.Jumbotron( 

[ 

html.H1("Victory By", className="display-3"), 

html.Div([ 

html.Label('Please choose the selection'), 

html.Label('Victory By'), 

dcc.Tabs([ 

dcc.Tab(label='Check Mate', children=[ 

html.Div( 

[html.P([html.Br()])]), 

html.Div( 

[html.P([html.Br()])]), 

html.Div([ 

dbc.Button("Position of king checkmated", outline=True, 

color="success", className="mr-1"), 

]) # classname for buttons 

]), 

dcc.Tab(label='Resign', children=[ 

html.Div( 

[html.P([html.Br()])]), 

html.Div( 

[html.P([html.Br()])]), 

html.Div( 

[ 

dbc.Button("Position of king checkmated when resigned", outline=True, 

color="warning", className="mr-1"), 

] 

) 

]), 

dcc.Tab(label='Draw', children=[ 

]), 

]) 

]), 

] 

) 

'''
