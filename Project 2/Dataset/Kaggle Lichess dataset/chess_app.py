# Because I have to learn Dash 

# run with python chess_app.py and visit 
# http://127.0.0.1:8050/ in your web browser.


## Imports
import dash

import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import numpy as np
import plotly.express as px


# Read the .csv file with the preprocessed data.
df = pd.read_csv("chess_app.csv")

# Set stylesheets and app. 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)



# Placeholder.

fig = px.pie(df["victory_status"])
fig.show()

app.layout = html.Div(
    children=[html.H1(children="Hello Dean"),
              html.Div(children="""Dash: a web application...."""),
              dcc.Graph(id="example graph",figure=fig)
              ])



# Main script check, the usual.
if __name__ == '__main__':
    app.run_server(debug=True)
    