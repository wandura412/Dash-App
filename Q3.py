# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 20:13:03 2021

@author: Dasitha Wanduragala
"""
@app.callback(
    dash.dependencies.Output('line3', 'figure'),
    [dash.dependencies.Input('drpdwn2', 'value')])

def location_filter (location):
    if location is None:
        fig3 = px.line( x =df['date'], y = df['Test_to_detection'],
               title='Total Deaths',
               color=df['location'])
        return fig3
    
    else:
         fig3 = px.line( x =df[df['location']==location]['date'], y = df[df['location']==location]['Test_to_detection'],
               title='Test to detection')
         print (location)
         return fig3
     
        
     
@app.callback(
    dash.dependencies.Output('line3', 'figure'),
    [dash.dependencies.Input('dtpick3', 'start_date')],
    [dash.dependencies.Input('dtpick3', 'end_date')],
    [dash.dependencies.Input('drpdwn3', 'value')])

def Q3(start_date,end_date,value): 
    
    value1 = str(value)
    dfd=dft[(dft['date']>start_date) & (dft['date'] < end_date)]
    dfl=dfd[dfd['location']== value1]
    
    if value is None and  start_date is None and (end_date is None):
        #fig3 = px.line(x =dfw['date'], y = dfw['total_deaths'],title='Worldwide Summary of variables')
        raise dash.exceptions.PreventUpdate
               
    else:       
        
        
      print( dfl['date'] )
      print(dfl['Test_to_detection'])
                 #title='Worldwide Summary of test to detection ratio')
        #fig3.update_yaxes(title=value1)
        #return fig3