#!/usr/bin/python
import sys, re
from datetime import datetime
import datetime
from matplotlib import pyplot as plt
import numpy as np
import operator
import math

def getBatteryLevel(file, dates, days, times):
	hist = np.empty(shape = (days, times))
	for i in range(days):
		for j in range(times):
			hist[i][j] = -1
	for i in range(days):
		lh = 0
		for row in file:
			if re.match(dates[i], row[2]):
				hr = int(row[2][11:13])
				min = int(row[2][14])
				j = hr * 6 + min
				hist[i][j] = int(row[4])

# 	Fill in the missing values in the beginning and at the end by
#	using the first or last available value
	j = 0
	while hist[0][j] == -1:
		j += 1
	for x in range(j-1):
		hist[0][x] = hist[0][j]

	j = times - 1	
	while hist[days-1][j] == -1:
		j -= 1
	x = j + 1
	while x < times:
		hist[days-1][x] = hist[days-1][j]
		x += 1
		
	for i in range(days):			
		for j in range(times):
			if hist[i][j] == -1:
				front = j - 1
				y = j
				while y < times and hist[i][y] == -1:
					y += 1
					end = y
				if front >= 0 and end < times:
					gap = end - front
					increment = (hist[i][end] - hist[i][front]) / gap
					y = front + 1
					while y < end:
						hist[i][y] = hist[i][y-1] + increment
						y += 1
				elif i < days - 2 and end >= times:
					y = 0
					end = 0
					while y < times-1 and hist[i+1][y] == -1:
						y += 1
						end = y
					gap = times - front + end - 1
					increment = (hist[i+1][y] - hist[i][front]) / gap
					y = front + 1
					while y < times:
						hist[i][y] = hist[i][y-1] + increment
						y += 1
				elif i > 0 and front < 0:
					front = times - 1
					gap = end
					increment = (hist[i][end] - hist[i-1][front]) / gap
					y = end - 1
					while y >= 0:
						hist[i][y] = hist[i][y+1] - increment
						y -= 1
	return hist

def getTemperature(file, dates, days, times):
	hist = np.empty(shape = (days, times))
	for i in range(days):
		for j in range(times):
			hist[i][j] = -1
	for i in range(days):
		lh = 0
		for row in file:
			if re.match(dates[i], row[2]):
				hr = int(row[2][11:13])
				min = int(row[2][14])
				j = hr * 6 + min
				hist[i][j] = int(row[4])
	j = 0
	while hist[0][j] == -1:
		j += 1
	for x in range(j-1):
		hist[0][x] = hist[0][j]

	j = times - 1	
	while hist[days-1][j] == -1:
		j -= 1
	x = j + 1
	while x < times:
		hist[days-1][x] = hist[days-1][j]
		x += 1
		
	for i in range(days):			
		for j in range(times):
			if hist[i][j] == -1:
				front = j - 1
				y = j
				while y < times and hist[i][y] == -1:
					y += 1
					end = y
				if front >= 0 and end < times:
					gap = end - front
					increment = (hist[i][end] - hist[i][front]) / gap
					y = front + 1
					while y < end:
						hist[i][y] = hist[i][y-1] + increment
						y += 1
				elif i < days - 2 and end >= times:
					y = 0
					end = 0
					while y < times-1 and hist[i+1][y] == -1:
						y += 1
						end = y
					gap = times - front + end - 1
					increment = (hist[i+1][y] - hist[i][front]) / gap
					y = front + 1
					while y < times:
						hist[i][y] = hist[i][y-1] + increment
						y += 1
				elif i > 0 and front < 0:
					front = times - 1
					gap = end
					increment = (hist[i][end] - hist[i-1][front]) / gap
					y = end - 1
					while y >= 0:
						hist[i][y] = hist[i][y+1] - increment
						y -= 1
	return hist

	
def getScreenPower(file, dates, days, times):
	hist = np.zeros(shape=(days,times))
	for i in range(days):
		for row in file:
			if re.match(dates[i], row[2]):
				hr = int(row[2][11:13])
				min = int(row[2][14])
				j = hr * 6 + min
				if row[4] == 'on':
					hist[i][j] = 2
				elif row[4] == 'off':
					hist[i][j] = 1
	for i in range(days):
		for j in range(times):
			if hist[i][j] == 2:
				m = i
				n = j
				while hist[m][n] != 1 and m < days:
					if n == times - 1:
						if m == days - 1:
							hist[m][n] = 1
						else:
							hist[m][n] = 1
							m += 1
							n = 0
					if n < times - 1:
						hist[m][n] = 1
						n += 1
	return hist

def getBrightness(file, dates, days, times):
	hist = np.zeros(shape=(days,times))
	for i in range(days):
		for row in file:
			if re.match(dates[i], row[2]):
				hr = int(row[2][11:13])
				min = int(row[2][14])
				j = hr * 6 + min
				hist[i][j] = row[4]
	return hist
						
def getOutgoingCalls(file, dates, days, times):
	hist = np.zeros(shape=(days,times))
	for i in range(days):
		for row in file:
			if re.match(dates[i], row[2]):
				hr = int(row[2][11:13])
				min = int(row[2][14])
				j = hr * 6 + min
				hist[i][j] = 1
	return hist

