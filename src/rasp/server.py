
import sys
import paho.mqtt.client as mqtt
import numpy as np
import os


def sendPicture(mqttc):
    print("sendPicture")
    f=open("webcam.jpg", "rb") #3.7kiB in same folder
    fileContent = f.read()
    byteArr = bytearray(fileContent)
    mqttc.publish("picam-everywhere/tm", byteArr)

def takePicture():
    print("takePicture")
    # initialize the camera
    stream = os.popen('fswebcam -r 1920x1080 --no-banner webcam.jpg')
    output = stream.read()
    return 0
    
def decode_msg(mqttc, msg):
    if msg == "takePicture":
        if takePicture() == 0:
            sendPicture(mqttc)
        else:
            print("Error taking picture")
    else:
        print("Unknown message")

def on_message(mqttc, userdata, message):
    print("Received message: " + str(message.payload.decode("utf-8")))
    decode_msg(mqttc, str(message.payload.decode("utf-8")))

def init_mqttc():
    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.connect("broker.hivemq.com")
    mqttc.subscribe("picam-everywhere/tc")
    return mqttc

def main() -> int:
    mqttc = init_mqttc()
    mqttc.loop_forever()
    # Normally never execute
    mqttc.disconnect()
    return 0

if __name__ == '__main__':
    main()
