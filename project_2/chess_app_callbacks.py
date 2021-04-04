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
    converters={"wKing_sqr": ast.literal_eval, "bKing_sqr": ast.literal_eval,
                "wQueen_sqr": ast.literal_eval, "bQueen_sqr": ast.literal_eval,
                "wRook_sqr": ast.literal_eval, "bRook_sqr": ast.literal_eval,
                "wRook2_sqr": ast.literal_eval, "bRook2_sqr": ast.literal_eval,
                "wBishop_sqr": ast.literal_eval, "bBishop_sqr": ast.literal_eval,
                "wBishop2_sqr": ast.literal_eval, "bBishop2_sqr": ast.literal_eval,
                "wKnight_sqr": ast.literal_eval, "bKnight_sqr": ast.literal_eval,
                "wKnight2_sqr": ast.literal_eval, "bKnight2_sqr": ast.literal_eval}
)

# Define function to output an 8*8 dataframe based on a df and a list of column names to parse.
def board_output(df,col_list):
    brd = np.zeros((8, 8))
    
    for col_name in col_list:
        for tup in df[col_name]:
            if tup == (None,None):
                pass
            else:
                brd[tup] += 1

    return pd.DataFrame(brd)


# Define global variables for later.
g_color = "white_color"
g_piece = "King"

#Define a dictionary to be used to update the board with the correct columns.
color_piece_dict = cp_dict = {
    ("white_color","King"):["wKing_sqr"], ("black_color","King"): ["bKing_sqr"],
    ("white_color","Queen"):["wQueen_sqr"], ("black_color","Queen"): ["bQueen_sqr"],
    ("white_color","Rook"):["wRook_sqr","wRook2_sqr"], ("black_color","Rook"): ["bRook_sqr","bRook2_sqr"],
    ("white_color","Bishop"):["wBishop_sqr","wBishop2_sqr"], ("black_color","Bishop"): ["bBishop_sqr","bBishop2_sqr"],
    ("white_color","Knight"):["wKnight_sqr","wKnight2_sqr"], ("black_color","Knight"): ["bKnight_sqr","bKnight2_sqr"]
    }



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
             dbc.Col(dbc.ButtonGroup([dbc.Button("White",color="Secondary",n_clicks=0,id="white_color"),
                                      dbc.Button("Black",color="Secondary",n_clicks=0,id="black_color")
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
    dbc.Row([dbc.Col(dbc.ButtonGroup([dbc.Button("King",color="Secondary",n_clicks=0,id="King"),
                                      dbc.Button("Queen",color="Secondary",n_clicks=0,id="Queen"),
                                      dbc.Button("Rook",color="Secondary",n_clicks=0,id="Rook"),
                                      dbc.Button("Bishop",color="Secondary",n_clicks=0,id="Bishop"),
                                      dbc.Button("Knight",color="Secondary",n_clicks=0,id="Knight")
                                      ])
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
    Input('King','n_clicks'),
    Input('Queen','n_clicks'),
    Input('Rook','n_clicks'),
    Input('Bishop','n_clicks'),
    Input('Knight','n_clicks'),
    Input('min_elo','value'),
    Input('max_elo','value'),
    Input("moves_slider",'value')
    )
def update_chessboard(white_color,black_color,King,Queen,Rook,Bishop,Knight,min_elo,max_elo,move_range):
    
    # Filters go here.
    dff = df_original[(df_original["avg_Elo"]>=int(min_elo)) &
                      (df_original["avg_Elo"]<=int(max_elo)) &
                      (df_original["moves"]>=int(move_range[0])) &
                      (df_original["moves"]<=int(move_range[-1]))
                      ]
    
    # Before further manipulation, get the number of games from the filtered dataframe.
    game_count = dff.shape[0]
    
    # Then retrieve the column of interest.
    global g_color 
    global g_piece
    
    trigger_button = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if trigger_button in ["white_color","black_color"]:
        g_color = trigger_button
    if trigger_button in ["King","Queen","Rook","Bishop","Knight"]:
        g_piece = trigger_button
    
    df = board_output(dff,cp_dict[g_color,g_piece])

    
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

