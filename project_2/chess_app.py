# Because I have to learn Dash

# run with python chess_app.py and visit
# http://127.0.0.1:8050/ in your web browser.


# Imports
import dash
import ast

import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import numpy as np
import plotly.express as px

# Read the .csv file with the preprocessed data.
df = pd.read_csv("chess_app.csv", dtype={"pawns": int, "knights": int, "bishops": int,
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

# Set stylesheets and app.
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Chess Analytics"

# producing heatmap with imshow(should consider changing it with go)
fig = px.imshow(df_king, color_continuous_scale=px.colors.sequential.Burgyl, labels=dict(
    x="", y="", color="No of checkmates"),
    x=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
    y=['1', '2', '3', '4', '5', '6', '7', '8'][::-1])

# Defining app layout
app.layout = html.Div([

    html.Div([
        html.H2("Chess App"),
        html.Img(src="/assets/chess-app.jpg"),
    ], className="banner"),

    html.Div([
        html.Div([
            html.Label('Range Slider'),
            dcc.RangeSlider(
                id="rangeslider",
                marks={i: 'label {}'.format(i) for i in range(0, 5)},
                min=0,
                max=5,
                value=[0, 1],
                step=1)
        ], className="five columns"),
        html.Div([
            dcc.Graph(id="Victory Status", figure=fig)
        ], className=" six columns"),

    ], className="row"),
])
# Statring the dash app
if __name__ == '__main__':
    app.run_server(debug=True)
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
