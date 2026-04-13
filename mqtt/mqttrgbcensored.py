from umqtt import MQTTClient

import network
from time import sleep
from machine import Pin

MQTT_SERVER = "192.168.x.y"
MQTT_USER = "abc"
MQTT_PASSWORD = "xyz"
MQTT_TOPIC = "onBoardBlink"
ssid = "abc"
password = "xyz"

pin = Pin("LED", Pin.OUT)
colorPin1 = "#000000"
colorPin2 = "#000000"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)               
wlan.connect(ssid, password)

def connect_wifi():
    led1 = Pin(13, Pin.OUT)
    led1.off()
    connection_timeout = 60
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
           # Pin 17 → GP13
        print("Start")
        led1.on()
        time.sleep(1)



def sub_cb(topic, msg):
    global colorPin1, colorPin2
    print((topic, msg))
    
    if topic == b"breadboardRGB/Strip1" or topic == b"breadboardRGB/all":
        if msg.startswith(b"#"):
            set_color_hex(1, msg)
            colorPin1 = msg
        elif msg == b"off":
            set_color_hex(1, "#000000")
        elif msg == b"on":
            set_color_hex(1, colorPin1)
        
    if topic == b"breadboardRGB/Strip2" or topic == b"breadboardRGB/all":
        if msg.startswith(b"#"):
            set_color_hex(2, msg)
            colorPin2 = msg
        elif msg == b"off":
            set_color_hex(2, "#000000")
        elif msg == b"on":
            set_color_hex(2, colorPin2)
        





import array, time
from machine import Pin
import rp2

# =======================
# KONFIGURATION
# =======================
NUM_LEDS_1 = 3
NUM_LEDS_2 = 2

PIN_1 = 22
PIN_2 = 21

brightness = 0.1

# =======================
# PIO PROGRAMM
# =======================
@rp2.asm_pio(
    sideset_init=rp2.PIO.OUT_LOW,
    out_shiftdir=rp2.PIO.SHIFT_LEFT,
    autopull=True,
    pull_thresh=24
)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()

# =======================
# INITIALISIERUNG
# =======================

sm1 = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_1))
sm1.active(1)

sm2 = rp2.StateMachine(1, ws2812, freq=8_000_000, sideset_base=Pin(PIN_2))
sm2.active(1)

ar1 = array.array("I", [0 for _ in range(NUM_LEDS_1)])
ar2 = array.array("I", [0 for _ in range(NUM_LEDS_2)])

# =======================
# LED FUNKTIONEN
# =======================

def pixels_show():
    def send(sm, ar):
        dimmer_ar = array.array("I", [0 for _ in range(len(ar))])
        for i, c in enumerate(ar):
            r = int(((c >> 8) & 0xFF) * brightness)
            g = int(((c >> 16) & 0xFF) * brightness)
            b = int((c & 0xFF) * brightness)
            dimmer_ar[i] = (g << 16) + (r << 8) + b
        sm.put(dimmer_ar, 8)

    send(sm1, ar1)
    send(sm2, ar2)
    time.sleep_ms(10)

def pixels_set(strip, i, color):
    value = (color[0] << 16) | (color[1] << 8) | color[2]
    if strip == 1:
        ar1[i] = value
    elif strip == 2:
        ar2[i] = value

def pixels_fill(strip, color):
    if strip == 1:
        for i in range(NUM_LEDS_1):
            pixels_set(1, i, color)
    elif strip == 2:
        for i in range(NUM_LEDS_2):
            pixels_set(2, i, color)

# =======================
# HEX FUNKTION
# =======================

def set_color_hex(strip, hex_color):
    if hex_color.startswith("#"):
        hex_color = hex_color[1:]

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    pixels_fill(strip, (r, g, b))
    pixels_show()

# =======================
# MAIN
# =======================
def main(server="localhost"):

    
    

    connect_wifi()
    c = MQTTClient("umqtt_client", MQTT_SERVER, user=MQTT_USER, password=MQTT_PASSWORD)
    c.set_callback(sub_cb)
    
    c.connect()
    
    c.subscribe(b"breadboardRGB/Strip1")
    c.subscribe(b"breadboardRGB/Strip2")
    c.subscribe(b"breadboardRGB/all")
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


main()

# =======================
# START
# =======================

if __name__ == "__main__":
    main()



