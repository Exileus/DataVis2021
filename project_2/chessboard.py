import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Define function to output an 8*8 dataframe based on a vector of coordinates.
def board_output(vector):
    brd = np.zeros((8, 8))
    for tup in vector:
        brd[tup] += 1

    return pd.DataFrame(brd)

def getChessboard(dimensions: int = 500, margin: int = 50):
    row = [0, 1] * 4
    boardmatrix = [row[::-1] if i % 2 == 1 else row for i in range(1, 9)]

    chessboard = go.Figure(
        layout=dict(
            margin=dict(l=margin, r=margin, t=margin, b=margin, pad=10),
            width=dimensions,
            height=dimensions,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            coloraxis_showscale=False,
            yaxis=dict(
                range=[0.5, 8.5], color="white", tickfont_size=12, fixedrange=True
            ),
            xaxis=dict(
                range=[-0.5, 7.5], color="white", tickfont_size=12, fixedrange=True
            ),
        )
    )
    chessboard.add_trace(
        go.Heatmap(
            x=["A", "B", "C", "D", "E", "F", "G", "H"],
            y=list(range(1, 9)),
            x0=0,
            y0=0,
            dx=0,
            z=boardmatrix,
            colorscale=["white", "black"],
            showscale=False,
        )
    )

    return chessboard


def getHeatmap(dataframe: pd.DataFrame):
    """DataFrame must have columns named:
    rows => 1 to 8
    letters => A to H
    freq => frequency"""
    heatmap = go.Scatter(
        x0=0,
        y0=0,
        dx=0,
        x=dataframe.letters,
        y=dataframe.rows,
        name="Name B",
        mode="markers",
        opacity=1,
        marker_symbol="square",
        marker_line_color="#c12917",
        marker_size=dataframe.freq,
        marker_sizeref=4,
        marker_sizemin=1,
        marker_sizemode="area",
        marker_opacity=1,
        marker_color="#c12917",
        # TODO
        hovertemplate="Test: %{y} - %{x}<br>number: 1<extra></extra>",
    )
    return heatmap