
import sys
import paho.mqtt.client as mqtt
import cv2 as cv
def sendPicture(mqttc):
    print("sendPicture")
    # TODO: send picture
    mqttc.publish("picam-everywhere/tm", "pictureTaken")

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

def main() -> int:
    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.connect("broker.hivemq.com")
    mqttc.subscribe("picam-everywhere/tc")
    mqttc.loop_forever()
    mqttc.disconnect()
    return 0

if __name__ == '__main__':
    main()
