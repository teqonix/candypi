#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from generatesampledata import candySampleData

data_generator = candySampleData()
data_generator.createExampleData(daysOfSampleData=4,maxRowsPerDay=567, startDateInteger=20180521, truncateDB=False)
