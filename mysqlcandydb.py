#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 21:23:33 2018

@author: pi
"""

import pymysql

class candydb:
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