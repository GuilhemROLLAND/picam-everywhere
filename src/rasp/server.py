
import sys
import paho.mqtt.client as mqtt
import cv2 as cv
import numpy as np

def sendPicture(mqttc):
    print("sendPicture")
    f=open("webcam.jpg", "rb") #3.7kiB in same folder
    fileContent = f.read()
    byteArr = bytearray(fileContent)
    mqttc.publish("picam-everywhere/tm", byteArr)

def takePicture():
    print("takePicture")
    # initialize the camera
    cam = cv.VideoCapture(0)   # 0 -> index of camera
    s, img = cam.read()
    if s:    # frame captured without any errors
        cv.namedWindow("cam-test")
        cv.imshow("cam-test",img)
        cv.waitKey(2000)
        cv.destroyWindow("cam-test")
        cv.imwrite("webcam.jpg",img) #save image

def decode_msg(mqttc, msg):
    if msg == "takePicture":
        takePicture()
        sendPicture(mqttc)
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
