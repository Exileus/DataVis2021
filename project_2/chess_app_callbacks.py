# Because I have to learn Dash

# run with python chess_app.py and visit
# http://127.0.0.1:8050/ in your web browser.


# Imports
import dash
import ast

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output


import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from chessboard import getChessboard, getHeatmap
from styles import *

# Read the .csv file with the preprocessed data.
df_original = pd.read_csv(
    "chess_app.csv",
    dtype={"pawns": int, "knights": int, "bishops": int, "rooks": int, "queens": int},
    converters={"wKing_sqr": ast.literal_eval, "bKing_sqr": ast.literal_eval},
)

# Define function to output an 8*8 dataframe based on a vector of coordinates.
def board_output(vector):
    brd = np.zeros((8, 8))
    for tup in vector:
        brd[tup] += 1

    return pd.DataFrame(brd)

# Set stylesheets and app.
external_stylesheets = [dbc.themes.BOOTSTRAP]#["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Chess Analytics"





# Cols go inside rows. Rows first.
# every page has 12 columns. 
# width defines columns for each component.



# Defining app layout
# A simple app for simple purposes.
app.layout = html.Div([
    dbc.Row([dbc.Col(html.H3("Test Shit."),
                    width={'size':3,'offset':0}
                    ),
             dbc.Col(html.H3("More text shit"),
                     width={'size':3,'offset':0})]
            ),
    dbc.Row([dbc.Col(html.H3("The input over there is for choice of color ->"),
                     width={'size':4,'offset':0}
                     ),
             dbc.Col(dbc.ButtonGroup([dbc.Button("White",color="Light",n_clicks=0,id="white_color"),
                                      dbc.Button("Black",color="Dark",n_clicks=0,id="black_color")
                                      ])
                     )
             ]),
    dbc.Row([dbc.Col(html.H3("Elo range:"),
                     width={'size':4,'offset':0}),
             dbc.Col(dcc.Input(id="min_elo",value="800"),
                     width={'size':2}),
             dbc.Col(dcc.Input(id="max_elo",value="1700"),
                     width={'size':2})
        ]),
    dbc.Row([dbc.Col(dcc.RangeSlider(id="moves_slider",min=1,max=50,value=[8,30],step=1,
                                     pushable=1,allowCross=False,
                                     marks={i:str(i) for i in range(0,50,5)}
                                     ),
                     width={'size':10,'offset':1}
                     )
        ]),
    dbc.Row([dbc.Col(dcc.Graph(id="chessboard"),
                     width={'size':"Auto"})
        ]),
    dbc.Row([dbc.Col(html.H3("Total Number of Games: "),width={'size':'Auto'}),
             dbc.Col(html.H3(id="game_count"),
                     width={"size":"Auto"})
             ])
    ])


@app.callback(
    Output("chessboard","figure"),
    Output("game_count","children"),
    Input('white_color','n_clicks'),
    Input('black_color','n_clicks'),
    Input('min_elo','value'),
    Input('max_elo','value'),
    Input("moves_slider",'value')
    )
def update_chessboard(white_color,black_color,min_elo,max_elo,move_range):
    
    # Filters go here.
    dff = df_original[(df_original["avg_Elo"]>=int(min_elo)) &
                      (df_original["avg_Elo"]<=int(max_elo)) &
                      (df_original["moves"]>=int(move_range[0])) &
                      (df_original["moves"]<=int(move_range[-1]))
                      ]
    
    # Before further manipulation, get the number of games from the filtered dataframe.
    game_count = dff.shape[0]
    
    # Then retrieve the column of interest.
    if 'black_color' in dash.callback_context.triggered[0]['prop_id']:
        df = board_output(dff["bKing_sqr"])
    else:
        df = board_output(dff["wKing_sqr"])

    
    #Transform it for the heatmap.
    x_coords = ["A", "B", "C", "D", "E", "F", "G", "H"]
    replacer = {i+1: x for i, x in enumerate(x_coords)}
    df = df.stack().reset_index().rename(columns={"level_0":"rows","level_1":"cols",0:"freq"})
    df.iloc[:,0:2] = df.iloc[:,0:2].apply(lambda x:x+1)
    df["letters"] = df.cols.replace(replacer)
    chessboard = getChessboard()
    chessboard.add_trace(getHeatmap(dataframe=df))
    
    return chessboard,game_count



# Statring the dash app
if __name__ == "__main__":
    app.run_server(debug=True)

