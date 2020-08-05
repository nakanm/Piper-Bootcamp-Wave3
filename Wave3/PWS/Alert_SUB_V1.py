#!/usr/bin/env python3

import os
import time
import datetime
import paho.mqtt.client as mqtt
import slackweb

# MQTT Broker
MQTT_HOST = "test.mosquitto.org"       # broker adress
MQTT_PORT = 1883                # broker port
MQTT_KEEP_ALIVE = 60            # keep alive

slack = slackweb.Slack(url="your Slack address")

# broker connect
def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

# recieve message
def on_message(mqttc, obj, msg):
    m = str(msg.payload.decode("utf-8"))
    print(m)
    slack.notify(text=m)  # Slack push
  
mqttc = mqtt.Client()
mqttc.on_message = on_message  # call back
mqttc.on_connect = on_connect
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEP_ALIVE)

mqttc.subscribe("your MQTT")  # name of topic

mqttc.loop_forever()  # loop

