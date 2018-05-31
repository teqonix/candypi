#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import random
import psutil
import datetime
import dothat.backlight as backlight
import dothat.lcd as lcd
import threading
import createCandyDashboard as DASHboard
import pymysql
from selenium import webdriver

#Set up GPIO for button press event:
GPIO.setmode(GPIO.BCM)  
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def lcdRainbowBackgroundThread():
    lcd_thread = threading.Thread(name="lcdRainbow", target=lcdRainbow)
    lcd_thread.start()

def firefoxBackgroundThread():
    web_thread = threading.Thread(name="webDisplay", target=runWebBrowser)
    web_thread.start()

def dashboardBackgroundThread():
    dashboard_thread = threading.Thread(name="dashboard", target=runDashboard)
    dashboard_thread.start()

def lcdScreenUpdatesThread(backlight):
    lcd_update_thread = threading.Thread(name="lcdScreenUpdatesThread", target=continuousLCDUpdate)
    lcd_update_thread.start()

def lcdWriteHeader(lcd):
    lcd.set_cursor_position(1, 1)
    lcd.write("*CANDY TRACKER* ")
    lcd.set_cursor_position(0, 0)
    lcd.write("!!!!- BETA -!!!!")
    lcd.set_cursor_position(2, 2)

def resetScreen(lcdBacklight, lcd):
    lcd.clear()
    randomBlue = random.randint(0,255)
    randomRed = random.randint(0,255)
    randomGreen = random.randint(0,255)
    backlight.rgb(randomRed,randomGreen,randomBlue)
    lcdWriteHeader(lcd)
    CPUusage = psutil.cpu_percent(interval=None)
    meminfo = psutil.virtual_memory()
    cpuUsageString = ("CPU " + str(round(CPUusage)) + "%")
    memUsageString = ("RAM " + str(round(meminfo.percent)) + "%")
    lcdWriteHeader(lcd)
    lcd.set_cursor_position(0, 2)
    lcd.write(memUsageString)
    lcd_cursor_x = (16 - len(cpuUsageString))
    lcd.set_cursor_position(lcd_cursor_x, 2)
    lcd.write(cpuUsageString)

def lcdRainbow():
    lcd.clear()
    lcd.set_cursor_position(0, 1)
    lcd.write("IT'S CANDY TIME!")
    for x in range(0,360):
        backlight.sweep((x % 360) / 360.0)
    lcd.clear()
    lcd.set_cursor_position(1, 1)
    lcd.write("CANDY TRACKER")
    print("LCD Updates Complete")
    resetScreen(backlight,lcd)

def candyButtonPressed(channel):
    print("We got ourselves a live one here!" + str(random.randint(0,50)))
    activeCandyButtonThreads = threading.active_count()
    current_threads = threading.enumerate()

    lcdRainbowActive = False
    for x in current_threads:
        if x.name == 'lcdRainbow':
            lcdRainbowActive = True
    
    if lcdRainbowActive == False:
        #This is used to keep the LCD from freaking out if the button is pressed multiple times
        lcdRainbowBackgroundThread()
    
    mysql = connectToDB()
    current_timestamp = datetime.datetime.now()
    with mysql.cursor() as cursor:
        currentEntrySQL = "INSERT INTO candydb.candycounts (candyconsumption_date_ik,logged_date) VALUES (" + current_timestamp.strftime("%Y%m%d") + ",STR_TO_DATE('" + current_timestamp.strftime("%Y,%m,%d, %H:%M:%S") + "', '%Y,%m,%d,%T'));"
        print(currentEntrySQL)
        cursor.execute(currentEntrySQL)
        mysql.commit()
        mysql.close()

def continuousLCDUpdate():
    while 1==1:
        time.sleep(1)
        lcdRainbowActive = False
        current_threads = threading.enumerate()
        
        for x in current_threads:
            if x.name == 'lcdRainbow':
                lcdRainbowActive = True
                
        if lcdRainbowActive == False:
            lcd.clear()
            resetScreen(backlight,lcd)


def runDashboard():
    DASHboard.setup_app()

def runWebBrowser():
    driver = webdriver.Firefox()
    driver.get("http://127.0.0.1:8050")
    while 1==1:
        for x in range(0,600):
            x = x + 1
            time.sleep(1)
            #print("Firefox refresh loop second " + str(x) + " of 600")
        driver.refresh()
    
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



#This has all the code needed to detect when the button has been pressed and released
GPIO.add_event_detect(6, GPIO.RISING, callback=candyButtonPressed, bouncetime=30000)
lcd.set_contrast(50)
resetScreen(backlight,lcd)

dashboardBackgroundThread()
firefoxBackgroundThread()
lcdScreenUpdatesThread(backlight)

while True:
    time.sleep(0.1)
GPIO.cleanup()

##while True:
##    input_state = GPIO.input(6)
##    print(str(input_state))
##    time.sleep(0.2)