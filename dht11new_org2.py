import RPi.GPIO as GPIO
import dht11
import time
import datetime
import paho.mqtt.client as mqtt

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# read data using pin 18
instance = dht11.DHT11(pin=18)

###### Edit variables to your environment #######
broker_address = "test.mosquitto.org"    #MQTT broker_address
Topic = "keiya777"

try:
	while True:
	    result = instance.read()
	    if result.is_valid():
	        #print("Last valid input: " + str(datetime.datetime.now()))
	        #print("Temperature: %-3.1f C" % result.temperature)
	        #print("Humidity: %-3.1f %%" % result.humidity)

                 # publish MQTT
                 print("creating new instance")
                 client = mqtt.Client()

                 print("connecting to broker: %s" % broker_address)
                 client.connect(broker_address, 1883, keepalive=60)

                 # print("Publishing message: %s to topic: %s" % (Msg, Topic))
                 # client.publish(Topic,str(datetime.datetime.now()) + result.temperature + result.humidity)
                 #datetime = str(datetime.datetime.now())
                 # temp = str(result.temperature)
                 # humi = str(result.humidity)
                 client.publish(Topic,'DateTime: ' + str(datetime.datetime.now()) +  '    Temperature: ' + str(result.temperature) + '    Humidity: ' +  str(result.humidity))
                 # client.publish(Topic,str(datetime.datetime.now()) + str(result.temperature) + str(result.humidity))
                 #client.publish(Topic,'DayTime' + datetime + 'Temp' + tempe + 'Humi' +  humi)

	    time.sleep(6)


except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()