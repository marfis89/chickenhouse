#!/usr/bin/env python3
# pip3 install RPi.GPIO paho-mqtt sht_sensor w1thermsensor
import base64
import datetime
import time
import sys

import cv2
import paho.mqtt.client as mqtt
from sht_sensor import Sht
from w1thermsensor import W1ThermSensor, Unit

# define mqtt_prefix
mqtt_prefix = "chickenhome"

# define data
broker_ip = "localhost"
broker_port = 1883

# define send delta's
time_img_delta_delay = 1 #seconds
time_sensor_delta_delay = 60 #seconds

#define send cam bool 
sendImg = False

# sht10 sensor
sht_10_DATA_PIN = 24 #GPIO.BCM  # blue cable
sht_10_SCK_PIN = 23 #GPIO.BCM # yellow cable
sht_sensor = Sht(sht_10_SCK_PIN, sht_10_DATA_PIN )

# DS18S20 sensor
sensor = W1ThermSensor()

# camera stuff
def sendImgMqtt():  

    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH,640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
    #cam.set(cv2.CAP_PROP_BUFFERSIZE, 2)

    # first send on start
    ret, img = cam.read() 
    if ret: 
        for _ in range(5): 
            ret, img = cam.read()

        _, buffer = cv2.imencode('.jpg', img)
        base64image = base64.b64encode(buffer)

        image_string = "data:image/jpeg;base64," + str(base64image.decode())     

        client.publish(mqtt_prefix +"/img", image_string) 
        
    cam.release()
    

# sensor stuff
def sendSensor():

    try_W1ThermSensor = False
    
    # first sensor stuff
    try:
        temperature = round(sht_sensor.read_t(), 2)
        humidity = round(sht_sensor.read_rh(), 2) 
    except Exception:
        temperature = 0
        humidity = 0
        try_W1ThermSensor = True
        pass

    if try_W1ThermSensor:
        try:        
            temperature = sensor.get_temperature()            
        except Exception:
            temperature = 0     
            pass 

    client.publish(mqtt_prefix +"/temperature", temperature)
    client.publish(mqtt_prefix +"/humidity", humidity)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    
    client.message_callback_add(mqtt_prefix +"/sendImg", on_message_sendImg) 

    client.subscribe([(mqtt_prefix +"/sendImg",2)])

# The callback for when a PUBLISH message is received from the server.
def on_message_sendImg(client, userdata, msg):    
    print(msg.topic+" "+str(msg.payload.decode()))

    global sendImg

    if str(msg.payload.decode()) == "true":        
        sendImg = True

    if str(msg.payload.decode()) == "false":
        sendImg = False  

# main loop        
def main():   

    global sendImg     

    # initialize the timer
    send_img_timerstart = datetime.datetime.now()
    send_sensor_timerstart = datetime.datetime.now()        

    while True:
        
        try:
            timerend = datetime.datetime.now()
            time_img_delta = (timerend - send_img_timerstart).total_seconds() 
            time_sensor_delta = (timerend - send_sensor_timerstart).total_seconds()

            if time_img_delta >= time_img_delta_delay and sendImg:  
                sendImgMqtt()
                send_img_timerstart = datetime.datetime.now()      

            # prevent overflow   
            elif  time_img_delta >= (time_img_delta_delay*10): 
                send_img_timerstart = datetime.datetime.now()

            #s end sensor stuff
            if time_sensor_delta >= time_sensor_delta_delay:
                sendSensor()
                send_sensor_timerstart = datetime.datetime.now()            
            
            # sleep 
            time.sleep(1)

        except KeyboardInterrupt:
            print('Keyboard interrupted!')
            client.loop_stop()     
            #cam.release()       
            break        

if __name__ == "__main__":

    # initialize the mqtt client
    client = mqtt.Client()
    # client.username_pw_set(username, password)
    client.on_connect = on_connect   

    client.connect(broker_ip, broker_port, 60)
    client.loop_start() 

    # initialize the camera and grab a reference to the raw camera capture
    #cam = cv2.VideoCapture(0)
    #cam.set(cv2.CAP_PROP_FRAME_WIDTH,640)
    #cam.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
    #cam.set(cv2.CAP_PROP_BUFFERSIZE, 2)
    
    # allow the camera to warmup
    time.sleep(0.1)

    # first send on start
    sendImgMqtt()
    sendSensor()

    # run loop
    sys.exit(main())
