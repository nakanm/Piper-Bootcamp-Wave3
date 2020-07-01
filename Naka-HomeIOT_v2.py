#!/usr/bin/env python3

import os
import RPi.GPIO as GPIO
import ADC0832
import datetime
import time
import paho.mqtt.client as mqtt

###### Edit variables to your environment #######
broker_address = "test.mosquitto.org"     #MQTT broker_address
Trigger = 16
Echo = 18
Topic = "Nakano-MQTT"
Msg = " "
Msg2 = " "
Msg3 = " "
Msg4 = " "
Msg5 = " "


# publish MQTT
print("creating new instance")
client = mqtt.Client("pub2") #create new instance

print("connecting to broker: %s" % broker_address)
client.connect(broker_address) #connect to broker

###############################################################
#        1. Temperature Cender                                #
#        2. Soil moisture detection                           #
#        3. Distance sensor                                   #
#        4. Light sensor                                      #
###############################################################
#--------------------------------------------------------------
#  Note: ds18b20's data pin must be connected to pin7(GPIO4).
#--------------------------------------------------------------

def init():
	ADC0832.setup()

# Reads temperature from sensor and prints to stdout
# id is the id of the sensor
def readSensor(id):
    global Msg
    tfile = open("/sys/bus/w1/devices/"+id+"/w1_slave")
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    temperature = temperature / 1000
#   print("Sensor: " + id  + " - Current temperature: %0.3f" % temperature)
    Msg = str("temperature %0.3f" % temperature)

# Reads temperature from all sensors found in /sys/bus/w1/devices/
# starting with "28-...
def readSensors():
    count = 0
    sensor = ""
    for file in os.listdir("/sys/bus/w1/devices/"):
        if (file.startswith("28-")):
            readSensor(file)
            count+=1
    if (count == 0):
        print ("No sensor found! Check connection")

# read distance sensor
def checkdist():
    GPIO.output(Trigger, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(Trigger, GPIO.LOW)
    while not GPIO.input(Echo):
        pass
    t1 = time.time()
    while GPIO.input(Echo):
        pass
    t2 = time.time()
    return (t2-t1)*340/2

GPIO.setmode(GPIO.BOARD)
GPIO.setup(Trigger,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(Echo,GPIO.IN)

# read sensor every 2second for all connected sensors
def loop():
    while True:
        readSensors()
        res = ADC0832.getResult()
        moisture = 255 - res
#        Msg2 = str('analog value: %03d moisture: %d' %(res, moisture))
        Msg2 = str('moisture %d' %(moisture))

        d = checkdist()
        df = "%0.2f" %d
        Msg3 = str('Distance %s' %df)

        res2 = ADC0832.getResult() - 80
        if res2 < 0:
            res2 = 0
        if res2 > 100:
            res2 = 100
#        print ('res2 = %d' % res2)
        Msg4 = ('Light %d' % res2)

        res3 = ADC0832.getResult()
        Gas_concentration = res3
#        print ('analog value: %03d Gas concentration: %d' %(res3, Gas_concentration))
        Msg5 = str('Gas-concentration %d' %(Gas_concentration))
#        d_time = datetime.datetime.now()
        d_date = datetime.datetime.now().date()
        d_time = datetime.datetime.now().time()
        d_time2 = d_time.strftime('%H:%M:%S') 

        Msg6 = str(d_date) + ' ' + str(d_time2) + ' ' + Msg + ' ' + Msg2 + ' ' + Msg3 + ' ' + Msg4 + ' ' + Msg5
        client.publish(Topic,Msg6)
        time.sleep(3600)

# Nothing to cleanup
def destroy():
    pass


###############################################################
# Main starts here
if __name__ == "__main__":
    init()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
        ADC0832.destroy()
        print ('Cleanup ADC! The end !')
