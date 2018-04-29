#!/usr/bin/env python3
"""
Spyder Editor

This is a temporary script file.
"""

import pymysql
import random
from datetime import datetime
from datetime import date 
from datetime import timedelta
import logging

def createSampleData (numberOfDays, maxEntriesPerDay, startDateInt):
    databaseentries = [] 
    try:
        start_datetime = datetime.strptime(str(startDateInt),"%Y%m%d")
    except Exception as e:
        logging.error("Error when trying to convert start date to date value in Python.." + str(startDateInt))
        raise 
    for x in range (0, numberOfDays):
        print("Here we go! " + str(x))
        todaysEntries = random.randint(0,maxEntriesPerDay)
        currentDate = start_datetime + timedelta(days=x)
        for entry in range(0,todaysEntries):
            print("Entry for day " + str(x) + ": " + str(entry) + " for " + str(currentDate))
            entryHour = random.randint(0,23)
            entryMinute = random.randint(0,59)
            entrySecond = random.randint(0,59)
            currentDate = (currentDate + timedelta(hours=entryHour, minutes=entryMinute, seconds=entrySecond))  
            currentDateStr = currentDate.strftime("%Y,%m,%d, %H:%M:%S")
            currentEntrySQL = "INSERT INTO candydb.candycounts (candyconsumption_date_ik,logged_date) VALUES (" + currentDate.strftime("%Y%m%d") + ",STR_TO_DATE('" + currentDateStr + "', '%Y,%m,%d,%T'));"
            databaseentries.append({"SQL Statement":currentEntrySQL,"Entry Date":currentDate})
    return databaseentries        

def connectToDB():
    connection = pymysql.connect(
            host = 'localhost'
            ,user = 'cobicandy'
            ,password = 'cobi'
            ,charset = 'utf8mb4'
            ,cursorclass=pymysql.cursors.DictCursor
            )
    connection.connect()
    return connection

#syntax: STR_TO_DATE('2018,01,01, 17:23:12', '%Y,%m,%d,%T')
     
if __name__ == "__main__":
    exampleData = createSampleData(numberOfDays = 165, maxEntriesPerDay = 55, startDateInt = 20180101)
    
    mysql = connectToDB()
    
    with mysql.cursor() as cursor:
        sql = "TRUNCATE TABLE candydb.candycounts"
        cursor.execute(sql)
        for exampleRow in (exampleData):    
            sql = exampleRow["SQL Statement"]
#            print(sql)
            cursor.execute(sql)
        
        mysql.commit()
        mysql.close()
            
    print("That's all folks!")
    
