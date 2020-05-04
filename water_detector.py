#!/usr/bin/python
import sys
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
from gpiozero import MotionSensor
import urllib2
import json
import os

led5=17
led4=26
led3=12
GPIO.setmode(GPIO.BCM)
GPIO.setup(led5,GPIO.OUT)
GPIO.setup(led4,GPIO.OUT)
GPIO.setup(led3,GPIO.OUT)
pir=MotionSensor(4)
#//////////////////////////////////
def sendNotification(token, channel, message):
    data = {
        "body" : message,
        "message_type" : "text/plain"
    }
    req = urllib2.Request('http://api.pushetta.com/api/pushes/{0}/'.format(channel))
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', 'Token {0}'.format(token))
    response = urllib2.urlopen(req, json.dumps(data))
#/////////////////////////////////
os.system('clear')
b=""
for i in "\t\t\t   Developed by Patata Group  \n":
    b=b+i
    print chr(27)+"[0;97m"+(b)
    time.sleep(0.05)
    os.system('clear')
for i in "\t\t\t  - Smart Irrigation System -":
    b=b+i
    print chr(27)+"[0;97m"+(b)
    time.sleep(0.08)
    os.system('clear')

time.sleep(0.10)
print chr(27)+"[0;92m"+"\t\t\t  - Smart Irrigation System -\n\n"

time.sleep(1.5)
#/////////////////////////////////

while True:
    humidity, temperature = Adafruit_DHT.read_retry(11,19)
    #////Sensor de humedad//////
    if humidity<61:
        GPIO.output(led3,GPIO.HIGH)
        print chr(27)+"[0;92m"+"\t  Sistema de riego activado"
        print chr(27)+"[0;39m"+'\tTemp: {0:0.1f}C  Humidity: {1:0.1f}%\n'.format(temperature, humidity)
        sendNotification("5bece809f43499fb718916401abb1c11478f58eb", "raspberry_pi3","Sistema de riego activado")
        print chr(27)+"[0;90m"+"-Notificacion enviada"
        time.sleep(10)
    if humidity>60:
        GPIO.output(led3,GPIO.LOW)  
        print chr(27)+"[0;30m"+"-----"
    #////Sensor de agua/////
    if pir.motion_detected:
        print chr(27)+"[0;96m"+"\t  Contenedor lleno"
        print chr(27)+"[0;39m"+"\thour:"+time.strftime('%l:%M %p %Z\n')
        GPIO.output(led5,GPIO.LOW)
        GPIO.output(led4,GPIO.HIGH)
        sendNotification("5bece809f43499fb718916401abb1c11478f58eb", "raspberry_pi3","El contenedor ha sido recargado")
        print chr(27)+"[0;90m"+"-Notificacion enviada"
        time.sleep(10)
    else:
        GPIO.output(led5,GPIO.HIGH)
        GPIO.output(led4,GPIO.LOW)
        print chr(27)+"[0;30m"+"-----"
    time.sleep(2)

