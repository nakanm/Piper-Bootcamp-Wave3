#!/usr/bin/env python3

import os
import time
import datetime
import pandas as pd
import redis
import urllib
import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

RedisHost = "127.0.0.1"
r = redis.Redis(host=RedisHost, port='6379', decode_responses = True)

homepath = "/home/ec2-user/Piper-Wave3/"
X_datetime_temp = []
Y_value_temp = []
X_datetime_moisture = []
Y_value_moisture = []
X_datetime_Light = []
Y_value_Light = []
X_datetime_Distance = []
Y_value_Distance = []
X_datetime_Gas = []
Y_value_Gas = []

length1 = [0]
length2 = [0]
length3 = [0]
length4 = [0]
length5 = [0]
l1=0
l2=0
l3=0
l4=0
l5=0

for key in r.scan_iter():
    sensor_value = r.get(key)
    key_list = key.split(" ") 
    sensor_key = key_list[2]
    t_datetime = key_list[0] + " " + key_list[1]
    datetime_temp = datetime.datetime.strptime(t_datetime, '%Y-%m-%d %H:%M:%S')

# "temperature"
    if sensor_key == "temperature":
       X_datetime_temp.append(datetime_temp)
       Y_value_temp.append(sensor_value)
       length1.append(l1)

# "moisture"
    if sensor_key == "moisture":
       X_datetime_moisture.append(datetime_temp)
       Y_value_moisture.append(sensor_value)
       length2.append(l2)

# "Light"
    if sensor_key == "Light":
       X_datetime_Light.append(datetime_temp)
       Y_value_Light.append(sensor_value)
       length3.append(l3)

# "Distance"
    if sensor_key == "Distance":
       X_datetime_Distance.append(datetime_temp)
       Y_value_Distance.append(sensor_value)
       length4.append(l4)

# "Gas-concentration"
    if sensor_key == "Gas-concentration":
       X_datetime_Gas.append(datetime_temp)
       Y_value_Gas.append(sensor_value)
       length5.append(l5)

plt.figure(figsize=(8,8), dpi=50)

# "temperature"
c = zip(X_datetime_temp, Y_value_temp)
d = sorted(c)
X_datetime_temp, Y_value_temp = zip(*d)
Y_value_temp2 = list(Y_value_temp) 
plt.gca().invert_yaxis()
fig, ax1 = plt.subplots()
ax1.plot(X_datetime_temp, Y_value_temp2)
# plt.show()
fig.savefig(homepath + "static/graph1.png")

# "moisture"
c = zip(X_datetime_moisture, Y_value_moisture)
d = sorted(c)
X_datetime_moisture, Y_value_moisture = zip(*d)
fig, ax1 = plt.subplots()
ax1.plot(X_datetime_moisture, Y_value_moisture)
# plt.show()
fig.savefig(homepath + "static/graph2.png")

# "Light"
c = zip(X_datetime_Light, Y_value_Light)
d = sorted(c)
X_datetime_Light, Y_value_Light = zip(*d)
fig, ax1 = plt.subplots()
ax1.plot(X_datetime_Light, Y_value_Light)
# plt.show()
fig.savefig(homepath + "static/graph3.png")

# "Distance"
c = zip(X_datetime_Distance, Y_value_Distance)
d = sorted(c)
X_datetime_Distance, Y_value_Distance = zip(*d)
fig, ax1 = plt.subplots()
ax1.plot(X_datetime_Distance, Y_value_Distance)
# plt.show()
fig.savefig(homepath + "static/graph4.png")

# "Gas-concentration"
c = zip(X_datetime_Gas, Y_value_Gas)
d = sorted(c)
X_datetime_Gas, Y_value_Gas = zip(*d)
fig, ax1 = plt.subplots()
ax1.plot(X_datetime_Gas, Y_value_Gas)
# plt.show()
fig.savefig(homepath + "static/graph5.png")

