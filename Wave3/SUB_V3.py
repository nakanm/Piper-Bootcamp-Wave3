#!/usr/bin/env python3

import time
import datetime
import paho.mqtt.client as mqtt
import redis
import slackweb

# MQTT Broker
MQTT_HOST = "test.mosquitto.org"       # broker adress
MQTT_PORT = 1883                # broker port
MQTT_KEEP_ALIVE = 360            # keep alive
RedisHost = "127.0.0.1"

slack = slackweb.Slack(url="your slack address")

# broker connect
def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

r = redis.Redis(host=RedisHost, port='6379')

# recieve message
def on_message(mqttc, obj, msg):
    m = str(msg.payload.decode("utf-8"))
    list = m.split(" ")

    datetime = list[0] + " " + list[1]
    sensor_list = list[2:]
    
#   Separete Key and Value
    sensor_key = sensor_list[0::2]
    sensor_value = sensor_list[1::2]

    for key,value in zip(sensor_key,sensor_value):
        key = datetime + " " + key
        print(key, value)
        msg = key + "=" + value
        r.set(key, value)
        slack.notify(text=msg)	# Slack push
  
mqttc = mqtt.Client()
mqttc.on_message = on_message  # call back
mqttc.on_connect = on_connect
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEP_ALIVE)

mqttc.subscribe("Nakano-MQTT")  # name of topic

mqttc.loop_forever()  # loop

