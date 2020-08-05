import paho.mqtt.client as mqtt
import time
import redis
import datetime


r = redis.Redis(host='', port='', password='') # put your credentials here!!!!!!!!!!!!



def on_message(client, userdata, message):
    m = str(message.payload.decode("utf-8"))
    #print str(datetime.datetime.now())
    print("message received " + m + "cm")
    
    r.set('RPIvalue',m)
    r.hset('RPIvalueHistory',str(datetime.datetime.now()),m)
    
    #timestamp = time.time()
    #print timestamp
    #dt_object = datetime.fromtimestamp(timestamp)
    #dt_object = "{0:%Y/%m/%d %H:%M:%S}".format(dt_object)
    #r.hset('RPItimetest', str(dt_object) , m)
    print("Store to Redis complete")
    
#    print("message topic=",message.topic)
#    print("message qos=",message.qos)
#    print("message retain flag=",message.retain)


broker_address="test.mosquitto.org"
print("creating new instance")
client = mqtt.Client("sub1") #create new instance
client.on_message = on_message  #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker

client.loop_start() #start the loop

while True:
    client.subscribe("topic")# put your topic here!!!!!!!!!!!
    time.sleep(1) # wait

client.loop_stop() #stop the loop
