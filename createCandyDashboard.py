#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from candytestplotly import generateCandyPlots
from generatesampledata import candySampleData
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def getDashboardContent(start_date, end_date):
    contentCandyPlotter = generateCandyPlots()
    candyheatmap = contentCandyPlotter.createCandyHeatmap(date_from=start_date, date_to=end_date, start_hour=6, end_hour=18)
    candyweeklyusage = contentCandyPlotter.createCandyWeeklyBarChart(9)

    candyHourlyTrend = contentCandyPlotter.fetchHourlyTrend()
    candyDayTrend = contentCandyPlotter.fetchDailyTrend()
    
    hourlyTrendImg = contentCandyPlotter.getKPIArrow(candyHourlyTrend.get("Hourly Trend"))
    hourlyMarkdownText = ("""
## Hourly Trend:
**Summary:** """ + candyHourlyTrend.get("Hourly Trend") + """  
**Current Hour Count:** """ + str(candyHourlyTrend.get("Current Hour Candy Count")) + """  
**Last Hour Count:** """ + str(candyHourlyTrend.get("Lag Hour Candy Count"))
    )
    
                
    dailyTrendImg = contentCandyPlotter.getKPIArrow(candyDayTrend.get("Daily Trend"))
    dailyMarkdownText = ("""
## Daily Trend:
**Summary:** """ + candyDayTrend.get("Daily Trend") + """  
**Current Day Count:** """ + str(candyDayTrend.get("Current Day Candy Count")) + """  
**Previous Day Count:** """ + str(candyDayTrend.get("Lag Day Candy Count")) 
    )
    
    return [candyHourlyTrend #0
            , hourlyTrendImg #1
            , hourlyMarkdownText #2
            , candyDayTrend #3
            , dailyTrendImg #4 
            , dailyMarkdownText #5 
            , candyheatmap #6 
            , candyweeklyusage #7 
            ]
    

def create_layout():
    print("Creating dash layout..")
    markdown_text = '''
# COBI Candy Tracker  
Last refreshed on: ''' + str(datetime.datetime.now())
#'''
#This is a dashboard showing our candy usage in the Business Intelligence Department.  Refreshed every 5 minutes.'''

    end_date=datetime.datetime.now()
    start_date= (end_date + datetime.timedelta(days=-9))

    dashboardData = getDashboardContent(start_date, end_date)
        
    dashboard_content = html.Div(children=[    
        html.Div(children=[
                   html.Div(children=[
                        dcc.Graph(
                                id='heatmap_chart'
                                ,figure = dashboardData[6]
                                )
                        ,dcc.Markdown(id='welcome_text'
                                      ,children=markdown_text
                                )
                    ]
                    ,style={'width': '60%', 'display': 'inline-block'}
                    )
                 ,html.Div(children=[
                         html.Div(children=
                                     dcc.Graph(     
                                             id='bar_chart',
                                             figure=dashboardData[7]
                                             )
                                    ) 
                    ],style={'width': '25%', 'display': 'inline-block'}) 
                 ,html.Div(children=[
                          html.Div(id='daily_trend',children=[
                                  dcc.Markdown(children=dashboardData[5]), #daily markdown text
                                  html.Img(src='data:image/png;base64,{}'.format(dashboardData[4].decode()),style={'width': '150px', 'height': 'auto'})
                                  ])
                          ,html.Div(id='hourly_trend',children=[
                                  dcc.Markdown(children=dashboardData[2]), #hourly markdown text
                                  html.Img(src='data:image/png;base64,{}'.format(dashboardData[1].decode()),style={'width': '150px', 'height': 'auto'})
                                  ])
                          ],style={'width': '15%', 'display': 'inline-block'})
                ,dcc.Interval(
                            id='interval-component',
                            interval=15*1000, # in milliseconds
                            n_intervals=0
                )
        ])
    
    ])
    
    return dashboard_content
    
    #plot(candyheatmap, filename='candy-heatmap.html')
    #plot(candyweeklyusage, filename='candyweeklyusage.html')

def setup_app():
    app = dash.Dash(__name__)
    app.css.config.serve_locally = True
    app.scripts.config.serve_locally = True
    app.layout = create_layout

    @app.callback(Output('welcome_text', 'children'),
                  [Input('interval-component', 'n_intervals')])
    def update_welcome_text(n):
        new_welcome_text = '''
    # COBI Candy Tracker  
    Last refreshed on: ''' + str(datetime.datetime.now()) + ''' for interval ''' + str(n)
        return [new_welcome_text]

    @app.callback(Output('heatmap_chart', 'figure'),
                  [Input('interval-component', 'n_intervals')])
    def update_heatmap(n):
        end_date=datetime.datetime.now()
        start_date= (end_date + datetime.timedelta(days=-9)) 
        new_heatmap = getDashboardContent(start_date, end_date)
        return new_heatmap[6]


    @app.callback(Output('bar_chart', 'figure'),
                  [Input('interval-component', 'n_intervals')])
    def update_bar_chart(n):
        end_date=datetime.datetime.now()
        start_date= (end_date + datetime.timedelta(days=-9)) 
        new_barchart = getDashboardContent(start_date, end_date)
        return new_barchart[7]

    @app.callback(Output('hourly_trend', 'children'),
                  [Input('interval-component', 'n_intervals')])
    def update_daily_trend(n):
        end_date=datetime.datetime.now()
        start_date= (end_date + datetime.timedelta(days=-9)) 
        trend_data = getDashboardContent(start_date, end_date)
        daily_trend = [ dcc.Markdown(children=trend_data[5]), #hourly markdown text
                         html.Img(src='data:image/png;base64,{}'.format(trend_data[4].decode()),style={'width': '125px', 'height': 'auto'})
                        ]
        return daily_trend

    @app.callback(Output('daily_trend', 'children'),
                  [Input('interval-component', 'n_intervals')])
    def update_hourly_trend(n):
        end_date=datetime.datetime.now()
        start_date= (end_date + datetime.timedelta(days=-9))
        trend_data = getDashboardContent(start_date, end_date)
        hourly_trend = [ dcc.Markdown(children=trend_data[2]), #hourly markdown text
                         html.Img(src='data:image/png;base64,{}'.format(trend_data[1].decode()),style={'width': '125px', 'height': 'auto'})
                        ]
        
        #data_generator = candySampleData()
        #data_generator.createExampleData(45, 125, 20180315)
        return hourly_trend
    app.run_server()

if __name__ == '__main__':
    ##app.run_server()
    setup_app()