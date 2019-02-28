# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 02:02:52 2019

@author: Ian
"""
import paho.mqtt.client as paho
import paho.mqtt.subscribe as subscribe
import requests
import json

broker = "<<YOUR MQTT BROKER IP >>"
port =1883
keepalive =60
#keepalive: maximum period in seconds allowed between communications with the broker. 
#If no other messages are being exchanged, this controls the rate at which the client will send ping messages to the broker

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

###### define callbacks ################################################################    

#the callback for when the client receives a CONNACK response from the server
#the value of rc indicates success or not:
#0: Connection successful 1: Connection refused - incorrect protocol version 
#2: Connection refused - invalid client identifier 3: Connection refused - server unavailable 
#4: Connection refused - bad username or password 5: Connection refused - not authorised 
#6-255: Currently unused.    
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code: " + str(rc) + "/n")
    pass

def on_disconnect(client, userdata, rc):
    if rc!=0:
        print("Unexpected disconnection")
    pass    
    
#the callback for when the broker has acknowledged the subscription
def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed to topic : " + str(mid) + " with Qos " + str(granted_qos) + "/n")
    pass

#the callback for when a PUBLISH message is received from the server
#if payload received matches, execute another command/script
def on_message(client, userdata, msg):
    print("Received message: "+ str(msg.payload) + " on topic" + str(msg.topic) 
    + " " + " with QoS " + str(msg.qos))
    
    ################## CONDITIONS INSERT HERE TO DEFINE THE CALLBACK YOU WANT FOR EACH MQTT topic listened to and the specific message for that topic filter #########################
    if msg.topic.decode() == "rpi/flame" and msg.payload.decode() == "High":
        print("calling on script to turn off gas valve...")
        
        ##### add command function to execute ######
        triggered("Open flame detected")
        turn_off_gasvalve()
        
    elif: ##############################
        
    else:
        ##################################
        
        
        
#instantiate an object of the mqtt client
#arguments:
#client_id: the unique client id string used when connecting to the broker        
#clean_session: a boolean that determines the client type. 
#If True, the broker will remove all information about this client when it disconnects. 
#If False, the client is a durable client and subscription information and queued messages
#will be retained when the client disconnects.        
#userdata: user defined data of any type that is passed as the userdata parameter to callbacks 
client= paho.Client(client_id= "rpi_sub", clean_session=False, 
                    userdata=None)

#client.max_inflight_messages.set()

#set a username and password for broker authentification
#called before connect*()
client.username_pw_set("<<YOUR MQTT BROKER USERNAME>>", "<<YOUR MQTT BROKER PASSWORD>>")

#client.reconnect_delay_set(min_delay=1, max_delay=120)

#assign the functions to the respective callbacks 
client.on_connect= on_connect
#client.on_subscribe= on_subscribe
client.on_message= on_message
client.on_disconnect= on_disconnect

#establish connection to the broker
client.connect(broker, port, keepalive)

#subscribe and listen to the specific MQTT topic
#allows multiple topic subscriptions in a single subscription command 
#client.subscribe([("rpi/flame", 1), ("rpi/pot", 1), ("rpi/gas", 1), ("rpi/flowrate", 1)])

#subscribe to a set of topics and process the messages received using a callback
subscribe.callback(callback=on_message, topics=["rpi/flame", "rpi/pot", "rpi/gas", "rpi/flowrate"], qos=1, 
                   hostname=broker, port=port, client_id="rpi_sub", keepalive=keepalive)

#the blocking call that processes network traffic, dispatches callbacks and handles automatic reconnecting
client.loop_forever()
