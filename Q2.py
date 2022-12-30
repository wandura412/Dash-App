# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 02:40:57 2021

@author: Dasitha Wanduragala
"""
import pandas as pd
from datetime import date
import dash
from dash import dcc
import numpy as np
from dash import html
#from dash.dependencies import Input, Output
import plotly.express as px
import json

app = dash.Dash(__name__)


df=pd.read_excel(r'C:\Users\Dasitha Wanduragala\Desktop\Data science\HNDDS\Visualization\Assignment\owid-covid-data.xlsx')
Q1 = ['total_cases', 'new_cases', 'new_deaths', 'total_deaths']


#SAAC
dfsac = df[df.location.isin(['Afghanistan', 'Bangladesh', 'Bhutan', 'India', 'Maldives', 'Nepal', 'Pakistan','Sri Lanka'])].groupby(['date'], as_index=False).sum().assign(location='SAC')  


#RoW
df2=df[~df['location'].isin(['Sri Lanka'])]
dfw1=df2[df2['location']== 'World']
dfw1['location'] = dfw1['location'].replace({'World': 'RoW'})

#Asia
dfasia=df[df['location']=='Asia']

#SL
dfsl=df[df['location']=='Sri Lanka']

#Combined
df_combined =pd.concat([dfsac,dfw1,dfasia,dfsl])

fig2 = px.line( x =df[df['location']== 'Sri Lanka']['date'], y = df[df['location']== 'Sri Lanka']['total_deaths'],title='Total Deaths')
               
               

app.layout = html.Div([     
    dcc.Graph(id='line2',figure=fig2,style=dict(width='100%')),
    
    html.Br(),  
    
    html.Div([
     html.Label(['Select Case Type'], style={'font-weight': 'bold', "text-align": "center"}),
     html.Div([
     dcc.Dropdown(
                id='drop01',  
                options=[ {'label': 'Total Cases', 'value': 'total_cases'},
                          {'label': 'New Cases', 'value': 'new_cases'},
                          {'label': 'New Deaths', 'value': 'new_deaths'},
                          {'label': 'Total Deaths', 'value': 'total_deaths'}]
                
                )],style=dict(width='25%')),
    
    html.Label(['Pick Required Dates'], style={'font-weight': 'bold', "text-align": "center"}),
    dcc.DatePickerRange(
                        id='dtpick01',
                        min_date_allowed=df['date'].min(),                       
                        max_date_allowed=df['date'].max(),style=dict(width='25%')),
    
    html.Label(['Select Location'], style={'font-weight': 'bold', "text-align": "center"}),
    dcc.Checklist(id='chk',
                  options=[
                          {'label': '‘Rest of the world', 'value': 'RoW'},
                          {'label': 'Asia', 'value': 'Asia'},
                          {'label': 'SAARC', 'value': 'SAC'}
                                                               ],style=dict(width='25%')),
    
    html.Label(['Select Aggregation Method'], style={'font-weight': 'bold', "text-align": "center"}),
    html.Div([
    dcc.Dropdown(
                id='drop02',  
                options=[ #{'label': 'Daily', 'value': 'daily'},
                          {'label': 'Weekly Average', 'value': 'w'},
                          {'label': 'Monthly Average', 'value': 'm'},
                          {'label': '7 Day rolling Average', 'value': '7'},
                          {'label': '14 Day rolling Average', 'value': '14'}])],style=dict(width='25%'))]
        ,style={'display': 'flex', 'flex-direction': 'row'})
    
    
    ])

@app.callback(
    dash.dependencies.Output('line2', 'figure'),
    [dash.dependencies.Input('dtpick01', 'start_date')],
    [dash.dependencies.Input('dtpick01', 'end_date')],
    [dash.dependencies.Input('chk', 'value')],
    [dash.dependencies.Input('drop01', 'value')],
    [dash.dependencies.Input('drop02', 'value')])

def Q2 (std,end,chkval,drpval,drpval2):
    
    
    u=(std and end and chkval and drpval and drpval2)

    
    if u is None:
        fig2 = px.line(x =df[df['location']== 'Sri Lanka']['date'],
                       y = df[df['location']== 'Sri Lanka']['total_deaths'],
                       title='World Wide Changes')
        return fig2
    
    else:
        dfd=df_combined[(df_combined['date']>std) & (df_combined['date'] < end)]
        dfgrp=dfd[['date','location','total_cases', 'new_cases', 'new_deaths', 'total_deaths']]
        dfgrp['date'] = pd.to_datetime(dfgrp['date'])
        drpval2_str=str(drpval2)
        if drpval2_str ==('m' or 'w'):
            dfgrp=dfgrp.groupby([
                           pd.Grouper(key='date', freq=drpval2_str),
                           pd.Grouper('location')]).mean().reset_index()
            #return dfgrp
            
        else:
           drpval2_int=int(drpval2)
           dfgrp[['total_cases', 'new_cases', 'new_deaths', 'total_deaths']]=dfgrp[['total_cases', 'new_cases', 'new_deaths', 'total_deaths']].rolling(drpval2_int).mean()
            
            #return dfgrp
        
        
        
            
    fig2 = px.line( x=dfgrp[dfgrp['location']== 'Sri Lanka']['date'], y=dfgrp[dfgrp['location']=='Sri Lanka'][drpval])
    for i in chkval:
        fig2.add_scatter(x=dfgrp[dfgrp['location']== i]['date'] ,y=dfgrp[dfgrp['location']==i][drpval],name=i )
            
        #fig2.update_xaxes(title_text='Date')
        #fig2.update_yaxes(title_text=drpval)
    fig2.update_layout(
        title="World Wide Changes",
        xaxis_title="Date",
        yaxis_title= drpval,
        legend_title="Location")
    return fig2
 
if __name__ == '__main__':
    app.run_server(port=8070, debug=False)       
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    