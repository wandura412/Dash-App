# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 21:13:24 2021

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
dfw= df[df['location']== 'World']
Q1 = ['total_cases', 'new_cases', 'new_deaths', 'total_deaths']
Q3 = ['Sri Lanka', 'India','Bangladesh','South Africa','United States','Australia','Indonesia']
df['Test_to_detection'] = df['new_tests'] / df['new_cases']
dft=df[df['Test_to_detection'].notna()]


#SL
dfsl=df.drop(df[df['location']=='Sri Lanka'].index)

#SAAC
dfsac = df[df.location.isin(['Afghanistan', 'Bangladesh', 'Bhutan', 'India', 'Maldives', 'Nepal', 'Pakistan','Sri Lanka'])].groupby(['date'], as_index=False).sum().assign(location='SAC')  
dfsac = pd.concat([df, dfsac]) 

#RoW
df2=df[~df['location'].isin(['Sri Lanka'])]
dfw1=df2[df2['location']== 'World']




fig = px.line( x =dfw['date'], y = dfw['total_deaths'])
fig2 = px.line( x =dfw['date'], y = dfw[dfw['location']=='Sri Lanka']['total_deaths'])
fig3 = px.line( x =df['date'], y = df['Test_to_detection'])
fig4=px.scatter(x=df[df['location']=='Sri Lanka']['new_tests'] , y=df[df['location']=='Sri Lanka']['new_cases'])
             

app.layout = html.Div([ 
    
        html.H1("Covid-19 Dashboard", className='header1', id='head_id',
            style={'textAlign': 'center', 
                   'color':'#34495e'}),
        
        html.Div([
            
            #Part 01
            html.H3("Select appropriate values", className='header2', id='head2',
            style={'textAlign': 'left', 
                   'color':'#34495e'}),
            dcc.Dropdown(
                id='drop1',  
                options=[{'label': i, 'value': i} for i in Q1],style=dict(width='33%')),
            
           
            dcc.DatePickerRange(
                        id='dtpick',
                        min_date_allowed=df['date'].min(),                       
                        max_date_allowed=df['date'].max()),
            dcc.Graph(id='line', figure=fig),
            
            
            
            
            #Part 03
            html.H4("Select Appropirate date range and \n Country to view Test to detection Ratio"),
            dcc.Dropdown(
                id='drpdwn3',  
                options=[{'label': i, 'value': i} for i in Q3]              
                ),
            
            dcc.DatePickerRange(
                        id='dtpick3',
                        min_date_allowed='2020-04-21',                       
                        max_date_allowed=dft['date'].max(),
                        initial_visible_month='2020-04-21',
                        start_date_placeholder_text ='2020-04-21',
                        end_date_placeholder_text='2020-05-21' ),            
            dcc.Graph(id='line3', figure=fig3),
            
            
            
            
            #part 04
            dcc.DatePickerRange(
                        id='dtpick4',
                        min_date_allowed='2020-03-01',                       
                        max_date_allowed=dft['date'].max(),
                        initial_visible_month='2020-04-21',
                        start_date_placeholder_text ='2020-03-01',
                        end_date_placeholder_text='2020-05-21' ),
            
            html.Div(id='corr_val'),
            
            dcc.Graph(id='scatter',figure=fig4)
            
           
                        
                        
            
          ])
        
        ])



@app.callback(
    dash.dependencies.Output('line', 'figure'),
    [dash.dependencies.Input('dtpick', 'start_date')],
    [dash.dependencies.Input('dtpick', 'end_date')],
    [dash.dependencies.Input('drop1', 'value')])

def Q1(start_date,end_date,value):
    if value is None:
        fig = px.line(x =dfw['date'], y = dfw['total_deaths'],title='Worldwide Summary of variables')
        return fig
    else:
        dfd=dfw[(dfw['date']>start_date) & (dfw['date'] < end_date)]
        fig=px.line(x=dfd['date'], y= dfd[value],title='Worldwide Summary of variables')
        fig.update_yaxes(title=value)
        return fig
    

@app.callback(
    dash.dependencies.Output('line3', 'figure'),
    [dash.dependencies.Input('drpdwn3', 'value')],
    [dash.dependencies.Input('dtpick3', 'start_date')],
    [dash.dependencies.Input('dtpick3', 'end_date')])

def location_filter (location,std,end):
    
    u=(location and std and end)
    
    if u is None:
        fig3 = px.line( x =df['date'], y = df['Test_to_detection'],
               title='Total Deaths',
               color=df['location'])
        return fig3
    
    else:
         dfl=dft[dft['location']== location]
         dfd=dfl[(dfl['date']>std) & (dfl['date'] < end)]
         fig3 = px.line( x =dfd[dfd['location']==location]['date'], y = dfd[dfd['location']==location]['Test_to_detection'],
               title='Test to detection Ratio')
         fig3.update_yaxes(title=location)
         return fig3


@app.callback(
    dash.dependencies.Output('scatter', 'figure'),
    [dash.dependencies.Input('dtpick4', 'start_date')],
    [dash.dependencies.Input('dtpick4', 'end_date')])
    
def date_filter (std,end):
    
    u=( std and end)
    
    if u is None:
        fig4 = px.scatter(x =df[df['location']=='Sri Lanka']['new_tests'], y = df[df['location']=='Sri Lanka']['new_cases'],
               title='New tests vs New Cases')               
        return fig4
    
    else:
        dfd=df[(df['date']>std) & (df['date'] < end)]
        fig4 = px.scatter(x =dfd[dfd['location']=='Sri Lanka']['new_tests'], y = dfd[dfd['location']=='Sri Lanka']['new_cases'],
               title='New tests vs New Cases')               
        return fig4
    

@app.callback(
    dash.dependencies.Output('corr_val', 'children'),
    [dash.dependencies.Input('dtpick4', 'start_date')],
    [dash.dependencies.Input('dtpick4', 'end_date')])
    
def date_filter2 (std,end):
    
    u=( std and end)
    
    if u is None:
                      
        return 'Please Select Data'
    
    else:  
        dfd=df[(df['date']>std) & (df['date'] < end)]
        c=dfd['new_tests'].corr(dfd['new_cases'])              
        return u'correlation : {} '.format(c)
        
        
        
        

    


    
    
    



if __name__ == '__main__':
    app.run_server(port=8070, debug=False)