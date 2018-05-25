#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysqlcandydb
import datetime
import logging
import base64
import plotly.graph_objs as go


class generateCandyPlots:
    
#    def __init__(self):       

    def getKPIArrow(self, trendString):
        if trendString == 'Down':
            image_path = '/home/pi/COBI_CandyTrack/assets/red_arrow_down.png'
        elif trendString == "Same":
            image_path = '/home/pi/COBI_CandyTrack/assets/yellow_arrow_right.png'
        elif trendString == "Up":
            image_path = '/home/pi/COBI_CandyTrack/assets/green_arrow_up.png'
        else:
            image_path = '/home/pi/COBI_CandyTrack/assets/black_arrow_down.png'
#            image_path = '/home/pi/COBI_CandyTrack/assets/black_arrow_down.png'
                    
        encoded_img = base64.b64encode(open(image_path, 'rb').read())
        return encoded_img
                
    
    def fetchHourlyTrend(self):
        sqlstatement = """SELECT 
                            CASE WHEN SUM(candycount_nb) IS NULL THEN 0 ELSE SUM(candycount_nb) END AS currentHourCandyCount
                            ,STR_TO_DATE(CONCAT(CAST(CURRENT_DATE AS CHAR(12)),' ',CAST(HOUR(CURRENT_TIME) AS CHAR),':00:00'),'%Y-%m-%d %T') AS startOfCurrentHour
                            ,CURRENT_TIMESTAMP AS queryCurrentTime
                        FROM candydb.candycounts cc
                        WHERE 1=1
                        	AND cc.logged_date BETWEEN 
                                STR_TO_DATE(CONCAT(CAST(CURRENT_DATE AS CHAR(12)),' ',CAST(HOUR(CURRENT_TIME) AS CHAR),':00:00'),'%Y-%m-%d %T')
                                AND CURRENT_TIMESTAMP
                    ;"""
                    
        try:
            dbconnection = mysqlcandydb
            db = dbconnection.candydb.connectToDB()
        except Exception as e:
            logging.exception("Error connecting to mySQL instance: " + str(e))
            
        with db.cursor() as cursor:
            cursor.execute(sqlstatement)
            currentHourCandyData = cursor.fetchall()
        
        sqlstatement = """SELECT 
                        	CASE WHEN SUM(candycount_nb) IS NULL THEN 0 ELSE SUM(candycount_nb) END AS lagHourCandyCount
                        	,ADDTIME(STR_TO_DATE(CONCAT(CAST(CURRENT_DATE AS CHAR(12)),' ',CAST(HOUR(CURRENT_TIME) AS CHAR),':00:00'),'%Y-%m-%d %T'),'-01:00:00')AS startOfLagHour
                        	,STR_TO_DATE(CONCAT(CAST(CURRENT_DATE AS CHAR(12)),' ',CAST(HOUR(CURRENT_TIME) AS CHAR),':00:00'),'%Y-%m-%d %T') AS endOfLagHour
                        FROM candydb.candycounts cc
                        WHERE 1=1
                        	AND cc.logged_date BETWEEN 
                        		ADDTIME(STR_TO_DATE(CONCAT(CAST(CURRENT_DATE AS CHAR(12)),' ',CAST(HOUR(CURRENT_TIME) AS CHAR),':00:00'),'%Y-%m-%d %T'),'-01:00:00')
                        		AND STR_TO_DATE(CONCAT(CAST(CURRENT_DATE AS CHAR(12)),' ',CAST(HOUR(CURRENT_TIME) AS CHAR),':00:00'),'%Y-%m-%d %T')
         ;"""
        
        with db.cursor() as cursor:
            cursor.execute(sqlstatement)
            lastHourCandyData = cursor.fetchall()

        previousHourCandyAmt = lastHourCandyData[0].get('lagHourCandyCount')
        currentHourCandyAmt = currentHourCandyData[0].get('currentHourCandyCount')
        hourlyTrend = ""
        lagHourCandyRatio = 0        
        
        if (previousHourCandyAmt != 0 and currentHourCandyAmt != 0):
            lagHourCandyRatio = (currentHourCandyAmt / previousHourCandyAmt)
            if (lagHourCandyRatio >= 0 and lagHourCandyRatio < 0.7):
                hourlyTrend = "Down"
            if (lagHourCandyRatio >= 0.7 and lagHourCandyRatio < 1.1):
                hourlyTrend = "Same"
            if (lagHourCandyRatio > 1.1):
                hourlyTrend = "Up"                
        elif (previousHourCandyAmt != 0 and currentHourCandyAmt == 0):
            hourlyTrend = "Down"
        elif (previousHourCandyAmt == 0 and currentHourCandyAmt != 0):
            hourlyTrend = "Up"

        db.close()

        return {'Hourly Trend Ratio': lagHourCandyRatio
                , 'Hourly Trend': hourlyTrend
                , 'Current Hour Candy Count': currentHourCandyAmt
                , 'Lag Hour Candy Count': previousHourCandyAmt}
    
    
    def fetchDailyTrend(self):
        sqlstatement = """SELECT 
                            CASE WHEN SUM(candycount_nb) IS NULL THEN 0 ELSE SUM(candycount_nb) END AS currentDayCandyCount
                            ,CURRENT_DATE AS startOfCurrentDay
                            ,CURRENT_TIMESTAMP AS queryCurrentTime
                        FROM candydb.candycounts cc
                        WHERE 1=1
                        	AND cc.logged_date BETWEEN CURRENT_DATE AND CURRENT_TIMESTAMP
                    ;"""
                    
        try:
            dbconnection = mysqlcandydb
            db = dbconnection.candydb.connectToDB()
        except Exception as e:
            logging.exception("Error connecting to mySQL instance: " + str(e))
            
        with db.cursor() as cursor:
            cursor.execute(sqlstatement)
            currentDayCandyData = cursor.fetchall()
        
        sqlstatement = """SELECT 
                            CASE WHEN SUM(candycount_nb) IS NULL THEN 0 ELSE SUM(candycount_nb) END AS lagDayCandyCount 
                            ,ADDDATE(CURRENT_DATE, INTERVAL -1 DAY) AS startOfPreviousDay
                            ,ADDDATE(CURRENT_TIMESTAMP, INTERVAL -1 DAY) AS endOfPreviousDayTrend
                        FROM candydb.candycounts cc
                        WHERE 1=1
                        	AND cc.logged_date BETWEEN ADDDATE(CURRENT_DATE, INTERVAL -1 DAY) AND ADDDATE(CURRENT_TIMESTAMP, INTERVAL -1 DAY)
                        """
        
        with db.cursor() as cursor:
            cursor.execute(sqlstatement)
            lastDayCandyData = cursor.fetchall()

        previousDayCandyAmt = lastDayCandyData[0].get('lagDayCandyCount')
        currentDayCandyAmt = currentDayCandyData[0].get('currentDayCandyCount')
        hourlyTrend = ""
        lagDayCandyRatio = 0
        
        if (previousDayCandyAmt != 0 and currentDayCandyAmt != 0):
            lagDayCandyRatio = (currentDayCandyAmt / previousDayCandyAmt)
            if (lagDayCandyRatio >= 0 and lagDayCandyRatio < 0.7):
                hourlyTrend = "Down"
            if (lagDayCandyRatio >= 0.7 and lagDayCandyRatio < 1.1):
                hourlyTrend = "Same"
            if (lagDayCandyRatio > 1.1):
                hourlyTrend = "Up"                
        elif (previousDayCandyAmt != 0 and currentDayCandyAmt == 0):
            hourlyTrend = "Down"
        elif (previousDayCandyAmt == 0 and currentDayCandyAmt != 0):
            hourlyTrend = "Up"

        db.close()
        
        return {'Daily Trend Ratio': lagDayCandyRatio
                , 'Daily Trend': hourlyTrend
                , 'Current Day Candy Count': currentDayCandyAmt
                , 'Lag Day Candy Count': previousDayCandyAmt}        

    
    def createCandyHeatmap(self, date_from, date_to, start_hour, end_hour):
        try:
             
            if start_hour < 0 and start_hour > 23:
                raise
            elif end_hour < 0 and start_hour > 23:
                raise
            
            timedelta_days = date_from - date_to
            
        except Exception as e:
            logging.exception("Please fix your input arguments.  Real dates and times are required.")
            raise 
            
        try:
            dbconnection = mysqlcandydb
            db = dbconnection.candydb.connectToDB()
        except Exception as e:
            logging.exception("Error connecting to mySQL instance: " + str(e))
            
        where_clause = """WHERE 1=1
            AND cc.candyconsumption_date_ik BETWEEN STR_TO_DATE('""" + date_from.strftime('%Y%m%d') + """','%Y%m%d') AND STR_TO_DATE('""" + date_to.strftime('%Y%m%d') + """','%Y%m%d')
            AND HOUR(cc.logged_date) BETWEEN """ + str(start_hour) + """ AND """ + str(end_hour)
    
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
        
        hour_list = range(start_hour,end_hour)
        
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
        #    print("Creating heatmap row for hour: " + str(hour))
            new_heatmap_row = []
        #    for day in reportDaysOfWeek:
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
         
        #    print("Line 119: " + str(days_needed_for_y_axis))
           
            days_to_remove = []
            for x in days_needed_for_y_axis:
        #        print("days_needed_for_y_axis loop: " + str(x))
                for y in days_in_database_for_hour:
        #            print("Checking to see if " + str(x[1]) + " is " + str(y[0]))
        #            print(x[1] + " " + y[1])
                    if y[1] == x[1]:    
        #                    print("removing " + str(x))
                        days_to_remove.append(x)
            
        #    print("days needed for y axis: " + str(days_needed_for_y_axis))
        #    print("days in database for hour " + str(days_in_database_for_hour))
        #    print("days with database data to remove from days needed list: " + str(days_to_remove))
            
            hourly_data_to_plot = days_needed_for_y_axis + days_in_database_for_hour
        #        
            hourly_data_to_plot.sort()
        #   
            for remove_day in days_to_remove:
                for x in hourly_data_to_plot:
                    if x == remove_day:
        #                print("Removing this day beause we found it in the database: " + str(x))
                        hourly_data_to_plot.remove(x)
             
        #    print(" hourly data to plot: " + str(hourly_data_to_plot))
        #        
            for day in hourly_data_to_plot:
        #        print("current day to plot: " + day[1])
        #        if day[1] == "Mon May 07" and hour == 17:
        #            print("Debug Stop")
        #            print("current hour in hourly_data_to_plot: " + str(hour))
                if day[2] == "in_database":
        #            print("in database: " + str(day[1]))
                    for dbdata in exampleData:
                        #print(dbdata)
                        if dbdata["reporting_date"] == day[0] and dbdata["logged_hour"] == hour:
                            candy_count = int(dbdata["CANDY_COUNT"])
        #                    print("Current dbdata matches! " + day[1] + " / hour: " + str(hour) + " Candy: " + str(candy_count))
                            new_heatmap_row.append(candy_count)
                elif day[2] == "not_in_database":
                    new_heatmap_row.append(0)
        #    print(new_heatmap_row)
            heatmap_z.append(list(new_heatmap_row))
        #        print(day)
        
        formattedDaysOfWeek = []
        
        for x in reportDaysOfWeek:
            formattedDaysOfWeek.append(x[1])
        
        #print("stahp")
        
        data = [
            go.Heatmap(
                z=heatmap_z,
                x=formattedDaysOfWeek,
                y=reportHours,
                colorscale='Viridis',
                colorbar = dict(
                        title = 'Pieces of Candy'
                        )
            )
        ]

        layout = go.Layout(
            title=('Candy Activity Within Past ' + str(timedelta_days)),
            xaxis = dict(ticks='', nticks=36, title='Timeline (Days)'),
            yaxis = dict(ticks='', title='Hour of Day (HH24)')
        )
        
        fig = go.Figure(data=data, layout=layout)
        return fig 

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()
        
    def createCandyWeeklyBarChart(self, weeks_looking_back):
        sqlstatement = """SELECT 
                    	SUM(cc.candycount_nb) AS candyconsumed_nb
                        ,CONCAT(dd.year, ' - Wk ', dd.week_starting_monday) AS week
                    FROM candydb.candycounts cc
                    	INNER JOIN candydb.date_dimension dd
                    		ON cc.candyconsumption_date_ik = dd.date_id
                    WHERE 1=1
                    	AND cc.logged_date BETWEEN DATE_ADD(CURRENT_DATE, INTERVAL -""" + str(weeks_looking_back) + """ WEEK) AND CURRENT_DATE
                    GROUP BY CONCAT(dd.year, ' ', dd.week_starting_monday)
                    ORDER BY cc.logged_date ASC
                    ;"""
                    
        try:
            dbconnection = mysqlcandydb
            db = dbconnection.candydb.connectToDB()
        except Exception as e:
            logging.exception("Error connecting to mySQL instance: " + str(e))
            
        with db.cursor() as cursor:
            cursor.execute(sqlstatement)
            weeklyCandyData = cursor.fetchall()                
    
        x_axis = []
        y_axis = []
        
        for x in weeklyCandyData:
#            print(x["week"])
            x_axis.append(x["week"])
        
        for y in weeklyCandyData:
            y_axis.append(y["candyconsumed_nb"])


        weeklyCandyBar = [go.Bar(
                    x=x_axis,
                    y=y_axis
            )]
    
        layout = go.Layout(
            title='Past ' + str(weeks_looking_back) + ' Weeks of Candy Usage',
            yaxis=dict(
                title='Pieces of Candy',
                titlefont=dict(
                    size=16,
                    color='rgb(107, 107, 107)'
                ),
            )
        )
                
        weeklyCandyBarChart = go.Figure(data=weeklyCandyBar, layout=layout)
        
        db.close()
        
        return weeklyCandyBarChart        