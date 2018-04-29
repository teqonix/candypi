#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from candytestplotly import generateCandyPlots
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html

def create_layout():
    candyPlotter = generateCandyPlots()
    print("Creating dash layout..")
    markdown_text = '''
# COBI Candy Tracker  
''' + str(datetime.datetime.now())
#'''
#This is a dashboard showing our candy usage in the Business Intelligence Department.  Refreshed every 5 minutes.'''

    end_date=datetime.datetime.now()
    start_date= (end_date + datetime.timedelta(days=-9))
    
    candyheatmap = candyPlotter.createCandyHeatmap(date_from=start_date, date_to=end_date, start_hour=6, end_hour=18)
    candyweeklyusage = candyPlotter.createCandyWeeklyBarChart(9)

    candyHourlyTrend = candyPlotter.fetchHourlyTrend()
    candyDayTrend = candyPlotter.fetchDailyTrend() 
    
    hourlyTrendImg = candyPlotter.getKPIArrow(candyHourlyTrend.get("Hourly Trend"))
    hourlyMarkdownText = ("""
## Hourly Trend:
**Summary:** """ + candyHourlyTrend.get("Hourly Trend") + """  
**Current Hour Count:** """ + str(candyHourlyTrend.get("Current Hour Candy Count")) + """  
**Last Hour Count:** """ + str(candyHourlyTrend.get("Lag Hour Candy Count"))
)
        
    dailyMarkdownText = ("""
## Daily Trend:
**Summary:** """ + candyDayTrend.get("Daily Trend") + """  
**Current Day Count:** """ + str(candyDayTrend.get("Current Day Candy Count")) + """  
**Previous Day Count:** """ + str(candyDayTrend.get("Lag Day Candy Count")) 
)
        
    dailyTrendImg = candyPlotter.getKPIArrow(candyDayTrend.get("Daily Trend"))
    
    dashboard_content = html.Div(children=[    
        html.Div(children=[
                   html.Div(children=[
                        dcc.Graph(
                                id='weekly candy activity'
                                ,figure = candyheatmap
                                )
                        ,dcc.Markdown(children=markdown_text)
                    ]
                    ,style={'width': '60%', 'display': 'inline-block'}
                    )
                 ,html.Div(children=[
                         html.Div(children=
                                     dcc.Graph(     
                                             id='heatmap',
                                             figure=candyweeklyusage
                                             )
                                    ) 
                    ],style={'width': '25%', 'display': 'inline-block'}) 
                 ,html.Div(children=[
                          html.Div(children=[
                                  dcc.Markdown(children=dailyMarkdownText),
                                  html.Img(src='data:image/png;base64,{}'.format(dailyTrendImg.decode()),style={'width': '150px', 'height': 'auto'})
                                  ])
                          ,html.Div(children=[
                                  dcc.Markdown(children=hourlyMarkdownText),
                                  html.Img(src='data:image/png;base64,{}'.format(hourlyTrendImg.decode()),style={'width': '150px', 'height': 'auto'})
                                  ])
                          ],style={'width': '15%', 'display': 'inline-block'})
                ])
    
    ])
    
    return dashboard_content
    
    #plot(candyheatmap, filename='candy-heatmap.html')
    #plot(candyweeklyusage, filename='candyweeklyusage.html')

app = dash.Dash()
#app.css.config.serve_locally = True
#app.scripts.config.serve_locally = True
app.layout = create_layout

if __name__ == '__main__':
    app.run_server()