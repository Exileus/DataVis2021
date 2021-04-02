# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 16:19:47 2021

@author: Tiago
"""


import numpy as np
import pandas as pd
import plotly.graph_objects as go

## I am going to crate a radar chart to see how the three main variants of concern
# (Uk, BR, ZA) compare to each other, given COVID-19s baseline.

## Variables
# Transmissability (Higher, lower)
# Lethality - estimated at 2% baseline, but unknown
# Resistance to vaccines
# Number of mutations from original
# Percentage of global cases 

# Create this DF
categories = ['Transmissability','Lethality','Resistance','NrMutations','Percentage']
data_dict = {"Base":[0,0,0,0,0.25],
             "UK":[1,0,0,20,0.05],
             "BR":[0,0,0,15,0.15],
             "ZA":[0,0,1,25,0.12]}
cat_text = ["Lower","Base","Higher"]

df = pd.DataFrame(data=data_dict,index=categories)

#%%

#Trying a Radar Chart
#Problem: multiple scales 

categories = ['Transmissability','Lethality','Resistance','NrMutations','Percentage']

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
      r=[1, 5, 2, 2, 3],
      theta=categories,
      fill='toself',
      name='BR'
))
fig.add_trace(go.Scatterpolar(
      r=[4, 3, 2.5, 1, 2],
      theta=categories,
      fill='toself',
      name='UK'
))

fig.add_trace(go.Scatterpolar(
      r=[4, 4, 2.5, 4, 4],
      theta=categories,
      fill='toself',
      name='ZA'
))

fig.add_trace(go.Scatterpolar(
      r=[4, 3, 2.5, 1, 2],
      theta=categories,
      fill='toself',
      name='Baseline'
))

fig.update_layout(
    title="Title",
    polar=dict(
        radialaxis=dict(visible=True,type="category",range=["Less","Same","More"])),
        radialaxis2=dict(visible=True,type="category",range=["Less","Same","More"])),
    showlegend=True
)
fig.show()

#%%

fig = go.Figure(data=
    go.Parcoords(
        name = "one",
        line = dict(color = np.linspace(0,1,5),colorscale="rainbow."),
        dimensions = list([
            dict(range = [-1,1],
                 tickvals=[-1,0,1],
                 ticktext=cat_text,
                 label = categories[0], values = df.iloc[0]),
            dict(range = [-1,1],
                 tickvals=[-1,0,1],
                 ticktext=cat_text,
                 label = categories[1], values = df.iloc[1]),
            dict(range = [-1,1],
                 tickvals=[-1,0,1],
                 ticktext=cat_text,
                 label = categories[2], values = df.iloc[2]),
            dict(range = [0,25],
                 tickvals=[0,5,10,15,20,25],
                 label = categories[3], values = df.iloc[3]),
            dict(range = [0,1],
                 tickvals=[(i/10) for i in range(11)],
                 label = categories[4], values = df.iloc[4])
        ])
    )
)

fig.add_trace(go.Parcoords(name="Two",)) ## How do we add a legend / name to each line? 
## As it is, they are all plotted in the same data space. 

fig.update_layout(
    title="Characterizing the Variants of Concern",
    plot_bgcolor = 'white',
    paper_bgcolor = 'white',
    showlegend=True,
)

fig.show()

