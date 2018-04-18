#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 12:27:15 2018

@author: pi
"""
import plotly
import mysqlcandydb
import datetime 
from plotly.offline import plot
import plotly.graph_objs as go

dbconnection = mysqlcandydb
db = dbconnection.candydb.connectToDB()

where_clause = """WHERE 1=1
    AND cc.candyconsumption_date_ik BETWEEN STR_TO_DATE('20180501','%Y%m%d') AND STR_TO_DATE('20180601','%Y%m%d')
    AND HOUR(cc.logged_date) BETWEEN 6 AND 18"""

sqlstatement = """SELECT 
	SUM(cc.candycount_nb) AS CANDY_COUNT
	, DATE(cc.logged_date) AS reporting_date
	, DATE_FORMAT(cc.logged_date,'%a %b %d') AS day_of_week
	, dd.weekend
	, HOUR(cc.logged_date) AS logged_hour
FROM candydb.candycounts cc
	INNER JOIN candydb.date_dimension dd
		ON cc.candyconsumption_date_ik = dd.date_id
""" + where_clause + """
GROUP BY dd.day_of_week
	, dd.weekend
	, DATE(cc.logged_date)
	, HOUR(cc.logged_date)
ORDER BY cc.logged_date ASC"""

#print(sqlstatement)

with db.cursor() as cursor:
    cursor.execute(sqlstatement)
    exampleData = cursor.fetchall()

sqlstatement = """
SELECT DISTINCT 
    DATE_FORMAT(cc.logged_date,'%a %b %d') AS day_of_week
FROM candydb.candycounts cc
""" + where_clause + """
ORDER BY cc.logged_date ASC
"""

with db.cursor() as cursor:
    cursor.execute(sqlstatement)
    weekday_list = cursor.fetchall()

sqlstatement = """
SELECT DISTINCT 
    HOUR(cc.logged_date) AS logged_hour
FROM candydb.candycounts cc
""" + where_clause + """
ORDER BY logged_hour ASC
"""

with db.cursor() as cursor:
    cursor.execute(sqlstatement)
    hour_list = cursor.fetchall()

db.close()

reportHours = []
reportDaysOfWeek = []

for x in hour_list:
    reportHours.append(x["logged_hour"])
    #reportHours.update({"Hour": exampleData[x]["logged_hour"]})
#
#
for x in weekday_list:
    reportDaysOfWeek.append(x["day_of_week"])
#
#
#distnctReportHoursSet = sorted(set(reportHours),key=reportHours.index)
#distinctReportDaysOfWeek = sorted(set(reportDaysOfWeek), key=reportDaysOfWeek.index)
#print(reportHoursSet)
#print(reportDaysOfWeekSet)
#

heatmap_z = []

for hour in reportHours:
    new_heatmap_row = []
    for day in reportDaysOfWeek:
        candy_count = 0
        for dbdata in exampleData:
            if dbdata["day_of_week"] == day and dbdata["logged_hour"] == hour:
                print(dbdata)
                candy_count = int(dbdata["CANDY_COUNT"])
                print(candy_count)
                new_heatmap_row.append(candy_count)
    print(day)
    heatmap_z.append(list(new_heatmap_row))



data = [
    go.Heatmap(
        z=heatmap_z,
        x=reportDaysOfWeek,
        y=reportHours,
        colorscale='Viridis',
    )
]

layout = go.Layout(
    title='Candy Activity Over Time',
    xaxis = dict(ticks='', nticks=36),
    yaxis = dict(ticks='' )
)

fig = go.Figure(data=data, layout=layout)
plot(fig, filename='candy-heatmap.html')


    
for candyactivity in exampleData:
    print(candyactivity)