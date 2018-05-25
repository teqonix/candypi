#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import math
import random
import dothat.backlight as backlight
import dothat.lcd as lcd
import threading
import createCandyDashboard as DASHboard
from selenium import webdriver
import urllib

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

def resetScreen(lcdBacklight, lcd):
    lcd.clear()
    lcdBacklight.rgb(255,0,0)
    lcd.set_cursor_position(1, 1)
    lcd.write("*CANDY TRACKER* ")
    lcd.set_cursor_position(2, 0)
    lcd.write(" !- BETA -! ")
    lcd.set_cursor_position(2, 2)
    lcd.write(" !- BETA -! ")

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
    
##    for x in current_threads:
##        print(str(x))
    
    if activeCandyButtonThreads < 3:
        #This is used to keep the LCD from freaking out if the button is pressed multiple times
        lcdRainbowBackgroundThread()

def runDashboard():
    DASHboard.setup_app()

def runWebBrowser():
    driver = webdriver.Firefox()
    driver.get("http://127.0.0.1:8050")
    while 1==1:
        for x in range(0,60):
            x = x + 1
            time.sleep(1)
            print("Firefox refresh loop second " + str(x) + " of 60")
        driver.refresh()
        
    

#This has all the code needed to detect when the button has been pressed and released
GPIO.add_event_detect(6, GPIO.RISING, callback=candyButtonPressed, bouncetime=200)
lcd.set_contrast(50)
resetScreen(backlight,lcd)

dashboardBackgroundThread()
firefoxBackgroundThread()

while True:
    time.sleep(0.1)
GPIO.cleanup()

##while True:
##    input_state = GPIO.input(6)
##    print(str(input_state))
##    time.sleep(0.2)