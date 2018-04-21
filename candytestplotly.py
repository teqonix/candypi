#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import plotly
import mysqlcandydb
import datetime
import sys
from plotly.offline import plot
import plotly.graph_objs as go

dbconnection = mysqlcandydb
db = dbconnection.candydb.connectToDB()
y_lowerbound = 6
y_upperbound = 18
date_from = datetime.date(2018,5,5)
date_to = datetime.date(2018,5,10)
date_difference = date_to - date_from

where_clause = """WHERE 1=1
    AND cc.candyconsumption_date_ik BETWEEN STR_TO_DATE('""" + date_from.strftime('%Y%m%d') + """','%Y%m%d') AND STR_TO_DATE('""" + date_to.strftime('%Y%m%d') + """','%Y%m%d')
    AND HOUR(cc.logged_date) BETWEEN """ + str(y_lowerbound) + """ AND """ + str(y_upperbound)

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

print(sqlstatement)

with db.cursor() as cursor:
    cursor.execute(sqlstatement)
    exampleData = cursor.fetchall()

sqlstatement = """
SELECT DISTINCT 
    DATE(cc.logged_date) AS reporting_date    
    ,DATE_FORMAT(cc.logged_date,'%a %b %d') AS day_of_week    
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
#    hour_list = cursor.fetchall()

hour_list = range(y_lowerbound,y_upperbound)

db.close()

reportHours = []
reportDaysOfWeek = []

for x in hour_list:
    reportHours.append(x)
    #reportHours.update({"Hour": exampleData[x]["logged_hour"]})
#
#
for x in weekday_list:
    reportDaysOfWeek.append([x["reporting_date"],x["day_of_week"]])
#
#
#distnctReportHoursSet = sorted(set(reportHours),key=reportHours.index)
#distinctReportDaysOfWeek = sorted(set(reportDaysOfWeek), key=reportDaysOfWeek.index)
#print(reportHoursSet)
#print(reportDaysOfWeekSet)
#

heatmap_z = []

#TBD Apr 18 AM: I need to catesian to all hours in the day for the plotted data to be correct!

for hour in reportHours:
    print("Creating heatmap row for hour: " + str(hour))
    new_heatmap_row = []
    for day in reportDaysOfWeek:
        candy_count = 0
        days_needed_for_y_axis = []
        for x in weekday_list:
            days_needed_for_y_axis.append([x["reporting_date"],x["day_of_week"],"not_in_database"])
            
        days_that_exist_for_hour = []    
        for dbdata in exampleData:
            if dbdata["logged_hour"] == hour:
                days_that_exist_for_hour.append([dbdata["reporting_date"],dbdata["day_of_week"]])
        
#        print("days that exist for hour " + str(hour) + ": " + str(days_that_exist_for_hour))

        days_in_database_for_hour = []
      
        for x in days_that_exist_for_hour:
            days_in_database_for_hour.append([x[0],x[1],"in_database"])
        
#        print("data source has data for these days: " + str(days_that_exist_for_hour))
        
        for x in days_needed_for_y_axis:
#            print(x)
            for y in days_in_database_for_hour:
                print("Checking to see if " + str(x[1]) + " is " + str(y[0]))
                if y[1] == x[1]:    
                    print("removing " + str(x))
                    days_needed_for_y_axis.remove(x)
        
        hourly_data_to_plot = days_needed_for_y_axis + days_in_database_for_hour
#        
        hourly_data_to_plot.sort()
#        
##        print(str(day) + " hourly data: " + str(hourly_data_to_plot))
#        
#        for hour in hourly_data_to_plot:
##            print("current day to plot: " + day)
##            print("current hour in hourly_data_to_plot: " + str(hour))
#            if hour[1] == "in_database":
#                for dbdata in exampleData:
#                    #print(dbdata)
#                    if dbdata["day_of_week"] == day and dbdata["logged_hour"] == hour[0]:
#                        candy_count = int(dbdata["CANDY_COUNT"])
#                        print("Current dbdata matches! " + day + " / hour: " + str(hour) + " Candy: " + str(candy_count))
#                        new_heatmap_row.append(candy_count)
#            elif hour[1] == "not_in_database":
#                new_heatmap_row.append(0)
##            print(new_heatmap_row)
#    heatmap_z.append(list(new_heatmap_row))
##        print(day)


#print("stahp")

#data = [
#    go.Heatmap(
#        z=heatmap_z,
#        x=reportDaysOfWeek,
#        y=reportHours,
#        colorscale='Viridis',
#    )
#]
#
#layout = go.Layout(
#    title='Candy Activity Over Time',
#    xaxis = dict(ticks='', nticks=36),
#    yaxis = dict(ticks='' )
#)
#
#fig = go.Figure(data=data, layout=layout)
#plot(fig, filename='candy-heatmap.html')