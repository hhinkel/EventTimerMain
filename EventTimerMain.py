import paho.mqtt.client as mqtt
import os
import time
import datetime
import urllib.parse
import json
from rider import Rider
from dbHelper import DbHelper
from setup import Setup

#Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with a result code of: " + str(rc))

def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    r = Rider(msg.payload)
    r.parseMessage()
    r.updateTables(setup.databaseFile)
    
def on_publish(client, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)

epoch = datetime.datetime(1970,1,1,0,0,0)
file = "setup.json"
Connected = False

setup = Setup(file)

db = DbHelper()

db.setDatabaseFile(setup.databaseFile)
db.openDatabaseFile()
db.connectToDatabase()
db.createXCTable()
db.createFenceTable()
db.createXCErrorTable()
db.closeDatabaseFile()

mqttc = mqtt.Client()

#Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

#Uncomment to enable debug messages
#mqttc.on_log = on_log

#Connect
mqttc.username_pw_set(setup.user, setup.key)
mqttc.connect(setup.server, int(setup.port))

#Start subscribe, with Qos level 0
mqttc.subscribe(setup.topic, 0)

mqttc.loop_start()

while Connected != True:
    time.sleep(0.1)

try: 
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    mqttc.disconnect()
    mqttc.loop_stop()

