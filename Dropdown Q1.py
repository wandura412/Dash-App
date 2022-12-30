# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 03:04:43 2021

@author: Dasitha Wanduragala
"""
@app.callback(
    dash.dependencies.Output('line', 'figure'),
    [dash.dependencies.Input('drop1', 'value')])

def Q1(value):
    if value is None:
        fig = px.line(x =dfw['date'], y = dfw['total_deaths'],title='Worldwide Summary of variables')
        return fig
    else:
        fig=px.line(x=dfw['date'], y= dfw[value],title='Worldwide Summary of variables')
        fig.update_yaxes(title=value)
        return fig
    
 @app.callback(
    dash.dependencies.Output('line2', 'figure'),
    [dash.dependencies.Input('chk', 'value')])

def Q2(value):
    print(value)
    
    return value