from umqtt import MQTTClient

import network
from time import sleep

MQTT_SERVER = "0.0.0.0"
MQTT_USER = "mqttuser"
MQTT_PASSWORD = "xyz" 
ssid = "abc"
password = "xyz"

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



def main(server="localhost"):
    connect_wifi()
    c = MQTTClient("pico_client", MQTT_SERVER, user=MQTT_USER, password=MQTT_PASSWORD)
    c.connect()
    c.publish(b"test", b"hello from pico")
    c.disconnect()

main()
