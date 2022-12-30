# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 14:54:30 2021

@author: Dasitha Wanduragala
"""
import pandas as pd
import datetime 
import dash
from dash import dcc
from dash import html
#from dash.dependencies import Input, Output
import plotly.express as px
import json


df=pd.read_excel(r'C:\Users\Dasitha Wanduragala\Desktop\Data science\HNDDS\Visualization\Assignment\owid-covid-data.xlsx')
dfw= df[df['location']== 'World']

#df['month_year'] = pd.to_datetime(df['date']).dt.to_period('M') 
#df['MY_str'] = df['month_year'].dt.strftime('%m.%Y') 

