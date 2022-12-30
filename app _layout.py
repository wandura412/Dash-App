# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 23:06:24 2021

@author: Dasitha Wanduragala
"""
import pandas as pd
import dash
from dash import dcc
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
            html.H3("1.Line chart that tracks worldwide changes ", className='header2', id='head2',
            style={'textAlign': 'left', 
                   'color':'#34495e'}),
             
            dcc.Graph(id='line', figure=fig),
            html.Br(),
            
            html.Div([          
                           
            html.Label(['Select Case Type'], style={'font-weight': 'bold', "text-align": "center"}),
            html.Div([
            dcc.Dropdown(
                id='drop1',  
                options=[{'label': i, 'value': i} for i in Q1])],
                style=dict(width='50%')),
            
           
            html.Label(['Pick Required Dates'], style={'font-weight': 'bold', "text-align": "center"}),
            dcc.DatePickerRange(
                        id='dtpick',
                        min_date_allowed=df['date'].min(),                       
                        max_date_allowed=df['date'].max(),
                        style=dict(width='50%')),
            
            
            ],style={'display': 'flex', 'flex-direction': 'row'}),
            
           
            #Part 02
            
            html.Div([
            html.H3("3.Multiple  Line chart to showing the Variation of several factors", className='header2', id='head2',
            style={'textAlign': 'left', 
                   'color':'#34495e'}),
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
                          ,style={'display': 'flex', 'flex-direction': 'row'}),
    
            
            ],style={'margin-top': '5vw'}),
            
            
            
            
            
            
            
            
            
            #Part 03
            html.Div([
            html.H3("3. Line chart to showing the daily test_to_detection ratio", className='header3', id='head3',
            style={'textAlign': 'left', 
                   'color':'#34495e'}),
            
            dcc.Graph(id='line3', figure=fig3),
            html.Br(),
            
            html.Div([
            html.Label(['Select Case Type'], style={'font-weight': 'bold', "text-align": "center"}),
            
            html.Div([
            dcc.Dropdown(
                id='drpdwn3',  
                options=[{'label': i, 'value': i} for i in Q3])],              
                style=dict(width='50%')),
            
                
            html.Label(['Pick Required Dates'], style={'font-weight': 'bold', "text-align": "center"}),
            dcc.DatePickerRange(
                        id='dtpick3',
                        min_date_allowed='2020-04-21',                       
                        max_date_allowed=dft['date'].max(),
                        initial_visible_month='2020-04-21',
                        start_date_placeholder_text ='2020-04-21',
                        end_date_placeholder_text='2020-05-21' ,style=dict(width='50%')),            
           
            
            ],style={'display': 'flex', 'flex-direction': 'row'})
            
            ],style={'margin-top': '5vw'}),
            
            
            
            
            
            
            
            #part 04
            html.Div([
            html.H3("4. A scatter plot to show the relationship between Tests and new cases only for Sri Lanka", className='header4', id='head4',
            style={'textAlign': 'left', 
                   'color':'#34495e'}),
            dcc.Graph(id='scatter',figure=fig4),
         
            html.Label(['Pick Required Dates'], style={'font-weight': 'bold', "text-align": "center"}),
            html.Div(id='corr_val'),
            dcc.DatePickerRange(
                        id='dtpick4',
                        min_date_allowed='2020-03-01',                       
                        max_date_allowed=dft['date'].max(),
                        initial_visible_month='2020-04-21',
                        start_date_placeholder_text ='2020-03-01',
                        end_date_placeholder_text='2020-05-21',style=dict(width='25%'))
            
            
           
            
           ],style={'margin-top': '5vw'})
                        
                        
            
          ])
        
        ])

if __name__ == '__main__':
    app.run_server(port=8080, debug=False)
