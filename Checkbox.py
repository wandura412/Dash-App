# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 19:45:17 2021

@author: Dasitha Wanduragala
"""

 dcc.Checklist(id='chk',
                  options=[
                          {'label': 'Sri Lanka', 'value': 'SL'},
                          {'label': '‘Rest of the world', 'value': 'RoW'},
                          {'label': 'Asia', 'value': 'Asia'},
                          {'label': 'SAARC', 'value': 'SAC'}
                                                               ])
 
 
 
@app.callback(
    dash.dependencies.Output('line2', 'figure'),
    [dash.dependencies.Input('chk', 'value')])

def Q2(value):
    if value==None:
         fig5=px.line(x=df['date'], y=df['new_cases'])
         return fig5
    
    elif value=='RoW':
        fig2 = px.line( x =dfw1['date'], y = dfw1['total_deaths'])
        print (value)
        return fig2   
    
    elif value=='Asia':
        fig3= px.line(x=df[df['location']=='Asia']['date'], y=df[df['location']=='Asia']['total_cases'])
        return fig3
    
    elif value=='SAC':
         fig4= px.line(x=dfsac[df['location']=='Asia']['date'], y=dfsac[df['location']=='Asia']['total_cases'])
         return fig4
     
    elif value=='SL':
         fig6=px.line( x =dfw['date'], y = dfw[dfw['location']=='Sri Lanka']['total_deaths'])
         return fig6