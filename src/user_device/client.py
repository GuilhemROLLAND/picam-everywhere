
import paho.mqtt.client as mqtt
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


mqttc = mqtt.Client()
img_label = None


def takePicture(mqttc):
    print("Send takePicture")
    info = mqttc.publish("picam-everywhere/tc", "takePicture")
    info.wait_for_publish()

def on_message(mqttc, userdata, message):
    print("Received message!")
    # Deal with the message
    f = open('webcam.jpg', "wb")
    f.write(message.payload)
    f.close()
    # Update the image
    global img_label
    img2 = ImageTk.PhotoImage(get_resized_img())
    img_label.configure(image=img2)
    img_label.image = img2


def init_mqttc(mqttc):
    mqttc.on_message = on_message
    mqttc.connect("broker.hivemq.com")
    mqttc.subscribe("picam-everywhere/tm")
    return mqttc

def takePicture_click():
    takePicture(mqttc)

def get_resized_img():
    return Image.open("webcam.jpg").resize((960,540), Image.ANTIALIAS)

def main() -> int:
    # Start mqtt client
    global mqttc
    mqttc = init_mqttc(mqttc)
    # Wait forever
    global img_label
    print("GUI starting...")
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Button(frm, text="Take Picture...", command=takePicture_click).grid(column=0, row=1)
    # Load the image
    img = ImageTk.PhotoImage(get_resized_img())
    img_label = ttk.Label(frm, image=img)
    img_label.grid(column=0, row=0)
    mqttc.loop_start()

    root.mainloop()
    return 0

if __name__ == '__main__':
    main()
