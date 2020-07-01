#!/usr/bin/env python3


import time
import datetime
import paho.mqtt.client as mqtt
import redis

# MQTT Broker
MQTT_HOST = "test.mosquitto.org"       # broker adress
MQTT_PORT = 1883                # broker port
MQTT_KEEP_ALIVE = 60            # keep alive
RedisHost = "127.0.0.1"

# broker connect
def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

r = redis.Redis(host=RedisHost, port='6379')

# recieve message
def on_message(mqttc, obj, msg):
    m = str(msg.payload.decode("utf-8"))
#    print("message received " + m)
    list = m.split(" ")

    datetime = list[0] + " " + list[1]
#    print(datetime)
    sensor_list = list[2:]
    
#   Separete Key and Value
    sensor_key = sensor_list[0::2]
    sensor_value = sensor_list[1::2]
#    for key in sensor_key:
#        key = datetime + " " + key
#        print(key)
#    for value in sensor_value:
#        print(value)
    for key,value in zip(sensor_key,sensor_value):
        key = datetime + " " + key
#        print(key)
#        print(value)
        r.set(key, value)   
    
#    r.set('RPIvalue',m)
#    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

mqttc = mqtt.Client()
mqttc.on_message = on_message  # call back
mqttc.on_connect = on_connect
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEP_ALIVE)

mqttc.subscribe("Nakano-MQTT")  # name of topic

mqttc.loop_forever()  # loop

