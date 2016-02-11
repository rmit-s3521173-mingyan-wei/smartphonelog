#!/usr/bin/python
import csv, sys, re
from datetime import datetime
from matplotlib import pyplot as plt
import datetime
import numpy as np
import process

dates = set()
app = []
battery = []
call = []
ring = []
text = []
charge = []
screen = []
bright = []
image = []
accel = []
pressure = []
location = []
wifi = []
temperature = []
audio = []

with open('data.csv', 'rb') as f:
	reader = csv.reader(f, delimiter = ';')
	reader.next()
	for row in reader:
		if re.match('2(.*)0', row[2]):
			if re.match('power(.*)level', row[3]):
				battery.append(row)
				date = row[2][:10]
				dates.add(date)
			elif re.match('app(.*)name', row[3]):
				app.append(row)
			elif re.match('power(.*)temperature', row[3]):
				temperature.append(row)
			elif re.match('phone(.*)calling(.*)', row[3]):
				call.append(row)
			elif re.match('sms(.*)sent(.*)', row[3]):
				text.append(row)				
			elif re.match('phone(.*)ringing(.*)', row[3]):
				ring.append(row)
			elif re.match('(.*)charger(.*)', row[3]):
				charge.append(row)
			elif re.match('screen(.*)power', row[3]):
				screen.append(row)
			elif re.match('screen(.*)level', row[3]):
				bright.append(row)
			elif re.match('wifi(.*)connected(.*)ssid', row[3]):
				wifi.append(row)
			elif re.match('audio(.*)ringer(.*)', row[3]):
				audio.append(row)
			elif re.match('image(.*)', row[3]):
				image.append(row)
			elif re.match('(.*)cid', row[3]) and row[4] != '-1':
				location.append(row)		
			elif re.match('sensor(.*)', row[3]):
				accel.append(row)
			elif re.match('sensor(.*)pressure(.*)', row[3]):
				pressure.append(row)

	dates = list(dates)
	dates = sorted(dates, key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
	print dates
	
	days = len(dates)
	times = 24 * 6
		
batteryLevel = process.getBatteryLevel(battery, dates, days, times)
battery_m = batteryLevel.mean(0)
print 'battery'
print battery_m
plt.plot(battery_m)
# plt.show()

tem = process.getTemperature(temperature, dates, days, times)
tem_m = tem.mean(0)
print 'temperature'
print tem_m
plt.plot(tem_m)
# plt.show()

screenPower = process.getScreenPower(screen, dates, days, times)
screen_m = screenPower.mean(0)
print 'screen power'
print screen_m
plt.plot(screen_m)
# plt.show()

outgoingCall = process.getOutgoingCalls(call, dates, days, times)
outgoing_m = outgoingCall.mean(0)
print 'outgoing calls'
print outgoing_m
plt.plot(outgoing_m)
# plt.show()

incomingCall = process.getIncomingCalls(ring, dates, days, times)
incoming_m = incomingCall.mean(0)
print 'incoming calls'
print incoming_m
plt.plot(incoming_m)
# plt.show()

sms = process.getText(text, dates, days, times)
sms_m = sms.mean(0)
print 'sms'
print sms_m
plt.plot(sms_m)
# plt.show()

charging = process.getCharging(charge, dates, days, times)
charging_m = charging.mean(0)
print 'charging'
print charging_m
plt.plot(charging_m)
# plt.show()

connectWifi = process.getWifiConnection(wifi, dates, days, times)
connectWifi_m = connectWifi.mean(0)
print 'connect to wifi'
print connectWifi_m
plt.plot(connectWifi_m)
# plt.show()

wifiList = process.rankWifi(wifi)
topWifi, wifi_m = process.getTopWifi(wifi, wifiList, dates, days, times)
print 'top wifi'
print wifi_m
plt.plot(wifi_m)
# plt.show()

ringerMode = process.getRingerMode(audio, dates, days, times)
ringer_m = ringerMode.mean(0)
print 'ringer mode'
print ringer_m
plt.plot(ringer_m)
# plt.show()

brightness = process.getBrightness(bright, dates, days, times)
bright_m = brightness.mean(0)
print 'brightness'
print bright_m
plt.plot(bright_m)
# plt.show()

photoLibrary = process.getImage(image, dates, days, times)
photo_m = photoLibrary.mean(0)
print 'photo'
print photo_m

cidList = process.rankCids(location)
cid, cid_m = process.getLocation(location, cidList, dates, days, times)
print 'cid'
print cid_m

appList = process.rankApps(app)
application, app_m = process.getApplication(app, appList, dates, days, times)
print 'app'
print app_m

matrix = np.zeros(shape = (43, times))
i = 0
while i < 10:
	matrix[i] = cid_m[i]
	i += 1
j = 0
while j < 20:
	matrix[i] = app_m[j]
	i += 1
	j += 1
k = 0
while k < 2:
	matrix[i] = wifi_m[k]
	i += 1
	k += 1
matrix[i] = battery_m
i += 1
matrix[i] = tem_m
i += 1
matrix[i] = screen_m
i += 1
matrix[i] = outgoing_m
i += 1
matrix[i] = incoming_m
i += 1
matrix[i] = sms_m
i += 1
matrix[i] = charging_m
i += 1
matrix[i] = connectWifi_m
i += 1
matrix[i] = ringer_m
i += 1
matrix[i] = bright_m
i += 1
matrix[i] = photo_m

a = 0
b = 0
while a < 30:
	while b < 10:
		print matrix[a][b]
		b += 1
	a += 1
	b = 0
	

