#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from plotly.offline import plot
from candytestplotly import generateCandyPlots
import datetime

candyPlotter = generateCandyPlots()

start_date=datetime.date(2018,7,1)
end_date=datetime.date(2018,7,25)

#candyheatmap = candyPlotter.createCandyHeatmap(date_from=start_date, date_to=end_date, start_hour=6, end_hour=18)
candyweeklyusage = candyPlotter.createCandyWeeklyBarChart(4)
#plot(candyheatmap, filename='candy-heatmap.html')
plot(candyweeklyusage, filename='candyweeklyusage.html')