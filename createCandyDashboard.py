#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from plotly.offline import plot
from candytestplotly import generateCandyPlots
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

markdown_text = '''
# COBI Candy Tracker
This is a dashboard showing our candy usage in the Business Intelligence Department.  Refreshed every 5 minutes.
'''

if __name__ == '__main__':
    candyPlotter = generateCandyPlots()

    start_date=datetime.date(2018,4,18)
    end_date=datetime.date(2018,4,26)
    
    candyheatmap = candyPlotter.createCandyHeatmap(date_from=start_date, date_to=end_date, start_hour=6, end_hour=18)
    candyweeklyusage = candyPlotter.createCandyWeeklyBarChart(4)
    
    app.layout = html.Div(children=[
    dcc.Markdown(children=markdown_text),

    html.Div(children=
             dcc.Graph(     
                     id='heatmap',
                     figure=candyheatmap
                     )
            ,style={'height': '360px', 'width': '70%', 'display': 'inline-block'}
            )
    ,html.Div(children=[
            dcc.Graph(
                    id='weekly candy activity'
                    ,figure = candyweeklyusage
                    )
            ],style={'height': '360px', 'width': '29%', 'display': 'inline-block'})
    
    ]) 
    
    #plot(candyheatmap, filename='candy-heatmap.html')
    #plot(candyweeklyusage, filename='candyweeklyusage.html')
    app.run_server()