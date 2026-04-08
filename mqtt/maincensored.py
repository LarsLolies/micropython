from umqtt import MQTTClient
from machine import Pin

import network
from time import sleep

MQTT_SERVER = "0.0.0.0"
MQTT_USER = "mqttuser"
MQTT_PASSWORD = "xyz" 
MQTT_TOPIC = "onBoardBlink"
ssid = "abc"
password = "xyz"

pin = Pin("LED", Pin.OUT)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)               
wlan.connect(ssid, password)

def connect_wifi():
    connection_timeout = 20
    while connection_timeout > 0:
        if wlan.status() >= 3:
            break
        connection_timeout -= 1
        print("Connecting to WiFi...")
        sleep(1)
    if wlan.status() != 3:
        raise RuntimeError("WiFi connection failed")
    else:
        print("Connected to WiFi")
        network_info = wlan.ifconfig()
        print("IP Address:", network_info[0])

def sub_cb(topic, msg):
    
    print((topic, msg))
    if msg==b"on":
        pin.on()
    elif msg==b"off":
        pin.off()


def main(server="localhost"):
    connect_wifi()
    c = MQTTClient("umqtt_client", MQTT_SERVER, user=MQTT_USER, password=MQTT_PASSWORD)
    c.set_callback(sub_cb)
    
    c.connect()
    
    c.subscribe(b"onBoardBlink")
    while True:
        if True:
            # Blocking wait for message
            c.wait_msg()
        else:
            # Non-blocking wait for message
            c.check_msg()
            # Then need to sleep to avoid 100% CPU usage (in a real
            # app other useful actions would be performed instead)
            time.sleep(1)

    c.disconnect()



if __name__ == "__main__":
    main()