
import sys
import paho.mqtt.client as mqtt

def on_message(mqttc, userdata, message):
    print("Received message: " + str(message.payload.decode("utf-8")))
    mqttc.disconnect()
    exit()


def main() -> int:
    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.connect("broker.hivemq.com")
    mqttc.subscribe("picam-everywhere/tm")
    print("Send takePicture")
    info = mqttc.publish("picam-everywhere/tc", "takePicture")
    info.wait_for_publish()
    print("Waiting for message")
    mqttc.loop_forever()
    return 0

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
