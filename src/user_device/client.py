
import sys
import paho.mqtt.client as mqtt
import cv2 as cv
import numpy as np

def takePicture(mqttc):
    print("Send takePicture")
    info = mqttc.publish("picam-everywhere/tc", "takePicture")
    info.wait_for_publish()

def on_message(mqttc, userdata, message):
    print("Received message!")
    f = open('webcam.jpg', "wb")
    f.write(message.payload)
    mqttc.disconnect()
    exit()

def init_mqttc():
    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.connect("broker.hivemq.com")
    mqttc.subscribe("picam-everywhere/tm")
    return mqttc

def main() -> int:
    # Start mqtt client
    mqttc = init_mqttc()
    # Send order to take picture
    takePicture(mqttc)
    # Wait forever
    print("Waiting for message...")
    mqttc.loop_forever()
    return 0

if __name__ == '__main__':
    main()