def getIncomingCalls(file, dates, days, times):
	hist = np.zeros(shape=(days,times))
	for i in range(days):
		for row in file:
			if re.match(dates[i], row[2]):
				hr = int(row[2][11:13])
				min = int(row[2][14])
				j = hr * 6 + min
				hist[i][j] = 1
	return hist
	
def getText(file, dates, days, times):
	hist = np.zeros(shape=(days,times))
	for i in range(days):
		for row in file:
			if re.match(dates[i], row[2]):
				hr = int(row[2][11:13])
				min = int(row[2][14])
				j = hr * 6 + min
				hist[i][j] = 1
	return hist
	
def getCharging(file, dates, days, times):
	hist = np.zeros(shape=(days,times))
	for i in range(days):
		for row in file:
			if re.match(dates[i], row[2]):
				hr = int(row[2][11:13])
				min = int(row[2][14])
				j = hr * 6 + min
				if row[4] == 'ac' or row[4] == 'usb':
					hist[i][j] = 1
	return hist
	
def getWifiConnection(file, dates, days, times):
	hist = np.zeros(shape=(days,times))
	for i in range(days):
		for row in file:
			if re.match(dates[i], row[2]):
				hr = int(row[2][11:13])
				min = int(row[2][14])
				j = hr * 6 + min
				hist[i][j] = 1
	return hist

def rankWifi(file):
	wifis = dict()
	for row in file:
		if row[4] not in wifis:
			wifis[row[4]] = 1
		else:
			wifis[row[4]] += 1
	sorted_wifi = sorted(wifis.items(), key = operator.itemgetter(1), reverse = True)
	topList = []
	for k,v in sorted_wifi[:2]:
		topList.append(k)
	return topList
	
def getTopWifi(file, topList, dates, days, times):
	listOfWifis = []
	listOfMean = []
	for x in topList:
		hist = np.zeros(shape=(days, times))
		for i in range(days):
			for row in file:
				if re.match(dates[i],row[2]) and row[4] == x:
					hr = int(row[2][11:13])
					min = int(row[2][14])
					j = hr * 6 + min
					hist[i][j] = 1
		average = hist.mean(0)
		listOfWifis.append(hist)
		listOfMean.append(average)
	return listOfWifis, listOfMean
	
def getRingerMode(file, dates, days, times):
	hist = np.zeros(shape=(days, times))
	for i in range(days):
		for row in file:
			if re.match(dates[i], row[2]):
				hr = int(row[2][11:13])
				min = int(row[2][14])
				j = hr * 6 + min
				if row[4] == 'silent' or row[4] == 'vibrate':
					hist[i][j] = 1
	return hist
	
def getImage(file, dates, days, times):
	hist = np.zeros(shape=(days, times))
	for i in range(days):
		for row in file:
			if re.match(dates[i], row[2]):
				hr = int(row[2][11:13])
				min = int(row[2][14])
				j = hr * 6 + min
				hist[i][j] = 1
	return hist
	
def getAccelerometer(file, dates, days, times):
	hist = np.zeros(shape=(days, times))
	for i in range(days):
		for row in file:
			if re.match(dates[i], row[2]):
				hr = int(row[2][11:13])
				min = int(row[2][14])
				j = hr * 6 + min
				hist[i][j] = row[4]
	return hist
	
def rankCids(file):
	cids = dict()
	for row in file:
		if row[4] not in cids:
			cids[row[4]] = 1
		else:
			cids[row[4]] += 1
	sorted_cid = sorted(cids.items(), key = operator.itemgetter(1), reverse = True)
	topList = []
	for k,v in sorted_cid[:10]:
		topList.append(k)
	return topList
	
def getLocation(file, topList, dates, days, times):
	listOfCids = []
	listOfMean = []
	for x in topList:
		hist = np.zeros(shape=(days, times))
		for i in range(days):
			for row in file:
				if re.match(dates[i],row[2]) and row[4] == x:
					hr = int(row[2][11:13])
					min = int(row[2][14])
					j = hr * 6 + min
					hist[i][j] = 1
		average = hist.mean(0)
		listOfCids.append(hist)
		listOfMean.append(average)
	return listOfCids, listOfMean
	
def rankApps(file):
	apps = dict()
	for row in file:
		if row[4] not in apps:
			apps[row[4]] = 1
		else:
			apps[row[4]] += 1
	applications = sorted(apps.items(), key = operator.itemgetter(1), reverse = True)
	topList = []
	for k,v in applications[:20]:
		topList.append(k)
	return topList
	
def getApplication(file, topList, dates, days, times):
	listOfApps = []
	listOfMean = []
	for x in topList:
		hist = np.zeros(shape=(days, times))
		for i in range(days):
			for row in file:
				if re.match(dates[i],row[2]) and row[4] == x:
					hr = int(row[2][11:13])
					min = int(row[2][14])
					j = hr * 6 + min
					hist[i][j] = 1
		average = hist.mean(0)
		listOfApps.append(hist)
		listOfMean.append(average)
	return listOfApps, listOfMean
	
def entropy(probabilities):
	return sum(-p * math.log(p, 2)
			for p in probabilities if p)
			

