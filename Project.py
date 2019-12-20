#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 17:59:52 2019

@author: fahmi
"""

# Import package dash
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objects as go
import pandas as pd
df = pd.read_csv('gapminderDataFiveYear.csv')

# Create Menu List for Dropdown Component
year_options = []
for year in df['year'].unique():
    year_options.append({'label':str(year), 'value':year})
    
# Create App and Layout with dcc.Graph and dcc.Dropdown
app = dash.Dash()
app.layout = html.Div(children=[
        dcc.Graph(id='graph'),
        dcc.Dropdown(id = 'year-picker', options = year_options,
                     value = df['year'].min())
        ])
        
# Create callback Function to update dcc.Graph using dcc.Dropdown
@app.callback(Output('graph', 'figure'),
              [Input('year-picker','value')])

# Create update figure function
def update_figure(selected_year):
    # filter data for selected dropdown
    filtered_df = df[df['year'] == selected_year]
    
    traces = []
    
    for continent_name in filtered_df['continent'].unique():
        df_by_continent = filtered_df[filtered_df['continent'] == continent_name]
        traces.append(go.Scatter(
                x = df_by_continent['gdpPercap'],
                y = df_by_continent['lifeExp'],
                mode = 'markers',
                opacity = 0.7,
                marker = {'size':15},
                name = continent_name,
                text = df_by_continent['country']
                ))
    return {'data':traces,
            'layout':go.Layout(title = 'GDP per Capita againt Life Expectancy',
                               xaxis = {'title':'GDP per Cap', 'type':'log'},
                               yaxis = {'title':'Life Expectancy'})}
            
# App run server
if __name__ == '__main__':
    app.run_server()