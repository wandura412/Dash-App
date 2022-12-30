# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 11:27:01 2021

@author: Dasitha Wanduragala
"""
@app.callback(
    dash.dependencies.Output('line2', 'figure'),
    [dash.dependencies.Input('dtpick', 'start_date')],
    [dash.dependencies.Input('dtpick', 'end_date')])

def update_output_div(start_date,end_date):
    
    if start_date is None:
        fig2 = px.line( x =df['date'], y = df['total_deaths'],
               title='Total Deaths',
               color=df['location'])
        return fig2
    else:
        dfd=df[(df['date']>start_date) & (df['date'] < end_date)]
        fig2 = px.line( x =dfd['date'], y = dfd['total_deaths'],title='date range')    
    return fig2