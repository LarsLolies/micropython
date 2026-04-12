import time
from neopixel import NeoPixel
num_pixels = 5
np = NeoPixel(num_pixels, 0, 16)


yellow = (255, 100, 0)
orange = (50, 255, 0)
green = (255, 0, 0)
blue = (0, 0, 255)
red = (0, 255, 0)
color0 = red


np.fill(orange)
print("Farbe Orange gesendet")
np.write()
