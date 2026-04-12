from machine import Pin
import my_neopixel

print("Start")

np = my_neopixel.NeoPixel(Pin(34), 1)

np[0] = (255, 255, 255)  # Weiß = maximal sichtbar
np.write()

print("Gesendet")