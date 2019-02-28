# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 10:47:09 2019

@author: Ian
"""
import paho.mqtt.client as paho
import requests
import json

broker = "169.254.51.214"
port = 1883
keepalive = 60
#keepalive: maximum period in seconds allowed between communications with the broker. 
#If no other messages are being exchanged, this controls the rate at which the client will send ping messages to the broker

###### define callbacks ####################################################################################################################################

def turn_on_gasvalve():
    ##### INSERT CODE HERE TO TURN ON VALVE #############





    
def turn_off_gasvalve():    
    ##### INSERT CODE HERE TO TURN OFF VALVE ############
    



    
    
def triggered(message):
    url = 'https://bosch-ville-api.unificationengine.com/v1/message/send'
    api_token = 'Y2gmZGV2aWNlX3R5cGU9WERJ'
    headers = {'Content-Type': 'application/json', 'Authorization': api_token}
    body = {"phone_number": "+6590698810", "message":message}
    requests.post(url, data=json.dumps(body), headers=headers)    
        
##############################################################################################################################################################
#the callback for when the broker has acknowledged the subscription
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to topic : " + str(mid) + " with Qos " + str(granted_qos) + "/n")
    pass
        
#the callback for when a message has been sent to the broker
def on_publish(client, userdata, mid):
    print("Published to topic: " + str(mid) + "\n")
    
#the callback for when the client receives a CONNACK response from the server
#the value of rc indicates success or not:
#0: Connection successful 1: Connection refused - incorrect protocol version 
#2: Connection refused - invalid client identifier 3: Connection refused - server unavailable 
#4: Connection refused - bad username or password 5: Connection refused - not authorised 
#6-255: Currently unused.    
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code: " + str(rc) + "\n")

def on_disconnect(client, userdata, rc):
    if rc!=0:
        print("Unexpected disconnection") 

#the callback for when a PUBLISH message is received from the server
#if payload received matches, execute another command/script
def on_message(client, userdata, msg):
    print("Received message: "+ str(msg.payload) + " on topic" + str(msg.topic) 
    + " " + " with QoS " + str(msg.qos))
    
    ################## INSERT CONDITIONS BELOW HERE TO DEFINE THE CALLBACK YOU WANT FOR EACH MQTT topic listened to and the specific message for that topic filter #########################
    if msg.topic.decode() == "rpi/flame" and msg.payload.decode() == "High":
        print("calling on script to turn off gas valve...")
        
        ##### add command function to execute ######
        triggered("Open flame detected")
        turn_off_gasvalve()
        
    elif: ##############################
        
    else:
        ##################################







######################################################################################################################################################################################

#instantiate an object of the mqtt client
#arguments: 1.client_id: the unique client id string used when connecting to the broker        
#           2.clean_session: a boolean that determines the client type. 
#           If True, the broker will remove all information about this client when it disconnects. 
#           If False, the client is a durable client and subscription information and queued messages will be retained when the client disconnects.        
#           3.userdata: user defined data of any type that is passed as the userdata parameter to callbacks 
client = paho.Client("rpi_pub", clean_session= False, userdata=None) 

#assign the functions to the respective callbacks 
client.on_publish= on_publish
client.on_message= on_message
client.on_connect= on_connect
client.on_disconnect= on_disconnect

#set a username and password for broker authentification
#called before connect*()
client.username_pw_set("projectalfred", "projectalfred")

#client.max_inflight_messages.set()

client.reconnect_delay_set(min_delay=1, max_delay=120)

#establish connection to the broker
client.connect(broker, port, keepalive)


####################### INTEGRATE VARIABLES USED IN COMBINED SENSOR SCRIPT BELOW ##################################
flame_msg= ".........."
pot_msg= "............"
gas_msg= "..........."
flowrate_msg= "..........."

#publish the payload on the defined MQTT topic
#arguments:1.topic
#          2.payload: Passing an int or float will result in the payload being converted to a string representing that number
#          If you wish to send a true int/float, use struct.pack() to create the payload you require
#          3.qos: quality of service level to use
#          4.retain: if set to True, the message will be set as the retained message for the topic 
client.publish("rpi2/sensor/pot", str(pot_msg), qos=0, retain=False)
client.publish("rpi2/sensor/flame", str(flame_msg), qos=0, retain=False)
client.publish("rpi2/sensor/gas", str(gas_msg), qos=0, retain=False)
client.publish("rpi2/sensor/flowrate", str(flowrate_msg), qos=0, retain=False)

#subscribe and listen to the specific MQTT topic
#allows multiple topic subscriptions in a single subscription command 
client.subscribe([("rpi2/sensor/flame", 0), ("rpi2/sensor/pot", 0), ("rpi2/sensor/gas", 0), ("rpi2/sensor/flowrate", 0)])

#the blocking call that processes network traffic, dispatches callbacks and handles automatic reconnecting
client.loop_forever()            